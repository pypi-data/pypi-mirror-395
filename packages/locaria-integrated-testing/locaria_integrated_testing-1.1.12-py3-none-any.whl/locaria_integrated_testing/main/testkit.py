"""
TestKit - Core orchestration engine for integrated testing framework.

Orchestrates test execution, result logging, email alerting, and acknowledgment tracking.
Manages shared resources (BigQuery client, Firestore client) across test runs for efficiency.
Handles test result aggregation, filtering by acknowledgment status, and finalization.
"""

import os
import json
import requests
import uuid
import pandas as pd
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Set
from google.cloud import firestore
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

from .acknowledge_manager import AcknowledgeManager
from ..utils.permission_resolver import PermissionResolver
from .. import __version__

class TestFailureException(Exception):
    """Custom exception raised when a test fails and fail_on_error is True."""
    pass

class TestKit:
    """
    Central orchestrator for test execution, logging, and alerting.
    
    Manages the full test lifecycle: initialization, result collection, acknowledgment
    filtering, email notifications, and finalization. Uses shared resource caching to
    minimize initialization overhead across multiple test runs.
    
    Key responsibilities:
    - Test result logging (pass/warn/fail) with structured metrics
    - Email alerting with acknowledgment-aware filtering
    - Firestore configuration management
    - BigQuery logging for historical tracking
    - Idempotent finalization to prevent duplicate notifications
    """
    
    # Class-level cache for shared resources
    _shared_bigquery_client = None
    _shared_firestore_client = None
    _shared_config = None
    
    def __init__(self, repository_name: str, pipeline_name: str = None, fail_on_error: bool = False, 
                 firestore_project_id: str = None, bigquery_client = None, bigquery_project_id: str = None):
        """
        Initialize the TestKit with repository and pipeline information.
        
        Sets up shared resources (BigQuery client, Firestore client) with caching for efficiency.
        Loads configuration from Firestore and initializes acknowledgment manager.
        
        Args:
            repository_name: Name of the repository (e.g., 'locate_2_pulls')
            pipeline_name: Name of the specific pipeline (e.g., 'plunet_employee_table')
            fail_on_error: If True, pipeline stops on test failures. If False, continues with alerts.
            firestore_project_id: Optional GCP project ID (defaults to 'locaria-dev-config-store')
            bigquery_client: Optional BigQuery client instance for test result logging
            
        Example:
            >>> testkit = TestKit(
            ...     repository_name='locate_2_pulls',
            ...     pipeline_name='plunet_employee_table',
            ...     fail_on_error=False,
            ...     firestore_project_id='locaria-dev-config-store'
            ... )
            >>> # Initializes with shared resource caching, loads config from Firestore
        """
        # Print version on initialization
        print(f"[INFO] Locaria Integrated Testing Framework v{__version__}")
        
        self.repository_name = repository_name
        self.pipeline_name = pipeline_name or "unknown"
        self.fail_on_error = fail_on_error
        self.run_id = self._generate_run_id()
        self.test_results = []
        self.warnings = []
        self.failures = []
        self.failure_emails_sent = False  # Track if failure email has been sent
        self.finalized = False  # Track if finalize_run() has been called to prevent duplicate execution
        self.start_time = datetime.now(timezone.utc)
        
        
        # Store provided parameters and fallbacks
        from ..utils.config_manager import (
            DEFAULT_FIRESTORE_PROJECT_ID,
            DEFAULT_BIGQUERY_PROJECT_ID,
            DEFAULT_BIGQUERY_DATASET_ID,
            DEFAULT_BIGQUERY_TEST_LOGS_TABLE,
            DEFAULT_PERMISSION_RESOLVER_PROJECT_ID
        )
        
        # --- GCP resource configuration block ---
        self.collection_integrated_testing_config = DEFAULT_FIRESTORE_PROJECT_ID
        self._firestore_project_id = firestore_project_id or DEFAULT_FIRESTORE_PROJECT_ID
        self._bigquery_project_id = bigquery_project_id or DEFAULT_BIGQUERY_PROJECT_ID
        self._bigquery_client = bigquery_client
        self._default_dataset_id = DEFAULT_BIGQUERY_DATASET_ID
        self._default_test_logs_table = DEFAULT_BIGQUERY_TEST_LOGS_TABLE
        env_permission_project = os.getenv("TESTKIT_ACCESS_CONTROL_PROJECT")
        self._permission_project_id = (
            env_permission_project
            or DEFAULT_PERMISSION_RESOLVER_PROJECT_ID
        )
        
        # Initialize BigQuery client for test result logging
        self.bigquery_client = self._init_bigquery_client()
        
        # Initialize Firestore client for configuration
        self.firestore_client = self._init_firestore_client()
        
        # Load configuration from Firestore
        self.config = self._load_config_from_firestore()
        self.bigquery_logging_config = self.config.get(
            'bigquery_logging',
            self._get_default_bigquery_logging_config()
        )

        # Permission resolver for access-controller lookups (Fire
        # store project defaults to locaria-prod-authenticator).
        self._permission_resolver: Optional[PermissionResolver] = None
        
        # Initialize acknowledgment manager with config (for collection names etc.)
        self.acknowledge_manager = AcknowledgeManager(
            self.firestore_client,
            self.repository_name,
            self.pipeline_name,
            config=self.config,
        )
        
        # Log test run start
        self._log_run_start()
    
    
    def _generate_run_id(self) -> str:
        """Generate unique run identifier with timestamp and UUID."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"{self.repository_name}_{self.pipeline_name}_{timestamp}_{unique_id}"
    
    def _init_bigquery_client(self) -> Optional[bigquery.Client]:
        """
        Initialize BigQuery client with caching and fallback logic.
        
        Priority: cached instance > provided instance > default credentials.
        Uses class-level cache to share instance across TestKit instances.
        
        Returns:
            BigQuery client instance or None if initialization fails
        """
        # Use cached BigQuery client if available
        if TestKit._shared_bigquery_client is not None:
            return TestKit._shared_bigquery_client
            
        # First priority: Use provided BigQuery client
        if self._bigquery_client is not None:
            TestKit._shared_bigquery_client = self._bigquery_client
            print("Using provided BigQuery client instance")
            return self._bigquery_client
            
        try:
            # Initialize BigQuery client with default credentials
            # Will use Application Default Credentials (ADC) from environment
            bq_client = bigquery.Client(project=self._bigquery_project_id)
            print("BigQuery client initialized with default credentials")
            TestKit._shared_bigquery_client = bq_client
            return bq_client
            
        except Exception as e:
            print(f"Warning: Could not initialize BigQuery client: {e}")
            return None
    
    def _init_firestore_client(self) -> Optional[firestore.Client]:
        """
        Initialize Firestore client with caching and fallback project ID.
        
        Uses class-level cache to share client across TestKit instances.
        Falls back to default project ID if none provided.
        
        Returns:
            Firestore client instance or None if initialization fails
        """
        # Use cached Firestore client if available
        if TestKit._shared_firestore_client is not None:
            return TestKit._shared_firestore_client
            
        try:
            project_id = self._firestore_project_id
            print(f"Using Firestore project ID: {project_id}")
            firestore_client = firestore.Client(project=project_id)
            print(f"Firestore client initialized for project: {project_id}")
            
            # Cache the Firestore client for future use
            TestKit._shared_firestore_client = firestore_client
            return firestore_client
            
        except Exception as e:
            print(f"Warning: Could not initialize Firestore client: {e}")
            return None
    
    def _load_config_from_firestore(self) -> Dict[str, Any]:
        """
        Load repository-specific configuration from Firestore.
        
        Attempts to load config for this repository. Falls back to default config
        if repository config not found or Firestore unavailable.
        
        Returns:
            Configuration dictionary (repository-specific or default)
        """
        try:
            # Import ConfigManager here to avoid circular imports
            from ..utils.config_manager import ConfigManager
            
            # Initialize ConfigManager
            config_manager = ConfigManager(project_id=self._firestore_project_id)
            
            # Load repository-specific configuration (all at once)
            config = config_manager.get_repository_config(self.repository_name)
            
            if config:
                print(f"Loaded configuration for repository: {self.repository_name}")
                return config
            else:
                print(f"No configuration found for repository: {self.repository_name}. Using default configuration.")
                return config_manager.get_default_config()
                
        except Exception as e:
            print(f"Warning: Could not load config from Firestore: {e}")
            # Fallback to default config if Firestore fails
            try:
                from ..utils.config_manager import ConfigManager
                config_manager = ConfigManager(project_id=self._firestore_project_id)
                return config_manager.get_default_config()
            except Exception as fallback_exc:
                print(
                    "Warning: Could not load default config from ConfigManager: "
                    f"{fallback_exc}"
                )
                # Final fallback: return minimal config so testkit can proceed
                return {}
    
    def _get_default_bigquery_logging_config(self) -> Dict[str, str]:
        """Default BigQuery logging config when not provided via Firestore."""
        return {
            'project_id': self._bigquery_project_id,
            'dataset_id': self._default_dataset_id,
            'test_logs_table': self._default_test_logs_table
        }

    def _get_permission_resolver(self) -> Optional[PermissionResolver]:
        """
        Lazily initialize permission resolver used for recipient lookups.
        """
        if not self._permission_project_id:
            return None

        if self._permission_resolver is not None:
            return self._permission_resolver

        try:
            print(
                "Initializing PermissionResolver for project "
                f"{self._permission_project_id}"
            )
            self._permission_resolver = PermissionResolver(
                project_id=self._permission_project_id
            )
        except Exception as exc:  # pragma: no cover - defensive logging
            print(
                f"Warning: Could not initialize PermissionResolver for "
                f"project {self._permission_project_id}: {exc}"
            )
            self._permission_resolver = None
        return self._permission_resolver

    def _collect_issue_owner_permissions(self, issues: List[Dict[str, Any]]) -> Set[str]:
        """
        Collect unique issue_owner permission strings from issue metrics.
        """
        return self._collect_permissions_from_metrics(issues, 'issue_owner')

    def _collect_issue_ack_access_permissions(self, issues: List[Dict[str, Any]]) -> Set[str]:
        """
        Collect unique issue_ack_access permission strings from issue metrics.
        """
        return self._collect_permissions_from_metrics(issues, 'issue_ack_access')

    def _get_permission_based_recipients(
        self, issues: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Resolve issue_owner permissions to concrete email addresses.
        """
        permissions = set()
        permissions.update(self._collect_issue_owner_permissions(issues))
        permissions.update(self._collect_issue_ack_access_permissions(issues))
        if not permissions:
            return []

        resolver = self._get_permission_resolver()
        if not resolver:
            return []

        try:
            resolved = resolver.get_emails_for_permissions(list(permissions))
            if resolved:
                print(
                    "Resolved permission-based recipients: "
                    f"{', '.join(resolved)} (permissions: {permissions})"
                )
            else:
                print(
                    "No permission-based recipients resolved "
                    f"for permissions: {permissions}"
                )
            return resolved
        except Exception as exc:  # pragma: no cover - defensive logging
            print(f"Warning: Could not resolve permission recipients: {exc}")
            return []

    def _get_configured_recipients(self, alert_type: str) -> List[str]:
        """Return statically configured recipients for alert type."""
        email_alerts = self.config.get('email_alerts', {})
        if alert_type == 'failure':
            return email_alerts.get('failure_recipients', []) or []
        return email_alerts.get('warning_recipients', []) or []

    def _build_append_recipients(
        self, alert_type: str, issues: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Combine configured recipients with permission-based recipients.
        """
        recipients = []
        recipients.extend(self._get_configured_recipients(alert_type))
        recipients.extend(self._get_permission_based_recipients(issues))
        return self._dedupe_emails(recipients)

    @staticmethod
    def _dedupe_emails(recipients: List[str]) -> List[str]:
        """Deduplicate emails while preserving original casing/order."""
        if not recipients:
            return []

        deduped = []
        seen = set()
        for recipient in recipients:
            if not isinstance(recipient, str):
                continue
            email = recipient.strip()
            if not email:
                continue
            normalized = email.lower()
            if normalized in seen:
                continue
            seen.add(normalized)
            deduped.append(email)
        return deduped

    def _collect_permissions_from_metrics(
        self,
        issues: List[Dict[str, Any]],
        field_name: str,
    ) -> Set[str]:
        """Generic permission extractor used for issue_owner and issue_ack_access."""
        collected: Set[str] = set()
        if not issues:
            return collected

        for issue in issues:
            metrics = issue.get('metrics') or {}
            permissions = metrics.get(field_name)
            if not permissions:
                continue

            if isinstance(permissions, str):
                candidate = permissions.strip()
                if candidate:
                    collected.add(candidate)
            elif isinstance(permissions, (list, tuple, set)):
                for candidate in permissions:
                    if isinstance(candidate, str):
                        trimmed = candidate.strip()
                        if trimmed:
                            collected.add(trimmed)
        return collected
    
    def _log_run_start(self):
        """Log the start of a test run."""
        start_message = f"Test run started - Repository: {self.repository_name}, Pipeline: {self.pipeline_name}, Run ID: {self.run_id}"
        print(f"🚀 {start_message}")
    
    def log_pass(self, test_name: str, message: str = "", metrics: Dict[str, Any] = None):
        """
        Log a passing test result.
        
        Args:
            test_name: Name of the test that passed
            message: Optional message describing the test result
            metrics: Optional dictionary of metrics/measurements
        """
        result = {
            'run_id': self.run_id,
            'repository': self.repository_name,
            'pipeline': self.pipeline_name,
            'test_name': test_name,
            'status': 'PASS',
            'message': message,
            'metrics': metrics or {},
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        self.test_results.append(result)
        # self._log_to_sheet(result) # logging all the passed tests clutters the logs
        print(f"✅ PASS: {test_name} - {message}")
    
    def log_warn(
        self, 
        test_name: str, 
        issue_identifier: str,
        message: str, 
        metrics: Dict[str, Any] = None, 
        acknowledgeable: bool = True,
    ):
        """
        Log a warning test result.
        
        Warnings don't stop pipeline execution but trigger email digests. Can be
        acknowledged to prevent email spam. Metrics are stored in Firestore for
        the Analytics Hub web interface.
        
        Args:
            test_name: Name of the test (e.g., 'check_consistent_daily_hours_per_person')
            issue_identifier: Unique identifier for the issue (e.g., 'john.doe@locaria.com').
                Use stable identifiers like email or ID, not timestamps.
            message: Warning message describing the issue (supports HTML for email formatting)
            metrics: Dictionary of metrics/measurements. Should include:
                - 'issue_owner': Union[str, List[str]] (permission(s) required to acknowledge)
                - 'issue_details': str (detailed description for Analytics Hub)
                - Any pipeline-specific fields (email, person_name, percentages, etc.)
            acknowledgeable: If True, this warning can be acknowledged and muted
        
        Example:
            >>> testkit.log_warn(
            ...     'check_hours',
            ...     'john.doe@locaria.com',
            ...     'Expected 35h/week, found 28h/week',
            ...     metrics={
            ...         'issue_owner': 'analytics_hub.data_team_ack',
            ...         'issue_details': 'John Doe has inconsistent weekly hours',
            ...         'email': 'john.doe@locaria.com',
            ...         'expected_hours': 35,
            ...         'actual_hours': 28
            ...     }
            ... )
        """
        metrics = self._ensure_issue_ack_access(metrics)

        result = {
            'run_id': self.run_id,
            'repository': self.repository_name,
            'pipeline': self.pipeline_name,
            'test_name': test_name,
            'issue_identifier': issue_identifier,
            'status': 'WARN',
            'message': message,
            'metrics': metrics or {},
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'acknowledgeable': acknowledgeable
        }
        
        self.warnings.append(result)
        self.test_results.append(result)
        
        print(f"⚠️  WARN: {test_name} - {message}")
    
    def log_fail(
        self, 
        test_name: str, 
        issue_identifier: str,
        message: str, 
        metrics: Dict[str, Any] = None, 
        stop_pipeline: bool = None, 
        acknowledgeable: bool = True
    ):
        """
        Log a failing test result and trigger alerts.
        
        Failures trigger immediate email notifications (unless acknowledged). Can optionally
        stop pipeline execution. Metrics are stored in Firestore for the Analytics Hub.
        
        Args:
            test_name: Name of the test that failed (e.g., 'check_data_completeness')
            issue_identifier: Unique identifier for the issue (e.g., 'plunet_employee_table').
                Use stable identifiers, not timestamps.
            message: Failure message describing the issue (supports HTML for email formatting)
            metrics: Dictionary of metrics/measurements. Should include:
                - 'issue_owner': Union[str, List[str]] (permission(s) required to acknowledge)
                - 'issue_details': str (detailed description for Analytics Hub)
                - Any pipeline-specific fields
            stop_pipeline: If True, send email and stop pipeline. If False, send email and continue.
                          If None, uses the fail_on_error setting from TestKit initialization.
            acknowledgeable: If True, this failure can be acknowledged and muted
            
        Raises:
            TestFailureException: If stop_pipeline is True, raises exception to stop pipeline
            
        Example:
            >>> testkit.log_fail(
            ...     'check_data_completeness',
            ...     'plunet_employee_table',
            ...     'Data completeness 85% below threshold 95%',
            ...     metrics={
            ...         'issue_owner': 'analytics_hub.data_team_ack',
            ...         'issue_details': 'Plunet employee table has low completeness',
            ...         'completeness': 0.85,
            ...         'threshold': 0.95,
            ...         'null_cells': 150
            ...     },
            ...     stop_pipeline=False  # Continue pipeline, just alert
            ... )
        """
        # Determine if we should stop the pipeline
        should_stop = stop_pipeline if stop_pipeline is not None else self.fail_on_error
        
        metrics = self._ensure_issue_ack_access(metrics)

        result = {
            'run_id': self.run_id,
            'repository': self.repository_name,
            'pipeline': self.pipeline_name,
            'test_name': test_name,
            'issue_identifier': issue_identifier,
            'status': 'FAIL',
            'message': message,
            'metrics': metrics or {},
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'acknowledgeable': acknowledgeable
        }
        
        self.failures.append(result)
        self.test_results.append(result)
        
        print(f"❌ FAIL: {test_name} - {message}")
        
        # If stop_pipeline=True, send summary email with all failures and stop
        if should_stop:
            self._send_failure_summary_email()
            raise TestFailureException(f"Pipeline stopped due to test failure: {test_name} - {message}")
           
    def _write_test_results_to_bigquery(self):
        """
        Write consolidated test run summary to BigQuery table.
        
        Writes a single summary row per pipeline execution with aggregated statistics
        instead of individual test results, reducing BigQuery storage and improving query performance.
        """
        if not self.bigquery_client:
            return
        
        try:
            # Read BigQuery logging configuration
            logging_project_id = self.bigquery_logging_config.get('project_id', self._bigquery_project_id)
            dataset_id = self.bigquery_logging_config.get('dataset_id', self._default_dataset_id)
            table_name = self.bigquery_logging_config.get('test_logs_table', self._default_test_logs_table)
            table_ref = f"{logging_project_id}.{dataset_id}.{table_name}"
            
            # Calculate summary statistics
            total_tests = len(self.test_results)
            passed = len([r for r in self.test_results if r['status'] == 'PASS'])
            warnings = len(self.warnings)
            failures = len(self.failures)
            
            # Group test results by test_name for detailed breakdown
            tests_by_name = {}
            for result in self.test_results:
                test_name = result.get('test_name', 'unknown')
                if test_name not in tests_by_name:
                    tests_by_name[test_name] = {'passed': 0, 'warnings': 0, 'failures': 0}
                status = result.get('status', '')
                if status == 'PASS':
                    tests_by_name[test_name]['passed'] += 1
                elif status == 'WARN':
                    tests_by_name[test_name]['warnings'] += 1
                elif status == 'FAIL':
                    tests_by_name[test_name]['failures'] += 1
            
            # Prepare consolidated summary row
            summary_metrics = {
                'total_tests': total_tests,
                'passed': passed,
                'warnings': warnings,
                'failures': failures,
                'run_duration': self._get_run_duration(),
                'tests_by_name': tests_by_name
            }
            
            # Get first test result for common fields (all should have same run_id, repository, pipeline)
            first_result = self.test_results[0] if self.test_results else {}
            
            row = {
                'run_id': first_result.get('run_id', self.run_id),
                'repository': first_result.get('repository', self.repository_name),
                'pipeline': first_result.get('pipeline', self.pipeline_name),
                'test_name': 'pipeline_summary',  # Special value indicating this is a summary row
                'issue_identifier': None,  # No specific issue for summary
                'status': 'SUMMARY',  # Special status for summary rows
                'message': f"Pipeline execution summary: {passed} passed, {warnings} warnings, {failures} failures",
                'metrics': json.dumps(summary_metrics),
                'timestamp': first_result.get('timestamp', datetime.now(timezone.utc).isoformat()),
                'acknowledgeable': False,  # Summaries are not acknowledgeable
                'log_timestamp': datetime.now(timezone.utc).isoformat()
            }
            
            # Convert to DataFrame (single row)
            df = pd.DataFrame([row])
            
            # Define schema
            schema = [
                bigquery.SchemaField("run_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("repository", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("pipeline", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("test_name", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("issue_identifier", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("status", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("message", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("metrics", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("timestamp", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("acknowledgeable", "BOOLEAN", mode="REQUIRED"),
                bigquery.SchemaField("log_timestamp", "STRING", mode="REQUIRED"),
            ]
            
            # Ensure dataset exists (create if it doesn't)
            dataset_ref = self.bigquery_client.dataset(dataset_id, project=logging_project_id)
            try:
                self.bigquery_client.get_dataset(dataset_ref)
                print(f"[INFO] BigQuery dataset {logging_project_id}.{dataset_id} already exists")
            except NotFound:
                print(f"[INFO] BigQuery dataset {logging_project_id}.{dataset_id} does not exist. Creating it...")
                dataset = bigquery.Dataset(dataset_ref)
                dataset.location = "US"  # Set dataset location
                dataset.description = "Cross-project logging for integrated test results"
                self.bigquery_client.create_dataset(dataset, exists_ok=True)
                print(f"[INFO] BigQuery dataset {logging_project_id}.{dataset_id} created successfully")
            
            # Ensure table exists (create if it doesn't)
            try:
                self.bigquery_client.get_table(table_ref)
                print(f"[INFO] BigQuery table {table_ref} already exists")
            except NotFound:
                print(f"[INFO] BigQuery table {table_ref} does not exist. Creating it...")
                table = bigquery.Table(table_ref, schema=schema)
                self.bigquery_client.create_table(table)
                print(f"[INFO] BigQuery table {table_ref} created successfully")
            
            # Replace NaN values with None for proper BigQuery handling
            df = df.where(pd.notnull(df), None)
            
            # Write DataFrame to BigQuery (append mode)
            job_config = bigquery.LoadJobConfig(
                schema=schema,
                write_disposition=bigquery.WriteDisposition.WRITE_APPEND
            )
            
            # Use load_table_from_dataframe for better compatibility
            job = self.bigquery_client.load_table_from_dataframe(df, table_ref, job_config=job_config)
            job.result()  # Wait for job to complete
            
            print(f"✅ Successfully wrote pipeline execution summary to BigQuery: {table_ref} (Total: {total_tests} tests, {passed} passed, {warnings} warnings, {failures} failures)")
            
        except Exception as e:
            print(f"Warning: Could not write test results to BigQuery: {e}")
            import traceback
            print(f"Full traceback: {traceback.format_exc()}")
    
    def _send_failure_summary_email(self):
        """
        Send failure summary email, excluding acknowledged issues to prevent spam.
        
        Only sends if there are new (unacknowledged) failures. Includes context about
        muted issues for transparency. Uses config-based email API URL with env fallback.
        """
        if not self.failures or self.failure_emails_sent:
            return
        
        # Filter out acknowledged issues to prevent email spam
        filtered_results = self.acknowledge_manager.filter_acknowledged_issues(self.failures)
        
        if not filtered_results['new_issues']:
            print("📧 All failure issues are acknowledged and muted - skipping email")
            return
            
        try:
            # Try config first, then environment variable fallback
            email_api_url = self.config.get('api_config', {}).get('email_api_url')
            if not email_api_url:
                email_api_url = os.getenv('EMAIL_API_URL')
                
            if not email_api_url:
                return
                
            # Build email content: new issues first, then acknowledged context
            failure_summary = []
            
            # Section 1: New issues that need attention
            if filtered_results['new_issues']:
                failure_summary.append("🚨 NEW ISSUES DETECTED:")
                for i, failure in enumerate(filtered_results['new_issues'], 1):
                    failure_summary.append(f"{i}. {failure['test_name']}<br/>   Message: {failure['message']}<br/>   Time: {failure['timestamp']}")
            
            # Section 2: Acknowledged issues (for context, but muted)
            if filtered_results['acknowledged_issues']:
                if failure_summary:
                    failure_summary.append("")  # Spacing between sections
                failure_summary.append("✅ PREVIOUSLY ACKNOWLEDGED (muted):")
                for i, failure in enumerate(filtered_results['acknowledged_issues'], 1):
                    metrics = failure.get('metrics', {})
                    # Support multiple field name variations for backward compatibility
                    person_name = metrics.get('person_name') or metrics.get('issue_name', 'Unknown')
                    person_email = metrics.get('person_email') or metrics.get('issue_identifier', 'Unknown')
                    failure_summary.append(f"{i}. {failure['test_name']} - {person_name} ({person_email}) - Acknowledged and muted")
            
            failure_summary_text = "<br/><br/>".join(failure_summary)
            
            payload = {
                "task_name": self.config.get('api_config', {}).get('email_template_failure', 'Test Failure Alert'),
                "custom_variables": {
                    "repository_name": self.repository_name,
                    "pipeline_name": self.pipeline_name,
                    "run_id": self.run_id,
                    "failure_count": len(filtered_results['new_issues']),
                    "failure_summary": failure_summary_text,
                    "run_duration": self._get_run_duration(),
                    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
                }
            }

            append_recipients = self._build_append_recipients(
                alert_type='failure',
                issues=filtered_results['new_issues'],
            )
            if append_recipients:
                payload["append_recipients"] = append_recipients
            
            response = requests.post(email_api_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"📧 Failure summary email sent successfully")
                    self.failure_emails_sent = True
                else:
                    print(f"Warning: Failure summary email failed: {result.get('message')}")
            else:
                print(f"Warning: Failure summary email failed with status {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"Warning: Could not send failure summary email: {e}")
    
    def send_warning_digest(self):
        """Send digest of all warnings at the end of a run, filtered by acknowledgment status."""
        if not self.warnings:
            return
        
        # Filter warnings into new vs acknowledged issues
        filtered_results = self.acknowledge_manager.filter_acknowledged_issues(self.warnings)
        
        if not filtered_results['new_issues']:
            print("📧 All warning issues are acknowledged and muted - skipping email")
            return
        
        try:
            # Get email API URL from centralized config
            email_api_url = self.config.get('api_config', {}).get('email_api_url')
            
            if not email_api_url:
                # Fallback to environment variable
                email_api_url = os.getenv('EMAIL_API_URL')
                
            if not email_api_url:
                return
                
            # Prepare warning digest with acknowledgment context
            warning_summary = []
            
            # Add new issues
            if filtered_results['new_issues']:
                warning_summary.append("⚠️ NEW WARNINGS DETECTED:")
                for i, warning in enumerate(filtered_results['new_issues'], 1):
                    warning_summary.append(f"{i}. {warning['test_name']}<br/>   Message: {warning['message']}<br/>   Time: {warning['timestamp']}")
            
            # Add acknowledged issues context
            if filtered_results['acknowledged_issues']:
                if warning_summary:
                    warning_summary.append("")  # Add spacing
                warning_summary.append("✅ PREVIOUSLY ACKNOWLEDGED (muted):")
                for i, warning in enumerate(filtered_results['acknowledged_issues'], 1):
                    metrics = warning.get('metrics', {})
                    # Try multiple field names for backward compatibility
                    person_name = metrics.get('person_name') or metrics.get('issue_name', 'Unknown')
                    person_email = metrics.get('person_email') or metrics.get('issue_identifier', 'Unknown')
                    warning_summary.append(f"{i}. {warning['test_name']} - {person_name} ({person_email}) - Acknowledged and muted")
            
            warning_summary_text = "<br/><br/>".join(warning_summary)
            
            payload = {
                "task_name": self.config.get('api_config', {}).get('email_template_warning', 'Test Warning Digest'),
                "custom_variables": {
                    "repository_name": self.repository_name,
                    "pipeline_name": self.pipeline_name,
                    "run_id": self.run_id,
                    "warning_count": len(filtered_results['new_issues']),
                    "warning_summary": warning_summary_text,
                    "run_duration": self._get_run_duration(),
                    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
                }
            }

            append_recipients = self._build_append_recipients(
                alert_type='warning',
                issues=filtered_results['new_issues'],
            )
            if append_recipients:
                payload["append_recipients"] = append_recipients
            
            response = requests.post(email_api_url, json=payload, timeout=30)
            if response.status_code == 200:
                print(f"Warning digest sent successfully for {len(self.warnings)} warnings")
            else:
                print(f"Warning: Warning digest failed with status {response.status_code}")
                
        except Exception as e:
            print(f"Warning: Could not send warning digest: {e}")
    
    def _get_run_duration(self) -> str:
        """Get the duration of the test run."""
        duration = datetime.now(timezone.utc) - self.start_time
        return str(duration).split('.')[0]  # Remove microseconds
    
    def get_threshold(self, path: str, default_value: Any = None) -> Any:
        """
        Retrieve threshold value from config using dot-notation path.
        
        Supports both global and pipeline-specific thresholds:
        - Global: 'global.row_count_change.warn_percentage'
        - Pipeline-specific: 'test_name.threshold_name' (auto-prefixed with pipeline name)
        
        Args:
            path: Dot-notation path to threshold value
            default_value: Returned if path not found
            
        Returns:
            Threshold value or default_value
        """
        try:
            # Determine if this is a global or pipeline-specific threshold
            if path.startswith('global.'):
                full_path = f"thresholds.{path}"
            else:
                # Pipeline-specific: prefix with pipeline name
                full_path = f"thresholds.{self.pipeline_name}.{path}"
            
            # Navigate nested dict structure using dot-notation
            current = self.config
            for key in full_path.split('.'):
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    self._log_missing_threshold(full_path, default_value)
                    return default_value
            
            return current
            
        except Exception as e:
            print(f"Error getting threshold for {self.pipeline_name}.{path}: {e}")
            return default_value

    def _ensure_issue_ack_access(self, metrics: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Ensure every metrics payload carries issue_ack_access for downstream consumers.
        """
        normalized = metrics.copy() if metrics else {}
        if 'issue_ack_access' not in normalized and 'issue_owner' in normalized:
            normalized['issue_ack_access'] = normalized['issue_owner']
        return normalized
    
    def set_threshold(self, path: str, value: Any) -> bool:
        """
        Set a threshold value using dot notation path.
        
        Args:
            path: Dot notation path to threshold. Can be:
                  - Pipeline-specific: 'test_name.threshold_name' (e.g., 'check_employee_data_completeness.completeness_threshold')
                  - Global: 'global.category.threshold_name' (e.g., 'global.row_count_change.warn_percentage')
            value: New threshold value
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Handle global thresholds
            if path.startswith('global.'):
                full_path = f"thresholds.{path}"
            else:
                # Pipeline-specific thresholds
                full_path = f"thresholds.{self.pipeline_name}.{path}"
            
            # Navigate to the parent of the target key and set the value
            keys = full_path.split('.')
            current = self.config
            
            # Navigate to the parent container
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            # Set the final value
            current[keys[-1]] = value
            
            # Update in Firestore if available
            if self.firestore_client:
                from ..utils.config_manager import ConfigManager
                config_manager = ConfigManager(project_id=self._firestore_project_id)
                return config_manager.set_threshold(self.repository_name, full_path, value)
            
            return True
            
        except Exception as e:
            print(f"Error setting threshold for {self.pipeline_name}.{path}: {e}")
            return False

    def _log_missing_threshold(self, full_path: str, default_value: Any) -> None:
        """Surface helpful debugging info when a threshold path is missing."""
        try:
            thresholds = self.config.get('thresholds', {}) if isinstance(self.config, dict) else {}
            pipeline_thresholds = thresholds.get(self.pipeline_name, {})
            global_thresholds = thresholds.get('global', {})
            print(
                "[TestKit] Missing threshold path '{path}' for repo '{repo}' "
                "pipeline '{pipeline}'. Returning default: {default_value}".format(
                    path=full_path,
                    repo=self.repository_name,
                    pipeline=self.pipeline_name,
                    default_value=default_value,
                )
            )
            print(
                "[TestKit] Available pipeline thresholds keys: "
                f"{list(pipeline_thresholds.keys())}"
            )
            print(
                "[TestKit] Available global thresholds keys: "
                f"{list(global_thresholds.keys())}"
            )
        except Exception as log_exc:
            print(f"[TestKit] Failed to log missing threshold details: {log_exc}")
    
    def is_test_enabled(self, test_category: str) -> bool:
        """
        Check if a test category is enabled.
        
        Args:
            test_category: Test category to check (e.g., 'enable_schema_validation')
            
        Returns:
            True if test is enabled, False otherwise
        """
        try:
            return self.config.get('test_switches', {}).get(test_category, True)
        except Exception:
            return True
    
    def update_config_in_firestore(self, config_updates: Dict[str, Any]) -> bool:
        """Update configuration in Firestore for this repository."""
        if not self.firestore_client:
            print("Warning: Firestore client not available. Cannot update configuration.")
            return False
        
        try:
            repo_doc_ref = self.firestore_client.collection(self.collection_integrated_testing_config).document(self.repository_name)
            
            # Add metadata
            config_updates['last_updated'] = datetime.now(timezone.utc)
            config_updates['updated_by'] = os.getenv('USER', 'unknown')
            
            # Update the document
            repo_doc_ref.set(config_updates, merge=True)
            print(f"Configuration updated for repository: {self.repository_name}")
            
            # Reload configuration
            self.config = self._load_config_from_firestore()
            return True
            
        except Exception as e:
            print(f"Error updating configuration in Firestore: {e}")
            return False
    
    def _batch_update_acknowledgments(self):
        """
        Batch-update Firestore with all acknowledgeable issues to minimize API calls.
        
        Groups issues by test_name and performs one batch write per test instead of
        one write per issue. Processes both warnings and failures, preserving their
        status and metadata for the acknowledgment system.
        """
        # Group issues by test_name for efficient batch processing
        issues_by_test: Dict[str, List[Dict[str, Any]]] = {}
        
        # Process warnings: extract issue data and group by test
        for result in self.warnings:
            if not result.get('acknowledgeable', True):
                continue
            
            issue_identifier = result.get('issue_identifier')
            test_name = result.get('test_name')
            
            if not issue_identifier or not test_name:
                continue
            
            metrics = result.get('metrics', {}) or {}
            # Prefer explicit issue_details from metrics; fall back to message
            issue_details = metrics.get('issue_details', result.get('message', ""))
            additional_metadata = metrics.copy()
            # Include status so acknowledgment system knows this is a warning
            additional_metadata['status'] = result.get('status', 'WARN')
            
            issues_by_test.setdefault(test_name, []).append({
                "issue_identifier": issue_identifier,
                "issue_details": issue_details,
                "additional_metadata": additional_metadata,
            })
        
        # Process failures: same logic as warnings but with FAIL status
        for result in self.failures:
            if not result.get('acknowledgeable', True):
                continue
            
            issue_identifier = result.get('issue_identifier')
            test_name = result.get('test_name')
            
            if not issue_identifier or not test_name:
                continue
            
            metrics = result.get('metrics', {}) or {}
            issue_details = metrics.get('issue_details', result.get('message', ""))
            additional_metadata = metrics.copy()
            additional_metadata['status'] = result.get('status', 'FAIL')
            
            issues_by_test.setdefault(test_name, []).append({
                "issue_identifier": issue_identifier,
                "issue_details": issue_details,
                "additional_metadata": additional_metadata,
            })
        
        # Batch write all issues per test to Firestore
        for test_name, issues in issues_by_test.items():
            try:
                success = self.acknowledge_manager.batch_update_issue_detections(
                    test_name=test_name,
                    issues=issues,
                )
                if not success:
                    print(f"[WARNING] Failed to write {len(issues)} issues to Firestore for test '{test_name}'")
            except Exception as e:
                print(f"Warning: Could not batch update acknowledgment entries for test {test_name}: {e}")
                import traceback
                traceback.print_exc()
    
    def finalize_run(self):
        """
        Finalize test run: batch-update acknowledgments, send emails, log summary.
        
        Idempotent - safe to call multiple times (e.g., in finally blocks).
        Prevents duplicate emails and logs by checking finalized flag.
        
        Execution order:
        1. Batch-update Firestore with all acknowledgeable issues
        2. Send failure email (if new unacknowledged failures exist)
        3. Send warning digest (if new unacknowledged warnings exist)
        4. Log summary to sheet and console
        
        Returns:
            Dict with test summary:
                {
                    'total_tests': int,
                    'passed': int,
                    'warnings': int,
                    'failures': int,
                    'run_duration': str
                }
            
        Example:
            >>> try:
            ...     # Run tests...
            ...     testkit.log_warn('test1', 'issue1', 'Warning message')
            ...     testkit.log_pass('test2', 'All good')
            ... finally:
            ...     summary = testkit.finalize_run()
            ...     # Returns: {
            ...     #     'total_tests': 2,
            ...     #     'passed': 1,
            ...     #     'warnings': 1,
            ...     #     'failures': 0,
            ...     #     'run_duration': '0:05:23'
            ...     # }
        """
        # Early return if already finalized to prevent duplicate emails/logs
        if self.finalized:
            print("Test run already finalized - skipping duplicate finalization")
            summary = {
                'total_tests': len(self.test_results),
                'passed': len([r for r in self.test_results if r['status'] == 'PASS']),
                'warnings': len(self.warnings),
                'failures': len(self.failures),
                'run_duration': self._get_run_duration()
            }
            return summary
        
        try:
            # Step 1: Batch-write all test results to BigQuery
            self._write_test_results_to_bigquery()
            
            # Step 2: Batch-update Firestore with all acknowledgeable issues
            # This must happen before email filtering so acknowledgment status is current
            try:
                self._batch_update_acknowledgments()
            except Exception as e:
                print(f"Warning: Could not batch update acknowledgment entries: {e}")
            
            # Step 3: Send failure email (only if new unacknowledged failures exist)
            self._send_failure_summary_email()
                       
            # Step 4: Send warning digest (only if new unacknowledged warnings exist)
            self.send_warning_digest()
            
            # Step 5: Calculate and log summary statistics
            summary = {
                'total_tests': len(self.test_results),
                'passed': len([r for r in self.test_results if r['status'] == 'PASS']),
                'warnings': len(self.warnings),
                'failures': len(self.failures),
                'run_duration': self._get_run_duration()
            }
            
            print(f"🏁 Test run completed: {summary}")
            
            # Mark as finalized to prevent duplicate execution
            self.finalized = True
            
            # Return summary for programmatic use
            return summary
            
        except Exception as e:
            print(f"Error finalizing test run: {e}")
            # Don't mark as finalized if there was an error, so it can be retried
            return None


# Convenience functions for easy import
def create_testkit(repository_name: str, pipeline_name: str = None, fail_on_error: bool = False, 
                   firestore_project_id: str = None, bigquery_client = None) -> TestKit:
    """Create a new TestKit instance."""
    return TestKit(repository_name, pipeline_name, fail_on_error, 
                   firestore_project_id=firestore_project_id, bigquery_client=bigquery_client)


def log_pass(testkit: TestKit, test_name: str, message: str = "", metrics: Dict[str, Any] = None):
    """Log a passing test."""
    testkit.log_pass(test_name, message, metrics)


def log_warn(testkit: TestKit, test_name: str, issue_identifier: str, message: str, metrics: Dict[str, Any] = None, acknowledgeable: bool = True):
    """Log a warning."""
    testkit.log_warn(test_name, issue_identifier, message, metrics, acknowledgeable)


def log_fail(testkit: TestKit, test_name: str, issue_identifier: str, message: str, metrics: Dict[str, Any] = None, stop_pipeline: bool = None, acknowledgeable: bool = True):
    """Log a failure."""
    testkit.log_fail(test_name, issue_identifier, message, metrics, stop_pipeline, acknowledgeable)
