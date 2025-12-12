"""
PermissionResolver - Resolve email recipients from Access Controller Firestore.

Looks up bindings/roles/permissions stored in the Access Controller (see
FIN_profitability_gcp/modules/utility_modules/access_controller.py) to determine
which users belong to a given permission string. Used by the integrated testing
framework to auto-route alerts to the correct acknowledge owner(s).
"""

from typing import Iterable, List, Optional, Set, Union

from google.cloud import firestore
from .config_manager import DEFAULT_PERMISSION_RESOLVER_PROJECT_ID

class PermissionResolver:
    """Resolve permission strings to user email addresses via Firestore."""

    _client_cache = {}

    def __init__(self, project_id: str = DEFAULT_PERMISSION_RESOLVER_PROJECT_ID):
        self.project_id = project_id
        self.client = self._init_client(project_id)
        self._permission_cache: dict[str, List[str]] = {}

    def _init_client(self, project_id: str) -> Optional[firestore.Client]:
        """
        Initialize Firestore client with caching so only one client per project exists.
        """
        if not project_id:
            return None

        cached_client = PermissionResolver._client_cache.get(project_id)
        if cached_client is not None:
            return cached_client

        try:
            client = firestore.Client(project=project_id)
            PermissionResolver._client_cache[project_id] = client
            return client
        except Exception as exc:  # pragma: no cover - defensive logging
            print(
                f"Warning: Unable to initialize Firestore client for permission resolver "
                f"(project: {project_id}): {exc}"
            )
            return None

    def get_emails_for_permissions(
        self, permissions: Union[str, Iterable[str]]
    ) -> List[str]:
        """
        Resolve one or many permission strings to a unique list of user emails.
        """
        if not permissions:
            return []

        if isinstance(permissions, str):
            permission_list = [permissions]
        else:
            permission_list = list(permissions)

        recipients: Set[str] = set()
        for permission in permission_list:
            emails = self._get_emails_for_single_permission(permission)
            recipients.update(emails)

        return sorted(recipients)

    def _get_emails_for_single_permission(self, permission: Optional[str]) -> List[str]:
        """Return cached recipients for a single permission."""
        if not permission or not isinstance(permission, str):
            return []

        normalized_permission = permission.strip()
        if not normalized_permission:
            return []

        if normalized_permission in self._permission_cache:
            return self._permission_cache[normalized_permission]

        emails = self._query_emails_by_permission(normalized_permission)
        self._permission_cache[normalized_permission] = emails
        return emails

    def _query_emails_by_permission(self, permission: str) -> List[str]:
        """
        Query Firestore for all bindings that include roles owning the permission.
        """
        if not self.client:
            return []

        try:
            # Use positional arguments for Firestore where() query (correct syntax)
            role_docs = (
                self.client.collection("roles")
                .where("permissions", "array_contains", permission)
                .stream()
            )
            role_names = [doc.id for doc in role_docs]
        except Exception as exc:  # pragma: no cover - defensive logging
            print(
                f"Warning: Unable to fetch roles for permission '{permission}': {exc}"
            )
            return []

        if not role_names:
            return []

        emails: Set[str] = set()
        bindings_collection = self.client.collection("bindings")

        for role in role_names:
            try:
                # Use positional arguments for Firestore where() query (correct syntax)
                matching_bindings = (
                    bindings_collection.where("roles", "array_contains", role).stream()
                )
                for binding in matching_bindings:
                    email = (binding.id or "").strip()
                    if email:
                        emails.add(email)
            except Exception as exc:  # pragma: no cover - defensive logging
                print(
                    f"Warning: Unable to fetch bindings for role '{role}' "
                    f"(permission '{permission}'): {exc}"
                )

        return sorted(emails)

