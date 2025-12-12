"""
RowCountTests - Data volume change monitoring and validation.

Tracks row count changes over time using Firestore history. Supports both append
(incremental) and truncate (full refresh) operations with different comparison logic.
Validates changes against configurable percentage thresholds.
"""

import pandas as pd
import inspect, os
from typing import Dict, List, Any, Optional, Union
from ..main.testkit import TestKit


class RowCountTests:
    """
    Row count change monitoring and validation.
    
    Tracks historical row counts in Firestore and validates current counts against
    previous runs. Different logic for append vs truncate operations to account for
    expected data volume patterns.
    """
    
    def __init__(self, testkit: TestKit, caller_script: Optional[str] = None):
        """
        Initialize RowCountTests with a TestKit instance.
        
        Args:
            testkit: TestKit instance for logging and configuration
        """
        self.testkit = testkit
    
        # Set caller script for easier identification in logs
        self.caller_script = caller_script if caller_script else os.path.basename(inspect.getfile(inspect.currentframe()))

    @staticmethod
    def _with_permissions(metrics: Dict[str, Any], issue_owner, issue_ack_access) -> Dict[str, Any]:
        resolved = dict(metrics or {})
        resolved["issue_owner"] = issue_owner
        resolved["issue_ack_access"] = issue_ack_access
        return resolved

    def check_row_count_change(self, df: Optional[pd.DataFrame], table_name: str, 
                              operation_type: str = "append", test_name: str = "check_row_count_change",
                              issue_owner: Union[str, List[str]] = "analytics_hub.data_team_ack",
                              issue_ack_access: Union[str, List[str], None] = None) -> bool:
        """
        Check row count changes against historical data and configurable thresholds.
        
        Tracks row counts in Firestore and validates current count against previous runs.
        Different logic for append (incremental) vs truncate (full refresh) operations.
        Warns if change exceeds warn_percentage (default 20%), fails if exceeds fail_percentage (default 50%).
        
        Args:
            df: DataFrame to validate (row count is len(df))
            table_name: Name of the table (e.g., 'plunet_employee_table')
            operation_type: "append" (incremental load) or "truncate" (full refresh)
            test_name: Name of the test for logging
            issue_owner: Permission string or list of permission strings for acknowledgment
            issue_ack_access: Optional additional permission(s) with the same acknowledgment access
            
        Returns:
            True if change is acceptable, False if exceeds failure threshold
            
        Example:
            >>> # Previous run had 1000 rows, current has 1200 rows
            >>> tests.check_row_count_change(
            ...     df,  # 1200 rows
            ...     'employee_table',
            ...     'truncate',  # Full refresh operation
            ...     issue_owner='analytics_hub.data_team_ack'
            ... )
            >>> # Compares 1200 vs 1000 = 20% increase
            >>> # If warn_threshold=20%, logs warning
            >>> # If fail_threshold=50%, passes (20% < 50%)
        """
        try:
            ack_access_value = issue_ack_access if issue_ack_access is not None else issue_owner
            if not self.testkit.is_test_enabled('enable_row_count_validation'):
                self.testkit.log_warn(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = "Row count validation disabled - validation skipped",
                    metrics = self._with_permissions({}, issue_owner, ack_access_value)
                )
                return True
            
            if df is None:
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = "DataFrame is None",
                    metrics = self._with_permissions({}, issue_owner, ack_access_value)
                )
                return False
            
            current_count = len(df)
            current_date = self.testkit.start_time.date().isoformat()
            
            # Load thresholds from config (enables dynamic tuning without code changes)
            warn_percentage = self.testkit.get_threshold('global.row_count_change.warn_percentage', 20)
            fail_percentage = self.testkit.get_threshold('global.row_count_change.fail_percentage', 50)
            
            # Retrieve historical row counts from Firestore (tracks trends over time)
            historical_data = self._get_row_count_history(table_name)
            
            # Persist current run for future comparisons
            self._store_row_count_execution(table_name, current_count, current_date, operation_type)
            
            # Use different validation logic based on load strategy (append accumulates, truncate replaces)
            if operation_type == "append":
                # Append: compare current total vs previous total (should increase incrementally)
                comparison_result = self._compare_append_operation(
                    current_count, historical_data, warn_percentage, fail_percentage
                )
            elif operation_type == "truncate":
                # Truncate: compare current count vs previous day (full refresh, should be similar)
                comparison_result = self._compare_truncate_operation(
                    current_count, historical_data, warn_percentage, fail_percentage
                )
            else:
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = f"Invalid operation_type: {operation_type}. Must be 'append' or 'truncate'",
                    metrics = self._with_permissions({}, issue_owner, ack_access_value)
                )
                return False
            
            # Log result based on comparison
            if comparison_result['status'] == 'pass':
                self.testkit.log_pass(
                    test_name = test_name, 
                    message = f"Row count change acceptable: {comparison_result['message']}",
                    metrics=comparison_result['metrics']
                )
                return True
            elif comparison_result['status'] == 'warn':
                # Add issue_owner to metrics
                warn_metrics = comparison_result['metrics'].copy()
                warn_metrics['issue_owner'] = issue_owner
                warn_metrics['issue_ack_access'] = ack_access_value
                self.testkit.log_warn(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = f"Row count change warning: {comparison_result['message']}",
                    metrics=warn_metrics
                )
                return True
            else:  # fail
                # Add issue_owner to metrics
                fail_metrics = comparison_result['metrics'].copy()
                fail_metrics['issue_owner'] = issue_owner
                fail_metrics['issue_ack_access'] = ack_access_value
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = f"Row count change failure: {comparison_result['message']}",
                    metrics=fail_metrics
                )
                return False
                
        except Exception as e:
            self.testkit.log_fail(
                test_name = test_name, 
                issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                message = f"Error checking row count change: {str(e)}",
                    metrics = self._with_permissions({"error": str(e)}, issue_owner, ack_access_value if 'ack_access_value' in locals() else issue_owner)
            )
            return False

    def _get_row_count_history(self, table_name: str) -> List[Dict[str, Any]]:
        """Get row count history for a table from Firestore."""
        try:
            if not self.testkit.firestore_client:
                return []
            
            # Get history from Firestore
            history_ref = self.testkit.firestore_client.collection('row_count_history').document(table_name)
            history_doc = history_ref.get()
            
            if history_doc.exists:
                data = history_doc.to_dict()
                return data.get('executions', [])
            else:
                return []
                
        except Exception as e:
            print(f"Warning: Could not retrieve row count history: {e}")
            return []

    def _store_row_count_execution(self, table_name: str, row_count: int, date: str, operation_type: str):
        """Store current execution in Firestore history."""
        try:
            if not self.testkit.firestore_client:
                return
            
            # Get existing history
            history_ref = self.testkit.firestore_client.collection('row_count_history').document(table_name)
            history_doc = history_ref.get()
            
            executions = []
            if history_doc.exists:
                data = history_doc.to_dict()
                executions = data.get('executions', [])
            
            # Create execution record with metadata for trend analysis
            current_execution = {
                'date': date,
                'row_count': row_count,
                'operation_type': operation_type,
                'run_id': self.testkit.run_id,
                'timestamp': self.testkit.start_time.isoformat()
            }
            
            # Prepend to list (most recent first) for efficient access to latest data
            executions.insert(0, current_execution)
            
            # Keep only last 7 executions (limits Firestore document size, provides sufficient history for trend detection)
            executions = executions[:7]
            
            # Store back to Firestore
            history_ref.set({
                'table_name': table_name,
                'executions': executions,
                'last_updated': self.testkit.start_time.isoformat()
            })
            
        except Exception as e:
            print(f"Warning: Could not store row count execution: {e}")

    def _compare_append_operation(self, current_count: int, historical_data: List[Dict], 
                                 warn_percentage: float, fail_percentage: float) -> Dict[str, Any]:
        """Compare append operation against historical data."""
        # If no history, pass (first run, can't compare)
        if not historical_data:
            return {
                'status': 'pass',
                'message': f"No historical data available. Current count: {current_count}",
                'metrics': {'current_count': current_count, 'change_percentage': 0}
            }
        
        # For append: compare current total vs previous total (should increase incrementally, not dramatically)
        previous_execution = historical_data[0]  # Most recent execution
        previous_count = previous_execution['row_count']
        
        # Handle division by zero (first data load, or table was empty)
        if previous_count == 0:
            change_percentage = 100 if current_count > 0 else 0
        else:
            change_percentage = ((current_count - previous_count) / previous_count) * 100
        
        metrics = {
            'current_count': current_count,
            'previous_count': previous_count,
            'change_percentage': round(change_percentage, 2),
            'operation_type': 'append'
        }
        
        # Evaluate change against thresholds (large increases/decreases indicate data loading issues)
        if abs(change_percentage) <= warn_percentage:
            return {
                'status': 'pass',
                'message': f"Append operation: {current_count} rows (change: {change_percentage:+.1f}%)",
                'metrics': metrics
            }
        elif abs(change_percentage) <= fail_percentage:
            return {
                'status': 'warn',
                'message': f"Append operation: {current_count} rows (change: {change_percentage:+.1f}% - exceeds warning threshold {warn_percentage}%)",
                'metrics': metrics
            }
        else:
            return {
                'status': 'fail',
                'message': f"Append operation: {current_count} rows (change: {change_percentage:+.1f}% - exceeds failure threshold {fail_percentage}%)",
                'metrics': metrics
            }

    def _compare_truncate_operation(self, current_count: int, historical_data: List[Dict], 
                                   warn_percentage: float, fail_percentage: float) -> Dict[str, Any]:
        """Compare truncate operation against historical data."""
        # If no history, pass (first run, can't compare)
        if not historical_data:
            return {
                'status': 'pass',
                'message': f"No historical data available. Current count: {current_count}",
                'metrics': {'current_count': current_count, 'change_percentage': 0}
            }
        
        # For truncate: compare against previous day's count (not same-day runs)
        # Avoids false positives from multiple pipeline runs on same day (full refresh should be similar day-to-day)
        current_date = self.testkit.start_time.date().isoformat()
        previous_day_execution = None
        
        # Find first execution from different day (historical_data sorted most recent first, skip same-day runs)
        for execution in historical_data:
            if execution['date'] != current_date:
                previous_day_execution = execution
                break
        
        # If only same-day runs exist, pass (can't compare day-to-day without previous day data)
        if not previous_day_execution:
            return {
                'status': 'pass',
                'message': f"No previous day data available. Current count: {current_count}",
                'metrics': {'current_count': current_count, 'change_percentage': 0}
            }
        
        previous_count = previous_day_execution['row_count']
        
        # Handle division by zero (table was empty on previous day)
        if previous_count == 0:
            change_percentage = 100 if current_count > 0 else 0
        else:
            change_percentage = ((current_count - previous_count) / previous_count) * 100
        
        metrics = {
            'current_count': current_count,
            'previous_count': previous_count,
            'change_percentage': round(change_percentage, 2),
            'operation_type': 'truncate',
            'previous_date': previous_day_execution['date']
        }
        
        # Evaluate change against thresholds (large day-to-day changes indicate data loading or source issues)
        if abs(change_percentage) <= warn_percentage:
            return {
                'status': 'pass',
                'message': f"Truncate operation: {current_count} rows (change: {change_percentage:+.1f}% vs {previous_day_execution['date']})",
                'metrics': metrics
            }
        elif abs(change_percentage) <= fail_percentage:
            return {
                'status': 'warn',
                'message': f"Truncate operation: {current_count} rows (change: {change_percentage:+.1f}% vs {previous_day_execution['date']} - exceeds warning threshold {warn_percentage}%)",
                'metrics': metrics
            }
        else:
            return {
                'status': 'fail',
                'message': f"Truncate operation: {current_count} rows (change: {change_percentage:+.1f}% vs {previous_day_execution['date']} - exceeds failure threshold {fail_percentage}%)",
                'metrics': metrics
            }
