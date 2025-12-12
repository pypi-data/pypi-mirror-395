"""
ConfigManager - Firestore-based configuration management for testing framework.

Manages repository-specific test configurations including thresholds, test switches,
email settings, and logging preferences. Provides CRUD operations and validation
for configuration data stored in Firestore.

Firestore Structure:
  Collection: integrated_testing_config
  └── Document: {repository_name}  # e.g., 'locate_2_pulls'
      ├── thresholds: Dict[str, Any]
      │   ├── global: Dict  # Global thresholds (e.g., row_count_change, data_freshness)
      │   └── {pipeline_name}: Dict  # Pipeline-specific thresholds
      ├── test_switches: Dict[str, bool]  # Feature flags
      ├── email_alerts: Dict  # Email configuration
      ├── logging: Dict  # Logging preferences
      ├── api_config: Dict  # API endpoints and templates
      └── created_at / last_updated: timestamp

Example Document:
  integrated_testing_config/locate_2_pulls
  {
    "thresholds": {
      "global": {
        "row_count_change": {"warn_percentage": 20, "fail_percentage": 50},
        "data_freshness": {"max_age_hours": 24, "warn_age_hours": 12}
      },
      "plunet_employee_table": {
        "check_data_completeness": {"completeness_threshold": 0.95}
      }
    },
    "test_switches": {
      "enable_business_logic_checks": true,
      "enable_freshness_checks": true
    }
  }
"""

import os
import copy
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from google.cloud import firestore

## Why defining those constants at module level?
## Those constants define behavior for everything that imports ConfigManager (including TestKit), 
## so keeping them module-level makes them available even before an instance is created 
## (e.g., when TestKit pulls defaults). Moving them inside __init__ would require every consumer to instantiate ConfigManager 
## just to read defaults, and you’d have to thread those values through multiple call sites. 
## Leaving them at module scope keeps a single authoritative set used both by ConfigManager and other modules 
## (like TestKit) without extra object creation.
DEFAULT_FIRESTORE_PROJECT_ID = "locaria-dev-config-store"
DEFAULT_BIGQUERY_PROJECT_ID = "locaria-dev-config-store"
DEFAULT_FIRESTORE_COLLECTION_NAME = "integrated_testing_config"
DEFAULT_FIRESTORE_GLOBAL_CONFIG_DOC = "global_testing_config"
DEFAULT_REPOSITORY_MAP_DOC = "repositories"
DEFAULT_BIGQUERY_DATASET_ID = "cross_project_logging"
DEFAULT_BIGQUERY_TEST_LOGS_TABLE = "integrated_test_logs"
DEFAULT_PERMISSION_RESOLVER_PROJECT_ID = "locaria-prod-authenticator"

class ConfigManager:
    """
    Manages repository-specific test configurations in Firestore.
    
    Handles creation, updates, retrieval, and validation of test configurations.
    Supports dot-notation paths for nested threshold access. Provides default
    configuration templates for new repositories.
    """
    
    def __init__(self, project_id: str = None):
        """
        Initialize the configuration manager.
        
        Args:
            project_id: GCP project ID for Firestore. If None, will use fallback project ID.
        """
        # Use provided project_id or fallback
        if project_id is None:
            project_id = DEFAULT_FIRESTORE_PROJECT_ID
            print(f"Warning: No firestore_project_id provided. Using fallback project ID: {project_id}")
        else:
            print(f"Using provided Firestore project ID: {project_id}")
        
        self.project_id = project_id
        self.firestore_client = firestore.Client(project=self.project_id)
        self.collection_name = DEFAULT_FIRESTORE_COLLECTION_NAME
        self.global_config_doc = DEFAULT_FIRESTORE_GLOBAL_CONFIG_DOC
    
    def create_repository_config(self, repository_name: str, config: Dict[str, Any]) -> bool:
        """
        Create a new repository configuration.
        
        Args:
            repository_name: Name of the repository
            config: Configuration dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Add metadata
            config['created_at'] = datetime.now(timezone.utc)
            config['created_by'] = os.getenv('USER', 'unknown')
            config['last_updated'] = datetime.now(timezone.utc)
            config['updated_by'] = os.getenv('USER', 'unknown')
            
            # Create the document
            doc_ref = self.firestore_client.collection(self.collection_name).document(repository_name)
            doc_ref.set(config)
            
            print(f"Created configuration for repository: {repository_name}")
            return True
            
        except Exception as e:
            print(f"Error creating configuration for {repository_name}: {e}")
            return False
    
    def update_repository_config(self, repository_name: str, config_updates: Dict[str, Any]) -> bool:
        """
        Update an existing repository configuration.
        
        Args:
            repository_name: Name of the repository
            config_updates: Dictionary of configuration updates
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Add metadata
            config_updates['last_updated'] = datetime.now(timezone.utc)
            config_updates['updated_by'] = os.getenv('USER', 'unknown')
            
            # Update the document
            doc_ref = self.firestore_client.collection(self.collection_name).document(repository_name)
            doc_ref.set(config_updates, merge=True)
            
            print(f"Updated configuration for repository: {repository_name}")
            return True
            
        except Exception as e:
            print(f"Error updating configuration for {repository_name}: {e}")
            return False
    
    def get_repository_config(self, repository_name: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for a specific repository.
        
        Args:
            repository_name: Name of the repository (e.g., 'locate_2_pulls')
            
        Returns:
            Configuration dictionary with thresholds, test_switches, etc., or None if not found
            
        Example:
            >>> config = manager.get_repository_config('locate_2_pulls')
            >>> # Returns: {
            >>> #     'thresholds': {...},
            >>> #     'test_switches': {...},
            >>> #     'email_alerts': {...}
            >>> # }
        """
        try:
            global_config = self._get_global_config()
            repository_overrides = self._get_repository_overrides(repository_name)
            if repository_overrides:
                base_config = copy.deepcopy(global_config)
                merged_config = self._deep_merge_dicts(base_config, repository_overrides)
                return merged_config
            
            # Fallback to legacy per-repository document support
            repo_config = self._get_repository_doc(repository_name)
            if repo_config:
                base_config = copy.deepcopy(global_config)
                merged_config = self._deep_merge_dicts(base_config, repo_config)
                return merged_config
            
            print(f"No configuration overrides found for repository: {repository_name}. Using global configuration.")
            return copy.deepcopy(global_config)
                
        except Exception as e:
            print(f"Error getting configuration for {repository_name}: {e}")
            return None
    
    def get_all_repository_configs(self) -> Dict[str, Any]:
        """
        Get all repository configurations.
        
        Returns:
            Dictionary mapping repository names to their configurations
        """
        try:
            configs = {}
            global_config = self._get_global_config()
            repository_map = self._get_repository_map()
            
            for repo_name, overrides in repository_map.items():
                configs[repo_name] = self._deep_merge_dicts(copy.deepcopy(global_config), overrides)
            
            # Include legacy standalone documents that may still exist
            docs = self.firestore_client.collection(self.collection_name).stream()
            for doc in docs:
                if doc.id in (self.global_config_doc, DEFAULT_REPOSITORY_MAP_DOC):
                    continue
                if doc.id in configs:
                    continue
                repo_config = doc.to_dict()
                configs[doc.id] = self._deep_merge_dicts(copy.deepcopy(global_config), repo_config)
            
            print(f"Retrieved configurations for {len(configs)} repositories")
            return configs
            
        except Exception as e:
            print(f"Error getting all repository configurations: {e}")
            return {}
    
    def delete_repository_config(self, repository_name: str) -> bool:
        """
        Delete configuration for a specific repository.
        
        Args:
            repository_name: Name of the repository
            
        Returns:
            True if successful, False otherwise
        """
        try:
            doc_ref = self.firestore_client.collection(self.collection_name).document(repository_name)
            doc_ref.delete()
            
            print(f"Deleted configuration for repository: {repository_name}")
            return True
            
        except Exception as e:
            print(f"Error deleting configuration for {repository_name}: {e}")
            return False
    
    def update_thresholds(self, repository_name: str, category: str, thresholds: Dict[str, Any]) -> bool:
        """
        Update thresholds for a specific category.
        
        Args:
            repository_name: Name of the repository
            category: Threshold category (e.g., 'row_count_change')
            thresholds: Dictionary of threshold updates
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get current repository configuration (raw document)
            current_config = self._get_repository_doc(repository_name)
            if not current_config:
                current_config = {}
            
            # Update thresholds
            if 'thresholds' not in current_config:
                current_config['thresholds'] = {}
            
            if category not in current_config['thresholds']:
                current_config['thresholds'][category] = {}
            
            current_config['thresholds'][category].update(thresholds)
            
            # Save updated configuration
            return self.update_repository_config(repository_name, current_config)
            
        except Exception as e:
            print(f"Error updating thresholds for {repository_name}: {e}")
            return False
    
    def update_test_switches(self, repository_name: str, switches: Dict[str, bool]) -> bool:
        """
        Update test switches for a repository.
        
        Args:
            repository_name: Name of the repository
            switches: Dictionary of test switch updates
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get current configuration
            current_config = self._get_repository_doc(repository_name)
            if not current_config:
                current_config = {}
            
            # Update test switches
            if 'test_switches' not in current_config:
                current_config['test_switches'] = {}
            
            current_config['test_switches'].update(switches)
            
            # Save updated configuration
            return self.update_repository_config(repository_name, current_config)
            
        except Exception as e:
            print(f"Error updating test switches for {repository_name}: {e}")
            return False
    
    ### THIS METHOD IS ONLY KICKING IN IF FIRESTORE CONFIG IS NOT FOUND FOR THE REPOSITORY
    ### Which is unlikely to happen, but just in case.
    def get_default_config(self) -> Dict[str, Any]:
        """
        Get the default configuration template.
        
        Returns:
            Default configuration dictionary
        """
        return {
            'thresholds': {
                'row_count_change': {
                    'warn_percentage': 20,
                    'fail_percentage': 50
                },
                'out_of_office_percentage': {
                    'warn_threshold': 25,
                    'fail_threshold': 35
                },
                'time_split_tolerance': {
                    'precision': 0.01
                },
                'data_freshness': {
                    'max_age_hours': 48,  # 2 days
                    'warn_age_hours': 24  # 1 day
                },
                'financial_data': {
                    'variance_threshold': 0.15,
                    'min_amount_threshold': 0.01
                },
                'api_response': {
                    'max_response_time_seconds': 30,
                    'min_success_rate': 0.95
                },
                'data_quality': {
                    'min_completeness_percentage': 95.0,
                    'max_null_percentage': 5.0,
                    'max_duplicate_percentage': 1.0
                },
                'numeric_ranges': {
                    'default_tolerance': 0.01
                }
            },
            'test_switches': {
                'enable_schema_validation': True,
                'enable_business_logic_checks': True,
                'enable_freshness_checks': True,
                'enable_row_count_validation': True,
                'enable_api_health_checks': True,
                'enable_data_quality_checks': True,
                'enable_numeric_range_checks': True
            },
            'pipeline_overrides': {},
            'email_alerts': {
                'failure_recipients': [],
                'warning_recipients': [],
                'digest_frequency': 'daily',
                'send_immediate_failure_alerts': True,
                'send_warning_digests': True
            },
            'logging': {
                'log_level': 'INFO',
                'max_log_entries': 1000,
                'log_retention_days': 30,
                'enable_console_logging': True
            },
            'default_behavior': {
                'fail_on_error': False,  # Default to continue on failures
                'stop_pipeline_on_failure': False  # Default to continue on failures
            }
        }
    
    def get_global_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration for global testing settings.
        """
        return {
            'api_config': {
                'email_api_url': 'https://locaria-dev-finance-reports.ew.r.appspot.com/api/tools/send_email_direct',
                'email_template_failure': 'Test Failure Alert',
                'email_template_warning': 'Test Warning Digest'
            },
            'bigquery_logging': {
                'project_id': DEFAULT_BIGQUERY_PROJECT_ID,
                'dataset_id': DEFAULT_BIGQUERY_DATASET_ID,
                'test_logs_table': DEFAULT_BIGQUERY_TEST_LOGS_TABLE
            }
        }
    
    def create_default_config_for_repository(self, repository_name: str) -> bool:
        """
        Create a default configuration for a repository.
        
        Args:
            repository_name: Name of the repository
            
        Returns:
            True if successful, False otherwise
        """
        default_config = self.get_default_config()
        return self.create_repository_config(repository_name, default_config)
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        """
        Validate a configuration dictionary.
        
        Args:
            config: Configuration dictionary to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check required top-level keys
        required_keys = ['thresholds', 'test_switches', 'email_alerts', 'logging']
        for key in required_keys:
            if key not in config:
                errors.append(f"Missing required key: {key}")
        
        # Validate thresholds structure
        if 'thresholds' in config:
            thresholds = config['thresholds']
            if not isinstance(thresholds, dict):
                errors.append("Thresholds must be a dictionary")
            else:
                # Check for required global threshold categories
                global_thresholds = thresholds.get('global', {})
                required_categories = ['row_count_change', 'data_freshness']
                for category in required_categories:
                    if category not in global_thresholds:
                        errors.append(f"Missing required global threshold category: {category}")
        
        # Validate test switches
        if 'test_switches' in config:
            switches = config['test_switches']
            if not isinstance(switches, dict):
                errors.append("Test switches must be a dictionary")
            else:
                # Check for required switches
                required_switches = ['enable_schema_validation', 'enable_business_logic_checks']
                for switch in required_switches:
                    if switch not in switches:
                        errors.append(f"Missing required test switch: {switch}")
                    elif not isinstance(switches[switch], bool):
                        errors.append(f"Test switch {switch} must be a boolean")
        
        return errors
    
    def get_threshold(self, repository_name: str, path: str, default_value: Any = None) -> Any:
        """
        Get a threshold value using dot notation path.
        
        Navigates nested config structure using dot-notation. Supports both global
        and pipeline-specific thresholds.
        
        Args:
            repository_name: Name of the repository (e.g., 'locate_2_pulls')
            path: Dot notation path to threshold.
                  Pipeline-specific: 'plunet_employee_table.check_data_completeness.completeness_threshold'
                  Global: 'global.row_count_change.warn_percentage'
            default_value: Default value if threshold not found
            
        Returns:
            Threshold value or default_value if not found
            
        Example:
            >>> threshold = manager.get_threshold(
            ...     'locate_2_pulls',
            ...     'plunet_employee_table.check_data_completeness.completeness_threshold',
            ...     default_value=0.95
            ... )
            >>> # Returns: 0.95 (or configured value if exists)
        """
        try:
            config = self.get_repository_config(repository_name)
            if not config:
                return default_value
            
            # Navigate nested dict structure using dot-notation (e.g., "thresholds.row_count.warn_percentage")
            current = config
            for key in path.split('.'):
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    # Path doesn't exist, return default
                    return default_value
            
            return current
            
        except Exception as e:
            print(f"Error getting threshold for {repository_name}.{path}: {e}")
            return default_value
    
    def set_threshold(self, repository_name: str, path: str, value: Any) -> bool:
        """
        Set a threshold value using dot notation path.
        
        Args:
            repository_name: Name of the repository
            path: Dot notation path to threshold (e.g., 'thresholds.plunet_employee_table.check_employee_data_completeness.completeness_threshold')
            value: New threshold value
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get current configuration
            current_config = self._get_repository_doc(repository_name)
            if not current_config:
                current_config = {}
            
            # Navigate to parent container, creating nested dicts as needed
            keys = path.split('.')
            current = current_config
            
            # Build nested structure up to the parent of target key
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            # Set the final value at the target path
            current[keys[-1]] = value
            
            # Save updated configuration
            return self.update_repository_config(repository_name, current_config)
            
        except Exception as e:
            print(f"Error setting threshold for {repository_name}.{path}: {e}")
            return False
    
    def get_pipeline_config(self, repository_name: str, pipeline_name: str) -> Dict[str, Any]:
        """
        Get all configuration for a specific pipeline.
        
        Args:
            repository_name: Name of the repository
            pipeline_name: Name of the pipeline
            
        Returns:
            Dictionary of pipeline configuration
        """
        try:
            config = self.get_repository_config(repository_name)
            if not config:
                return {}
            
            # Get pipeline-specific thresholds
            thresholds = config.get('thresholds', {})
            pipeline_thresholds = thresholds.get(pipeline_name, {})
            
            return {
                'thresholds': pipeline_thresholds,
                'global_thresholds': thresholds.get('global_thresholds', {}),
                'test_switches': config.get('test_switches', {}),
                'email_alerts': config.get('email_alerts', {}),
                'logging': config.get('logging', {})
            }
            
        except Exception as e:
            print(f"Error getting pipeline config for {repository_name}.{pipeline_name}: {e}")
            return {}

    def _get_repository_doc(self, repository_name: str) -> Dict[str, Any]:
        """
        Get the raw repository configuration document without global defaults.
        """
        try:
            doc_ref = self.firestore_client.collection(self.collection_name).document(repository_name)
            doc = doc_ref.get()
            if doc.exists:
                return copy.deepcopy(doc.to_dict())
            return {}
        except Exception as e:
            print(f"Error getting repository document for {repository_name}: {e}")
            return {}

    def _get_global_config(self) -> Dict[str, Any]:
        """
        Retrieve the global testing configuration document, creating defaults if missing.
        """
        try:
            doc_ref = self.firestore_client.collection(self.collection_name).document(self.global_config_doc)
            doc = doc_ref.get()
            if doc.exists:
                config = copy.deepcopy(doc.to_dict())
                # Ensure legacy structures don't leak repository maps to consumers
                config.pop('repositories', None)
                return config
            default_global = self.get_global_default_config()
            self._set_global_config(default_global)
            return copy.deepcopy(default_global)
        except Exception as e:
            print(f"Warning: Could not retrieve global testing config: {e}")
            return copy.deepcopy(self.get_global_default_config())

    def _set_global_config(self, config: Dict[str, Any]) -> None:
        """
        Persist global testing configuration to Firestore.
        """
        try:
            doc_ref = self.firestore_client.collection(self.collection_name).document(self.global_config_doc)
            doc_ref.set(config, merge=True)
        except Exception as e:
            print(f"Warning: Could not update global testing config: {e}")

    def _get_repository_map(self) -> Dict[str, Any]:
        """
        Retrieve the repositories document containing per-repo overrides.
        """
        try:
            doc_ref = self.firestore_client.collection(self.collection_name).document(DEFAULT_REPOSITORY_MAP_DOC)
            doc = doc_ref.get()
            if doc.exists:
                data = doc.to_dict() or {}
                # Firestore stores maps as dicts; ensure deep copy
                return copy.deepcopy(data)
            return {}
        except Exception as e:
            print(f"Warning: Could not retrieve repository overrides map: {e}")
            return {}

    def _get_repository_overrides(self, repository_name: str) -> Dict[str, Any]:
        """
        Get overrides for a repository from the repositories document.
        """
        repository_map = self._get_repository_map()
        overrides = repository_map.get(repository_name)
        if overrides:
            return copy.deepcopy(overrides)
        return {}

    def _deep_merge_dicts(self, base: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively merge two dictionaries, with overrides taking precedence.
        """
        for key, value in overrides.items():
            if isinstance(value, dict) and isinstance(base.get(key), dict):
                base[key] = self._deep_merge_dicts(base[key], value)
            else:
                base[key] = copy.deepcopy(value)
        return base