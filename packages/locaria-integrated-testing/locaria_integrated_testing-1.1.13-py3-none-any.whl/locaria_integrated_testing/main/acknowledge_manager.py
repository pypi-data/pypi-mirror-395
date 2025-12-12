"""
AcknowledgeManager - Firestore-backed issue acknowledgment and mute tracking.

Manages per-issue acknowledgment state to prevent email spam. Uses Firestore
subcollections: one document per test, with an 'issues' subcollection containing
one document per unique issue. Supports permission-based access control via
issue_owner / issue_ack_access fields (single string or list of strings).

Firestore Structure:
  Collection: pipeline_acknowledgments
  └── Document: {repo}%{pipeline}%{test_name}
      ├── Fields:
      │   ├── test_name: str
      │   └── last_updated: timestamp (UTC)
      └── Subcollection: issues
          └── Document: {issue_key_simple}  # Normalized identifier (lowercase, stripped)
              ├── acknowledged: bool
              ├── muted_until: timestamp (UTC) | None
              ├── identifier: str  # Original issue identifier
              ├── details: str  # Human-readable issue description
              ├── issue_first_occurrence: timestamp (UTC)
              ├── issue_last_occurrence: timestamp (UTC)
             ├── issue_owner: Union[str, List[str]]  # Primary permission(s) required to acknowledge
             ├── issue_ack_access: Union[str, List[str]]  # Secondary/alias permissions with same access
              ├── acknowledged_by: str | None  # Email of person who acknowledged
              ├── acknowledged_at: timestamp (UTC) | None
              ├── acknowledgment_reason: str | None
              └── additional_metadata: Dict[str, Any]  # Pipeline-specific fields (status, email, etc.)

Example Document Path:
  pipeline_acknowledgments/locate_2_pulls%capacity_tracker%check_consistent_daily_hours_per_person/issues/john.doe@locaria.com
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Union
from google.cloud import firestore


class AcknowledgeManager:
    """
    Manages issue acknowledgment and mute state in Firestore.
    
    Tracks which issues have been acknowledged, by whom, and until when they're muted.
    Supports permission-based access control through issue_owner / issue_ack_access fields. Uses batch
    operations for efficiency when updating multiple issues.
    
    Key operations:
    - Check if issue is currently acknowledged/muted
    - Acknowledge individual issues with configurable mute period
    - Batch-update issue detection tracking
    - Filter test results by acknowledgment status
    """
    
    def __init__(
        self,
        firestore_client: firestore.Client,
        repository_name: str,
        pipeline_name: str,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the AcknowledgeManager.
        
        Args:
            firestore_client: Firestore client instance
            repository_name: Name of the repository (e.g., 'locate_2_pulls')
            pipeline_name: Name of the pipeline (e.g., 'capacity_tracker_linguists_days_off')
        """
        self.firestore_client = firestore_client
        self.repository_name = repository_name
        self.pipeline_name = pipeline_name

        # Acknowledgment-related configuration (all overridable via Firestore config)
        ack_cfg = (config or {}).get("acknowledgments", {})

        # Firestore collection that stores per-test documents
        self.collection = ack_cfg.get("collection_name", "pipeline_acknowledgments")
        # Name of the per-test subcollection that stores per-issue documents
        self.issue_subcollection_name = ack_cfg.get("issue_subcollection_name", "issues")

        # Default behavior knobs
        self.default_mute_days = ack_cfg.get("default_mute_days", 7)
        self.max_emails_per_day = ack_cfg.get("max_emails_per_day", 1)
    
    def _generate_document_id(self, test_name: str) -> str:
        """
        Generate document ID for a given test.
        
        Args:
            test_name: Name of the test
            
        Returns:
            Document ID in format: {repo}%{pipeline}%{test_name}
        """
        return f"{self.repository_name}%{self.pipeline_name}%{test_name}"
    
    
    def check_issue_acknowledged(self, test_name: str, issue_identifier: str) -> bool:
        """
        Check if specific issue is acknowledged and still muted.
        
        Args:
            test_name: Name of the test (e.g., 'check_consistent_daily_hours_per_person')
            issue_identifier: Primary identifier (e.g., 'john.doe@locaria.com', 'employee_123')
            
        Returns:
            True if issue is acknowledged and mute period hasn't expired, False otherwise
            
        Example:
            >>> is_muted = manager.check_issue_acknowledged(
            ...     'check_duplicate_records',
            ...     'john.doe@locaria.com'
            ... )
            >>> # Returns True if acknowledged within last 7 days (default mute period)
        """
        try:
            # Build Firestore path: pipeline_acknowledgments/{repo}%{pipeline}%{test}/issues/{issue_key}
            doc_id = self._generate_document_id(test_name)
            issue_key_simple = str(issue_identifier).lower().strip()
            issue_doc_ref = (
                self.firestore_client.collection(self.collection)
                .document(doc_id)
                .collection(self.issue_subcollection_name)
                .document(issue_key_simple)
            )
            issue_doc = issue_doc_ref.get()
            
            # Return False if issue doesn't exist (not yet acknowledged)
            if not issue_doc.exists:
                return False
            
            issue = issue_doc.to_dict() or {}
            
            # Return False if not acknowledged (user hasn't muted this issue yet)
            if not issue.get('acknowledged', False):
                return False
            
            # Check if mute period has expired (muted_until is in the past)
            mute_until = issue.get('muted_until')
            if not mute_until:
                return False
            
            # Normalize Firestore timestamp to datetime for comparison (handles both Timestamp and string formats)
            if hasattr(mute_until, 'timestamp'):
                mute_until = datetime.fromtimestamp(mute_until.timestamp(), tz=timezone.utc)
            elif isinstance(mute_until, str):
                mute_until = datetime.fromisoformat(mute_until.replace('Z', '+00:00'))
            
            # Return True if still within mute period (prevents email spam for known issues)
            current_time = datetime.now(timezone.utc)
            return current_time < mute_until
            
        except Exception as e:
            print(f"Warning: Error checking acknowledgment status: {e}")
            return False
    
    def acknowledge_issue(self, test_name: str, issue_identifier: str, 
                         acknowledged_by: str) -> bool:
        """
        Acknowledge specific issue and mute for configured period.
        
        Sets acknowledged=True and muted_until to current_time + default_mute_days.
        Preserves existing issue_first_occurrence and issue owner/access fields.
        
        Args:
            test_name: Name of the test (e.g., 'check_consistent_daily_hours_per_person')
            issue_identifier: Primary identifier (e.g., 'john.doe@locaria.com')
            acknowledged_by: Email of person acknowledging (e.g., 'admin@locaria.com')
            
        Returns:
            True if successful, False otherwise
            
        Example:
            >>> success = manager.acknowledge_issue(
            ...     'check_duplicate_records',
            ...     'john.doe@locaria.com',
            ...     'admin@locaria.com'
            ... )
            >>> # Mutes issue for 7 days (default), prevents email notifications
        """
        try:
            # Generate document ID for the test
            doc_id = self._generate_document_id(test_name)
            # Work directly with the per-issue document in the `issues` subcollection
            issues_collection = (
                self.firestore_client.collection(self.collection)
                .document(doc_id)
                .collection(self.issue_subcollection_name)
            )

            # Create issue key (simple identifier)
            issue_key_simple = str(issue_identifier).lower().strip()
            issue_doc_ref = issues_collection.document(issue_key_simple)
            existing_doc = issue_doc_ref.get()
            existing_data: Dict[str, Any] = existing_doc.to_dict() if existing_doc.exists else {}

            # Update the issue using the new per-document structure
            current_time = datetime.now(timezone.utc)
            mute_until = current_time + timedelta(days=self.default_mute_days)

            # Preserve existing owner / first occurrence where available
            issue_first_occurrence = existing_data.get("issue_first_occurrence", current_time)
            issue_owner = existing_data.get("issue_owner", "analytic_hub.data_team_ack")
            issue_ack_access = existing_data.get("issue_ack_access", issue_owner)

            update_data = {
                "acknowledged": True,
                "muted_until": mute_until,
                "identifier": existing_data.get("identifier", issue_identifier),
                "details": existing_data.get("details", ""),
                "issue_first_occurrence": issue_first_occurrence,
                "issue_last_occurrence": current_time,
                "issue_owner": issue_owner,
                "issue_ack_access": issue_ack_access,
                "acknowledged_by": acknowledged_by,
                "acknowledged_at": current_time,
            }

            # Save/merge the document so we don't drop other metadata fields
            issue_doc_ref.set(update_data, merge=True)
            return True
            
        except Exception as e:
            print(f"❌ Error acknowledging issue: {e}")
            return False
    
    def batch_update_issue_detections(
            self,
            test_name: str,
            issues: List[Dict[str, Any]]
    ) -> bool:
        """
        Batch-update Firestore with issue detection tracking for a single test.
        
        Efficiently handles multiple issues in one batch operation. Preserves existing
        acknowledgment state while updating occurrence timestamps and metadata. Uses
        batch read to minimize Firestore round trips.
        
        Args:
            test_name: Name of the test (e.g., 'check_consistent_daily_hours_per_person')
            issues: List of issue dictionaries, each containing:
                - issue_identifier: str (e.g., 'john.doe@locaria.com')
                - issue_details: str (e.g., 'Expected 35h/week, found 28h/week')
                - additional_metadata: Dict with optional fields like:
                  - issue_owner / issue_ack_access: Union[str, List[str]] (permission(s))
                  - status: str ('WARN' or 'FAIL')
                  - email: str, person_name: str, etc.
        
        Returns:
            True if successful, False otherwise
            
        Example:
            >>> issues = [
            ...     {
            ...         'issue_identifier': 'john.doe@locaria.com',
            ...         'issue_details': 'Expected 35h/week, found 28h/week',
            ...         'additional_metadata': {
            ...             'issue_owner': 'analytics_hub.data_team_ack',
            ...             'status': 'WARN',
            ...             'email': 'john.doe@locaria.com',
            ...             'person_name': 'John Doe'
            ...         }
            ...     }
            ... ]
            >>> manager.batch_update_issue_detections('check_hours', issues)
            >>> # Updates Firestore: sets issue_last_occurrence, preserves acknowledged state
        """
        if not issues:
            return True
        
        try:
            doc_id = self._generate_document_id(test_name)
            test_doc_ref = self.firestore_client.collection(self.collection).document(doc_id)
            issues_collection = test_doc_ref.collection(self.issue_subcollection_name)

            now_utc = datetime.now(timezone.utc)

            # Phase 1: Preprocess all issues to build document refs and payloads (batch processing minimizes Firestore round trips)
            issue_entries: List[Dict[str, Any]] = []
            doc_refs: List[firestore.DocumentReference] = []

            for issue in issues:
                issue_identifier = issue.get("issue_identifier")
                # Skip issues without identifiers (can't create stable document key without identifier)
                if not issue_identifier:
                    continue

                issue_details = issue.get("issue_details", "")
                additional_metadata = issue.get("additional_metadata") or {}

                # Normalize issue key (lowercase, trimmed) for case-insensitive lookup and consistent document IDs
                issue_key_simple = str(issue_identifier).lower().strip()
                issue_doc_ref = issues_collection.document(issue_key_simple)

                # Enrich details string with key metrics for better visibility in Analytics Hub UI
                details = f"{issue_details}"
                if additional_metadata:
                    if "absent_percentage" in additional_metadata:
                        details += f" - {additional_metadata['absent_percentage']}% absent"
                    elif "expected_weekly_hours" in additional_metadata:
                        details += f" - Expected {additional_metadata['expected_weekly_hours']}h/week"

                issue_entries.append({
                    "key": issue_key_simple,
                    "identifier": issue_identifier,
                    "details": details,
                    "additional_metadata": additional_metadata,
                    "doc_ref": issue_doc_ref,
                })
                doc_refs.append(issue_doc_ref)

            if not issue_entries:
                return True

            # Phase 2: Batch-fetch existing documents to preserve acknowledgment state (prevents losing mute status on updates)
            existing_docs = {}
            for doc in self.firestore_client.get_all(doc_refs):
                if doc.exists:
                    existing_docs[doc.id] = doc.to_dict()

            batch = self.firestore_client.batch()

            # Ensure parent test document has fields (prevents placeholder/italic documents in Firestore console, makes them queryable)
            batch.set(test_doc_ref, {
                "test_name": test_name,
                "last_updated": now_utc,
            }, merge=True)

            # Track expired mutes for consolidated logging
            expired_mutes: List[Dict[str, str]] = []

            # Phase 3: Build update payloads for each issue, preserving existing acknowledgment state
            for entry in issue_entries:
                key = entry["key"]
                issue_identifier = entry["identifier"]
                details = entry["details"]
                additional_metadata = entry["additional_metadata"]
                issue_doc_ref = entry["doc_ref"]

                existing_data = existing_docs.get(key) or {}
                is_new_issue = not bool(existing_data)
                
                # Check if existing issue's mute period has expired
                mute_expired = False
                if existing_data:
                    existing_acknowledged = existing_data.get("acknowledged", False)
                    muted_until = existing_data.get("muted_until")
                    
                    # If issue is acknowledged and has a mute_until timestamp, check if it's expired
                    if existing_acknowledged and muted_until:
                        # Handle both Firestore Timestamp and datetime objects
                        if hasattr(muted_until, 'timestamp'):
                            # Firestore Timestamp object
                            mute_expiry_time = datetime.fromtimestamp(muted_until.timestamp(), tz=timezone.utc)
                        elif isinstance(muted_until, datetime):
                            # Already a datetime object
                            mute_expiry_time = muted_until if muted_until.tzinfo else muted_until.replace(tzinfo=timezone.utc)
                        else:
                            mute_expiry_time = None
                        
                        if mute_expiry_time and now_utc > mute_expiry_time:
                            mute_expired = True
                            # Archive the expired issue before creating a new one
                            test_doc_ref = self.firestore_client.collection(self.collection).document(doc_id)
                            archive_ref = test_doc_ref.collection("archives").document(key)
                            
                            # Prepare archived issue data (match structure used in delete_issue)
                            archived_issue_data = {
                                "original_document_id": doc_id,
                                "issue_key": key,
                                "issue": existing_data.copy(),  # Original issue data preserved
                                "archived_at": now_utc,
                                "archive_reason": "mute_expired",
                            }
                            
                            # Write to archive and delete from active issues
                            batch.set(archive_ref, archived_issue_data)
                            batch.delete(issue_doc_ref)
                            
                            # Mark as new issue since we're archiving the old one
                            is_new_issue = True
                            existing_data = {}  # Clear existing data so we create fresh issue
                            
                            # Track for consolidated logging
                            expired_mutes.append({
                                "identifier": issue_identifier,
                                "muted_until": mute_expiry_time.isoformat() if mute_expiry_time else "unknown"
                            })

                # Resolve issue_owner: explicit override > existing value > default (allows permission updates without losing history)
                owner_override = additional_metadata.get("issue_owner")
                existing_owner = existing_data.get("issue_owner")
                issue_owner = owner_override or existing_owner or "analytic_hub.data_team_ack"

                ack_access_override = additional_metadata.get("issue_ack_access")
                existing_ack_access = existing_data.get("issue_ack_access")
                issue_ack_access = ack_access_override or existing_ack_access or issue_owner

                # Preserve first occurrence for new issues, always update last occurrence (tracks issue lifecycle)
                issue_first_occurrence = existing_data.get("issue_first_occurrence") or now_utc

                update_data: Dict[str, Any] = {
                    "identifier": issue_identifier,
                    "details": details,
                    "issue_first_occurrence": issue_first_occurrence,
                    "issue_last_occurrence": now_utc,
                    "issue_owner": issue_owner,
                    "issue_ack_access": issue_ack_access,
                    **additional_metadata,
                }

                # New issues: initialize acknowledgment fields to False/None
                if is_new_issue:
                    update_data.setdefault("acknowledged", False)
                    update_data.setdefault("muted_until", None)
                else:
                    # For existing issues, preserve acknowledgment state (unless mute expired, then it's already archived)
                    if not mute_expired:
                        update_data["acknowledged"] = existing_data.get("acknowledged", False)
                        update_data["muted_until"] = existing_data.get("muted_until")

                # Only set if not already deleted (mute_expired case)
                if not mute_expired:
                    batch.set(issue_doc_ref, update_data, merge=True)
                else:
                    # Create new issue document since old one was archived
                    batch.set(issue_doc_ref, update_data)

            # Log consolidated summary of expired mutes if any
            if expired_mutes:
                if len(expired_mutes) == 1:
                    print(f"[INFO] Archived 1 expired mute for test '{test_name}': {expired_mutes[0]['identifier']} (muted_until: {expired_mutes[0]['muted_until']})")
                else:
                    identifiers = [m['identifier'] for m in expired_mutes]
                    print(f"[INFO] Archived {len(expired_mutes)} expired mutes for test '{test_name}': {', '.join(identifiers[:5])}{'...' if len(identifiers) > 5 else ''}")

            batch.commit()
            return True
        
        except Exception as e:
            print(f"❌ Error updating multiple issue detections: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def filter_acknowledged_issues(self, test_results: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Filter test results into new vs acknowledged issues.
        
        Separates test results into two lists: new issues that need attention, and
        acknowledged issues that are muted. Used by email system to prevent spam.
        
        Args:
            test_results: List of test result dictionaries. Each dict should have:
                - 'issue_identifier': Unique identifier (e.g., 'john.doe@locaria.com')
                - 'test_name': Name of the test (e.g., 'check_consistent_daily_hours_per_person')
                - 'acknowledgeable': Boolean indicating if issue can be acknowledged
                - 'status': 'WARN' or 'FAIL'
                - 'message': str, 'metrics': Dict, etc.
            
        Returns:
            Dictionary with two keys:
                - 'new_issues': List[Dict] - Issues that are not acknowledged/muted
                - 'acknowledged_issues': List[Dict] - Issues that are currently muted
            
        Example:
            >>> test_results = [
            ...     {
            ...         'test_name': 'check_hours',
            ...         'issue_identifier': 'john.doe@locaria.com',
            ...         'acknowledgeable': True,
            ...         'status': 'WARN',
            ...         'message': 'Hours mismatch'
            ...     },
            ...     {
            ...         'test_name': 'check_hours',
            ...         'issue_identifier': 'jane.smith@locaria.com',
            ...         'acknowledgeable': True,
            ...         'status': 'WARN',
            ...         'message': 'Hours mismatch'
            ...     }
            ... ]
            >>> filtered = manager.filter_acknowledged_issues(test_results)
            >>> # Returns: {
            >>> #     'new_issues': [...],  # Issues not yet acknowledged
            >>> #     'acknowledged_issues': [...]  # Issues currently muted
            >>> # }
        """
        new_issues = []
        acknowledged_issues = []
        
        for result in test_results:
            # Non-acknowledgeable issues always go to new_issues (can't be muted, always need attention)
            if not result.get('acknowledgeable', True):
                new_issues.append(result)
                continue
            
            # Extract issue identifier and test name (required to check acknowledgment status in Firestore)
            result_issue_identifier = result.get('issue_identifier')
            test_name = result.get('test_name')
            
            # If metadata missing, treat as new (can't check acknowledgment without identifier)
            if not all([result_issue_identifier, test_name]):
                new_issues.append(result)
                continue
            
            # Check Firestore to see if this specific issue is currently muted
            is_acknowledged = self.check_issue_acknowledged(test_name, result_issue_identifier)
            
            # Route to appropriate list (muted issues excluded from email digests to prevent spam)
            if is_acknowledged:
                acknowledged_issues.append(result)
            else:
                new_issues.append(result)
        
        return {
            'new_issues': new_issues,
            'acknowledged_issues': acknowledged_issues
        }
    


# Convenience functions for easy import
def create_acknowledge_manager(firestore_client: firestore.Client, 
                              repository_name: str, pipeline_name: str) -> AcknowledgeManager:
    """Create a new AcknowledgeManager instance."""
    return AcknowledgeManager(firestore_client, repository_name, pipeline_name)


