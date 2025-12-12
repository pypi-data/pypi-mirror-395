"""
DuplicateTests - Duplicate record detection and validation.

Identifies duplicate records based on single or composite key columns.
Provides both summary and detailed duplicate reporting for debugging.
"""

import pandas as pd
from typing import Dict, List, Any, Optional, Union
import inspect, os
from ..main.testkit import TestKit


class DuplicateTests:
    """
    Duplicate record detection and validation.
    
    Checks for duplicate records using single or composite key columns.
    Supports both quick summary checks and detailed duplicate reporting.
    """
    
    def __init__(self, testkit: TestKit, caller_script: Optional[str] = None):
        """
        Initialize DuplicateTests with a TestKit instance.
        
        Args:
            testkit: TestKit instance for logging and configuration
        """
        self.testkit = testkit
    
        # Set caller script for easier identification in logs
        self.caller_script = caller_script if caller_script else os.path.basename(inspect.getfile(inspect.currentframe()))

    def check_duplicate_records(self, df: Optional[pd.DataFrame], key_columns: List[str], 
                               test_name: str = "check_duplicate_records",
                               issue_owner: Union[str, List[str]] = "analytics_hub.data_team_ack",
                               issue_ack_access: Union[str, List[str], None] = None) -> bool:
        """
        Check for duplicate records based on specified key columns.
        
        Validates that the combination of key columns uniquely identifies each record.
        Fails if duplicates are found.
        
        Args:
            df: DataFrame to validate
            key_columns: List of column names that should uniquely identify records.
                        Single column: ["employee_id"]
                        Composite key: ["employee_id", "date", "project_code"]
            test_name: Name of the test for logging
            issue_owner: Permission string or list of permission strings for acknowledgment
            issue_ack_access: Optional additional permission(s) with the same acknowledgment access
            
        Returns:
            True if no duplicates found, False if duplicates detected
            
        Example:
            >>> df = pd.DataFrame({
            ...     'employee_id': [1, 2, 1, 3],
            ...     'date': ['2024-01-01', '2024-01-01', '2024-01-01', '2024-01-02']
            ... })
            >>> tests.check_duplicate_records(df, key_columns=['employee_id', 'date'])
            >>> # Logs failure: "Found 2 duplicate records based on key columns"
        """
        try:
            ack_access_value = issue_ack_access if issue_ack_access is not None else issue_owner
            if not self.testkit.is_test_enabled('enable_business_logic_checks'):
                self.testkit.log_warn(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = "Business logic checks disabled - validation skipped",
                    metrics = {
                        "issue_owner": issue_owner,
                        "issue_ack_access": ack_access_value,
                    }
                )
                return True
            
            if df is None or df.empty:
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = "DataFrame is None or empty",
                    metrics = {
                        "issue_owner": issue_owner,
                        "issue_ack_access": ack_access_value,
                    }
                )
                return False
            
            # Fail early if key columns missing (can't check uniqueness without them)
            missing_columns = [col for col in key_columns if col not in df.columns]
            if missing_columns:
                self.testkit.log_fail(
                    test_name = test_name,
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Missing key columns: {missing_columns}",
                    metrics = {
                        "missing_columns": missing_columns,
                        "issue_owner": issue_owner,
                        "issue_ack_access": ack_access_value,
                    }
                )
                return False
            
            # Count unique combinations of key columns (duplicates = total - unique)
            total_rows = len(df)
            unique_rows = df[key_columns].drop_duplicates()
            unique_count = len(unique_rows)
            
            # Fail if duplicates found (violates uniqueness constraint, causes data integrity issues)
            if total_rows != unique_count:
                duplicates = total_rows - unique_count
                metrics = {
                    "total_rows": total_rows,
                    "unique_rows": unique_count,
                    "duplicates": duplicates,
                    "key_columns": key_columns,
                    "issue_owner": issue_owner,
                    "issue_ack_access": ack_access_value,
                }
                self.testkit.log_fail(
                    test_name = test_name,
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Found {duplicates} duplicate records based on key columns {key_columns}",
                    metrics = metrics
                )
                return False
            else:
                self.testkit.log_pass(
                    test_name,
                    f"No duplicate records found based on key columns {key_columns}",
                    {
                        "total_rows": total_rows,
                        "unique_rows": unique_count,
                        "key_columns": key_columns
                    }
                )
                return True
                
        except Exception as e:
            self.testkit.log_fail(
                test_name = test_name, 
                issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                message = f"Error checking duplicate records: {str(e)}",
                metrics = {
                    "issue_owner": issue_owner,
                    "issue_ack_access": ack_access_value if 'ack_access_value' in locals() else issue_owner,
                }
            )
            return False

    def check_duplicate_records_with_details(self, df: Optional[pd.DataFrame], key_columns: List[str], 
                                           test_name: str = "check_duplicate_records_with_details",
                                           issue_owner: Union[str, List[str]] = "analytics_hub.data_team_ack",
                                           issue_ack_access: Union[str, List[str], None] = None) -> bool:
        """
        Check for duplicate records and provide detailed information about duplicates.
        
        Args:
            df: DataFrame to validate
            key_columns: List of column names that should uniquely identify records
            test_name: Name of the test for logging
            issue_owner: Permission string or list of permission strings (e.g., "analytics_hub.data_team_ack" 
                        or ["analytics_hub.data_team_ack", "analytics_hub.engineering_ack"]) 
                        to set who can acknowledge this issue. Defaults to "analytics_hub.data_team_ack".
            
        Returns:
            True if no duplicates found, False otherwise
        """
        try:
            ack_access_value = issue_ack_access if issue_ack_access is not None else issue_owner
            if not self.testkit.is_test_enabled('enable_business_logic_checks'):
                self.testkit.log_warn(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = "Business logic checks disabled - validation skipped",
                    metrics = {
                        "issue_owner": issue_owner,
                        "issue_ack_access": ack_access_value,
                    }
                )
                return True
            
            if df is None or df.empty:
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = "DataFrame is None or empty",
                    metrics = {
                        "issue_owner": issue_owner,
                        "issue_ack_access": ack_access_value,
                    }
                )
                return False
            
            # Fail early if key columns missing
            missing_columns = [col for col in key_columns if col not in df.columns]
            if missing_columns:
                self.testkit.log_fail(
                    test_name = test_name,
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Missing key columns: {missing_columns}",
                    metrics = {
                        "missing_columns": missing_columns,
                        "issue_owner": issue_owner,
                        "issue_ack_access": ack_access_value,
                    }
                )
                return False
            
            # Find all duplicate records (keep=False marks all instances of duplicates, not just extras)
            total_rows = len(df)
            duplicate_mask = df.duplicated(subset=key_columns, keep=False)
            duplicate_count = duplicate_mask.sum()
            
            if duplicate_count > 0:
                # Extract and sort duplicate records for analysis
                duplicate_records = df[duplicate_mask].sort_values(key_columns)
                # Group by key columns to count occurrences per duplicate key
                duplicate_groups = duplicate_records.groupby(key_columns).size()
                
                # Build human-readable summary of duplicate groups
                duplicate_summary = []
                for key_values, count in duplicate_groups.items():
                    # Handle both single-column (scalar) and multi-column (tuple) keys
                    if isinstance(key_values, tuple):
                        key_str = " | ".join([f"{col}={val}" for col, val in zip(key_columns, key_values)])
                    else:
                        key_str = f"{key_columns[0]}={key_values}"
                    duplicate_summary.append(f"{key_str} (appears {count} times)")
                
                metrics = {
                    "total_rows": total_rows,
                    "duplicate_count": duplicate_count,
                    "duplicate_groups": len(duplicate_groups),
                    "key_columns": key_columns,
                    "duplicate_summary": duplicate_summary[:10],  # Limit to first 10 for brevity
                    "issue_owner": issue_owner,
                    "issue_ack_access": ack_access_value,
                }
                self.testkit.log_fail(
                    test_name = test_name,
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Found {duplicate_count} duplicate records in {len(duplicate_groups)} groups based on key columns {key_columns}",
                    metrics = metrics
                )
                return False
            else:
                self.testkit.log_pass(
                    test_name,
                    f"No duplicate records found based on key columns {key_columns}",
                    {
                        "total_rows": total_rows,
                        "key_columns": key_columns
                    }
                )
                return True
                
        except Exception as e:
            self.testkit.log_fail(
                test_name = test_name, 
                issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                message = f"Error checking duplicate records with details: {str(e)}",
                metrics = {
                    "issue_owner": issue_owner,
                    "issue_ack_access": ack_access_value if 'ack_access_value' in locals() else issue_owner,
                }
            )
            return False
