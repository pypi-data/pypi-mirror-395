"""
FreshnessTests - Data freshness and timestamp validation.

Validates that data is current, timestamps progress correctly, and data age
distributions are acceptable. Supports configurable age thresholds and frequency
validation for time-series data.
"""

import pandas as pd
import inspect, os
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple
from ..main.testkit import TestKit


class FreshnessTests:
    """
    Data freshness and timestamp validation tests.
    
    Ensures data is current, timestamps are valid and progressing correctly, and
    data age distributions meet business requirements. Supports frequency validation
    for time-series data patterns.
    """
    
    def __init__(self, testkit: TestKit, caller_script: Optional[str] = None):
        """
        Initialize FreshnessTests with a TestKit instance.
        
        Args:
            testkit: TestKit instance for logging and configuration
        """
        self.testkit = testkit
    
        # Set caller script for easier identification in logs
        self.caller_script = caller_script if caller_script else os.path.basename(inspect.getfile(inspect.currentframe()))

    def _resolve_permissions(self, issue_owner, issue_ack_access):
        if issue_ack_access is None:
            issue_ack_access = issue_owner
        return issue_owner, issue_ack_access

    @staticmethod
    def _with_permissions(metrics: Dict[str, Any], issue_owner, issue_ack_access) -> Dict[str, Any]:
        resolved = dict(metrics or {})
        resolved["issue_owner"] = issue_owner
        resolved["issue_ack_access"] = issue_ack_access
        return resolved

    def check_data_freshness(self, df: Optional[pd.DataFrame], timestamp_column: str, 
                           max_age_hours: int = None, test_name: str = "check_data_freshness",
                           issue_owner: Union[str, List[str]] = "analytics_hub.data_team_ack",
                           issue_ack_access: Union[str, List[str], None] = None) -> bool:
        """
        Check that data is fresh based on timestamp column.
        
        Validates that the most recent timestamp in the DataFrame is within the
        max_age_hours threshold. Fails if data is stale.
        
        Args:
            df: DataFrame to validate
            timestamp_column: Name of the column containing timestamps (e.g., 'updated_at', 'timestamp')
            max_age_hours: Maximum age in hours (default 24). If None, uses config.
            test_name: Name of the test for logging
            issue_owner: Permission string or list of permission strings for acknowledgment
            
        Returns:
            True if most recent timestamp is within max_age_hours, False otherwise
            
        Example:
            >>> df = pd.DataFrame({
            ...     'timestamp': [
            ...         pd.Timestamp.now() - pd.Timedelta(hours=2),
            ...         pd.Timestamp.now() - pd.Timedelta(hours=30),  # Stale
            ...         pd.Timestamp.now() - pd.Timedelta(hours=1)
            ...     ]
            ... })
            >>> tests.check_data_freshness(df, 'timestamp', max_age_hours=24)
            >>> # Logs failure: "Data is 30:00:00 old (max allowed: 1 day, 0:00:00)"
            >>> # Uses most recent timestamp (1 hour ago) which passes
        """
        try:
            issue_owner, issue_ack_access = self._resolve_permissions(issue_owner, issue_ack_access)
            if not self.testkit.is_test_enabled('enable_freshness_checks'):
                self.testkit.log_warn(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = "Freshness checks disabled - validation skipped",
                    metrics = self._with_permissions({}, issue_owner, issue_ack_access)
                )
                return True
            
            if df is None or df.empty:
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = "DataFrame is None or empty",
                    metrics = self._with_permissions({}, issue_owner, issue_ack_access)
                )
                return False
            
            if timestamp_column not in df.columns:
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = f"Timestamp column '{timestamp_column}' not found",
                    metrics = self._with_permissions({"timestamp_column": timestamp_column}, issue_owner, issue_ack_access)
                )
                return False
            
            # Load max age threshold from config if not provided (allows per-pipeline tuning)
            if max_age_hours is None:
                max_age_hours = self.testkit.get_threshold('data_freshness', 'max_age_hours', 24)
            
            # Parse timestamp strings to datetime objects (handles various formats, invalid becomes NaT)
            try:
                timestamps = pd.to_datetime(df[timestamp_column], errors='coerce')
            except Exception as e:
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = f"Error converting timestamps: {str(e)}",
                    metrics = self._with_permissions({"error": str(e), "timestamp_column": timestamp_column}, issue_owner, issue_ack_access)
                )
                return False
            
            # Flag unparseable timestamps (indicates data quality issues in source)
            invalid_timestamps = timestamps.isnull().sum()
            if invalid_timestamps > 0:
                self.testkit.log_fail(
                    test_name = test_name, issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Found {invalid_timestamps} invalid timestamps in column '{timestamp_column}'",
                    metrics = self._with_permissions({"invalid_timestamps": invalid_timestamps, "timestamp_column": timestamp_column}, issue_owner, issue_ack_access)
                )
                return False
            
            # Calculate age of most recent data point (indicates if pipeline is running/stuck)
            now = datetime.now(timezone.utc)
            max_age = timedelta(hours=max_age_hours)
            
            # Use most recent timestamp as proxy for overall data freshness
            latest_timestamp = timestamps.max()
            # Normalize timezone to UTC for consistent comparison
            if latest_timestamp.tzinfo is None:
                latest_timestamp = latest_timestamp.replace(tzinfo=timezone.utc)
            
            data_age = now - latest_timestamp
            
            # Fail if data is stale (indicates pipeline failure or upstream data source issues)
            if data_age > max_age:
                self.testkit.log_fail(
                    test_name = test_name, issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Data is {data_age} old (max allowed: {max_age})",
                    metrics = self._with_permissions({
                        "data_age_hours": data_age.total_seconds() / 3600,
                        "max_age_hours": max_age_hours,
                        "latest_timestamp": latest_timestamp.isoformat(),
                        "timestamp_column": timestamp_column,
                    }, issue_owner, issue_ack_access)
                )
                return False
            else:
                self.testkit.log_pass(
                    test_name = test_name, issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Data is fresh (age: {data_age}, max allowed: {max_age})",
                    metrics = {
                        "data_age_hours": data_age.total_seconds() / 3600,
                        "max_age_hours": max_age_hours,
                        "latest_timestamp": latest_timestamp.isoformat(),
                        "timestamp_column": timestamp_column
                    }
                )
                return True
                
        except Exception as e:
            self.testkit.log_fail(
                test_name = test_name, 
                issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                message = f"Error checking data freshness: {str(e)}",
                metrics = self._with_permissions({"error": str(e)}, issue_owner, issue_ack_access)
            )
            return False
    
    def check_timestamp_progression(self, df: Optional[pd.DataFrame], timestamp_column: str, 
                                  test_name: str = "check_timestamp_progression",
                                  issue_owner: Union[str, List[str]] = "analytics_hub.data_team_ack",
                                  issue_ack_access: Union[str, List[str], None] = None) -> bool:
        """
        Check that timestamps are progressing forward (no future timestamps).
        
        Validates that all timestamps are in the past. Useful for catching timezone
        issues, clock synchronization problems, or data entry errors.
        
        Args:
            df: DataFrame to validate
            timestamp_column: Name of the column containing timestamps (e.g., 'updated_at')
            test_name: Name of the test for logging
            issue_owner: Permission string or list of permission strings for acknowledgment
            
        Returns:
            True if no future timestamps found, False if any future timestamps detected
            
        Example:
            >>> df = pd.DataFrame({
            ...     'timestamp': [
            ...         pd.Timestamp.now() - pd.Timedelta(hours=1),
            ...         pd.Timestamp.now() + pd.Timedelta(days=1),  # Future timestamp
            ...         pd.Timestamp.now() - pd.Timedelta(hours=2)
            ...     ]
            ... })
            >>> tests.check_timestamp_progression(df, 'timestamp')
            >>> # Logs failure: "Found 1 future timestamps"
        """
        try:
            issue_owner, issue_ack_access = self._resolve_permissions(issue_owner, issue_ack_access)
            if not self.testkit.is_test_enabled('enable_freshness_checks'):
                self.testkit.log_warn(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = "Freshness checks disabled - validation skipped",
                    metrics = self._with_permissions({}, issue_owner, issue_ack_access)
                )
                return True
            
            if df is None or df.empty:
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = "DataFrame is None or empty",
                    metrics = self._with_permissions({}, issue_owner, issue_ack_access)
                )
                return False
            
            if timestamp_column not in df.columns:
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = f"Timestamp column '{timestamp_column}' not found",
                    metrics = self._with_permissions({"timestamp_column": timestamp_column}, issue_owner, issue_ack_access)
                )
                return False
            
            # Convert timestamp column to datetime
            try:
                timestamps = pd.to_datetime(df[timestamp_column], errors='coerce')
            except Exception as e:
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = f"Error converting timestamps: {str(e)}",
                    metrics = self._with_permissions({"error": str(e), "timestamp_column": timestamp_column}, issue_owner, issue_ack_access)
                )
                return False
            
            # Flag unparseable timestamps (indicates data quality issues)
            invalid_timestamps = timestamps.isnull().sum()
            if invalid_timestamps > 0:
                self.testkit.log_fail(
                    test_name = test_name, issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Found {invalid_timestamps} invalid timestamps",
                    metrics = self._with_permissions({"invalid_timestamps": invalid_timestamps, "timestamp_column": timestamp_column}, issue_owner, issue_ack_access)
                )
                return False
            
            # Detect future timestamps (catches timezone bugs, clock sync issues, data entry errors)
            now = datetime.now(timezone.utc)
            future_timestamps = timestamps[timestamps > now]
            
            if len(future_timestamps) > 0:
                self.testkit.log_fail(
                    test_name = test_name, issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Found {len(future_timestamps)} future timestamps",
                    metrics = self._with_permissions({
                        "future_timestamps": len(future_timestamps),
                        "timestamp_column": timestamp_column,
                        "max_future_timestamp": future_timestamps.max().isoformat(),
                    }, issue_owner, issue_ack_access)
                )
                return False
            else:
                self.testkit.log_pass(
                    test_name = test_name, issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"No future timestamps found in column '{timestamp_column}'",
                    metrics = {
                        "total_timestamps": len(timestamps),
                        "timestamp_column": timestamp_column,
                        "latest_timestamp": timestamps.max().isoformat()
                    }
                )
                return True
                
        except Exception as e:
            self.testkit.log_fail(
                test_name = test_name, 
                issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                message = f"Error checking timestamp progression: {str(e)}",
                metrics = self._with_permissions({"error": str(e)}, issue_owner, issue_ack_access)
            )
            return False
    
    def check_data_consistency(self, df: Optional[pd.DataFrame], timestamp_column: str, 
                             expected_frequency: str = None, test_name: str = "check_data_consistency",
                             issue_owner: Union[str, List[str]] = "analytics_hub.data_team_ack",
                             issue_ack_access: Union[str, List[str], None] = None) -> bool:
        """
        Check that data is consistent in terms of frequency and gaps.
        
        Validates timestamp sequence for missing periods. Useful for time-series data
        that should have regular intervals (hourly, daily, etc.). Also checks for duplicate timestamps.
        
        Args:
            df: DataFrame to validate
            timestamp_column: Name of the column containing timestamps (e.g., 'timestamp')
            expected_frequency: Expected frequency string (e.g., 'D' for daily, 'H' for hourly, 'W' for weekly).
                               Uses pandas frequency strings. If None, only checks for duplicates.
            test_name: Name of the test for logging
            issue_owner: Permission string or list of permission strings for acknowledgment
            
        Returns:
            True if data is consistent (no duplicates, no gaps if frequency specified), False otherwise
            
        Example:
            >>> df = pd.DataFrame({
            ...     'timestamp': pd.date_range('2024-01-01', periods=5, freq='D')
            ... })
            >>> # Remove one day to create a gap
            >>> df = df[df['timestamp'] != '2024-01-03']
            >>> tests.check_data_consistency(df, 'timestamp', expected_frequency='D')
            >>> # Logs warning: "Found 1 missing timestamps for frequency 'D'"
        """
        try:
            issue_owner, issue_ack_access = self._resolve_permissions(issue_owner, issue_ack_access)
            if not self.testkit.is_test_enabled('enable_freshness_checks'):
                self.testkit.log_warn(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = "Freshness checks disabled - validation skipped",
                    metrics = self._with_permissions({}, issue_owner, issue_ack_access)
                )
                return True
            
            if df is None or df.empty:
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = "DataFrame is None or empty",
                    metrics = self._with_permissions({}, issue_owner, issue_ack_access)
                )
                return False
            
            if timestamp_column not in df.columns:
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = f"Timestamp column '{timestamp_column}' not found",
                    metrics = self._with_permissions({"timestamp_column": timestamp_column}, issue_owner, issue_ack_access)
                )
                return False
            
            # Parse timestamp strings to datetime (handles various formats, invalid becomes NaT)
            try:
                timestamps = pd.to_datetime(df[timestamp_column], errors='coerce')
            except Exception as e:
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = f"Error converting timestamps: {str(e)}",
                    metrics = self._with_permissions({"error": str(e), "timestamp_column": timestamp_column}, issue_owner, issue_ack_access)
                )
                return False
            
            # Fail if timestamps can't be parsed (indicates data quality issues)
            invalid_timestamps = timestamps.isnull().sum()
            if invalid_timestamps > 0:
                self.testkit.log_fail(
                    test_name = test_name, issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Found {invalid_timestamps} invalid timestamps",
                    metrics = self._with_permissions({"invalid_timestamps": invalid_timestamps, "timestamp_column": timestamp_column}, issue_owner, issue_ack_access)
                )
                return False
            
            # Sort for gap detection (needed to identify missing periods)
            timestamps_sorted = timestamps.sort_values()
            
            # Flag duplicate timestamps (indicates data loading issues, double-processing)
            duplicate_timestamps = timestamps_sorted.duplicated().sum()
            if duplicate_timestamps > 0:
                self.testkit.log_fail(
                    test_name = test_name, issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Found {duplicate_timestamps} duplicate timestamps",
                    metrics = self._with_permissions({"duplicate_timestamps": duplicate_timestamps, "timestamp_column": timestamp_column}, issue_owner, issue_ack_access)
                )
                return False
            
            # Validate expected frequency if specified (detects missing periods in time-series data)
            if expected_frequency:
                # Generate expected timestamp sequence (e.g., daily means every day should have data)
                start_date = timestamps_sorted.min()
                end_date = timestamps_sorted.max()
                expected_range = pd.date_range(start=start_date, end=end_date, freq=expected_frequency)
                
                # Find gaps: timestamps that should exist but don't (indicates pipeline failures or missing source data)
                missing_timestamps = set(expected_range) - set(timestamps_sorted)
                
                if len(missing_timestamps) > 0:
                    self.testkit.log_warn(
                        test_name = test_name, issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                        message = f"Found {len(missing_timestamps)} missing timestamps for frequency '{expected_frequency}'",
                        metrics = self._with_permissions({
                            "missing_timestamps": len(missing_timestamps),
                            "expected_frequency": expected_frequency,
                            "timestamp_column": timestamp_column,
                            "date_range": f"{start_date} to {end_date}",
                        }, issue_owner, issue_ack_access)
                    )
                else:
                    self.testkit.log_pass(
                        test_name = test_name, issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                        message = f"All expected timestamps present for frequency '{expected_frequency}'",
                        metrics = {
                            "expected_frequency": expected_frequency,
                            "timestamp_column": timestamp_column,
                            "total_timestamps": len(timestamps_sorted),
                            "date_range": f"{start_date} to {end_date}"
                        }
                    )
            else:
                self.testkit.log_pass(
                    test_name = test_name, issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Timestamp consistency checked (no frequency specified)",
                    metrics = {
                        "timestamp_column": timestamp_column,
                        "total_timestamps": len(timestamps_sorted),
                        "date_range": f"{timestamps_sorted.min()} to {timestamps_sorted.max()}"
                    }
                )
            
            return True
                
        except Exception as e:
            self.testkit.log_fail(
                test_name = test_name, 
                issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                message = f"Error checking data consistency: {str(e)}",
                metrics = self._with_permissions({"error": str(e)}, issue_owner, issue_ack_access)
            )
            return False
    
    def check_partition_freshness(self, project_id: str, dataset_id: str, table_id: str, 
                                partition_column: str = None, test_name: str = "check_partition_freshness",
                                issue_owner: Union[str, List[str]] = "analytics_hub.data_team_ack",
                                issue_ack_access: Union[str, List[str], None] = None) -> bool:
        """
        Check that BigQuery table partitions are fresh.
        
        Args:
            project_id: BigQuery project ID
            dataset_id: BigQuery dataset ID
            table_id: BigQuery table ID
            partition_column: Partition column name (optional)
            test_name: Name of the test for logging
            issue_owner: Permission string or list of permission strings (e.g., "analytics_hub.data_team_ack" 
                        or ["analytics_hub.data_team_ack", "analytics_hub.engineering_ack"]) 
                        to set who can acknowledge this issue. Defaults to "analytics_hub.data_team_ack".
            
        Returns:
            True if partitions are fresh, False otherwise
        """
        try:
            issue_owner, issue_ack_access = self._resolve_permissions(issue_owner, issue_ack_access)
            if not self.testkit.is_test_enabled('enable_freshness_checks'):
                self.testkit.log_warn(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = "Freshness checks disabled - validation skipped",
                    metrics = self._with_permissions({}, issue_owner, issue_ack_access)
                )
                return True
            
            # This would require BigQuery client integration
            # For now, we'll log a warning that this feature needs implementation
            self.testkit.log_warn(
                test_name = test_name, issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                message = "Partition freshness check not yet implemented - requires BigQuery client integration",
                metrics = self._with_permissions({
                    "project_id": project_id,
                    "dataset_id": dataset_id,
                    "table_id": table_id,
                    "partition_column": partition_column,
                }, issue_owner, issue_ack_access)
            )
            return True
                
        except Exception as e:
            self.testkit.log_fail(
                test_name = test_name, 
                issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                message = f"Error checking partition freshness: {str(e)}",
                metrics = self._with_permissions({"error": str(e)}, issue_owner, issue_ack_access)
            )
            return False
    
    def check_data_age_distribution(self, df: Optional[pd.DataFrame], timestamp_column: str, 
                                  test_name: str = "check_data_age_distribution",
                                  issue_owner: Union[str, List[str]] = "analytics_hub.data_team_ack",
                                  issue_ack_access: Union[str, List[str], None] = None) -> bool:
        """
        Check the distribution of data ages to identify potential issues.
        
        Args:
            df: DataFrame to validate
            timestamp_column: Name of the column containing timestamps
            test_name: Name of the test for logging
            issue_owner: Permission string or list of permission strings (e.g., "analytics_hub.data_team_ack" 
                        or ["analytics_hub.data_team_ack", "analytics_hub.engineering_ack"]) 
                        to set who can acknowledge this issue. Defaults to "analytics_hub.data_team_ack".
            
        Returns:
            True if data age distribution is acceptable, False otherwise
        """
        try:
            issue_owner, issue_ack_access = self._resolve_permissions(issue_owner, issue_ack_access)
            if not self.testkit.is_test_enabled('enable_freshness_checks'):
                self.testkit.log_warn(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = "Freshness checks disabled - validation skipped",
                    metrics = self._with_permissions({}, issue_owner, issue_ack_access)
                )
                return True
            
            if df is None or df.empty:
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = "DataFrame is None or empty",
                    metrics = self._with_permissions({}, issue_owner, issue_ack_access)
                )
                return False
            
            if timestamp_column not in df.columns:
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = f"Timestamp column '{timestamp_column}' not found",
                    metrics = self._with_permissions({"timestamp_column": timestamp_column}, issue_owner, issue_ack_access)
                )
                return False
            
            # Convert timestamp column to datetime
            try:
                timestamps = pd.to_datetime(df[timestamp_column], errors='coerce')
            except Exception as e:
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = f"Error converting timestamps: {str(e)}",
                    metrics = self._with_permissions({"error": str(e), "timestamp_column": timestamp_column}, issue_owner, issue_ack_access)
                )
                return False
            
            # Check for invalid timestamps
            invalid_timestamps = timestamps.isnull().sum()
            if invalid_timestamps > 0:
                self.testkit.log_fail(
                    test_name = test_name, issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Found {invalid_timestamps} invalid timestamps",
                    metrics = self._with_permissions({"invalid_timestamps": invalid_timestamps, "timestamp_column": timestamp_column}, issue_owner, issue_ack_access)
                )
                return False
            
            # Calculate data ages
            now = datetime.now(timezone.utc)
            data_ages = now - timestamps
            
            # Convert to hours for analysis
            ages_hours = data_ages.dt.total_seconds() / 3600
            
            # Calculate statistics
            min_age = ages_hours.min()
            max_age = ages_hours.max()
            mean_age = ages_hours.mean()
            median_age = ages_hours.median()
            
            # Check for very old data
            warn_age_hours = self.testkit.get_threshold('data_freshness', 'warn_age_hours', 12)
            max_age_hours = self.testkit.get_threshold('data_freshness', 'max_age_hours', 24)
            
            old_data_count = (ages_hours > max_age_hours).sum()
            warn_data_count = (ages_hours > warn_age_hours).sum()
            
            if old_data_count > 0:
                self.testkit.log_fail(
                    test_name = test_name, issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Found {old_data_count} records older than {max_age_hours} hours",
                    metrics = self._with_permissions({
                        "old_data_count": old_data_count,
                        "max_age_hours": max_age_hours,
                        "min_age_hours": min_age,
                        "max_age_hours_actual": max_age,
                        "mean_age_hours": mean_age,
                        "median_age_hours": median_age,
                    }, issue_owner, issue_ack_access)
                )
                return False
            elif warn_data_count > 0:
                self.testkit.log_warn(
                    test_name = test_name, issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Found {warn_data_count} records older than {warn_age_hours} hours",
                    metrics = self._with_permissions({
                        "warn_data_count": warn_data_count,
                        "warn_age_hours": warn_age_hours,
                        "min_age_hours": min_age,
                        "max_age_hours": max_age,
                        "mean_age_hours": mean_age,
                        "median_age_hours": median_age,
                    }, issue_owner, issue_ack_access)
                )
            else:
                self.testkit.log_pass(
                    test_name = test_name, issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Data age distribution is acceptable",
                    metrics = {
                        "min_age_hours": min_age,
                        "max_age_hours": max_age,
                        "mean_age_hours": mean_age,
                        "median_age_hours": median_age,
                        "total_records": len(ages_hours)
                    }
                )
            
            return True
                
        except Exception as e:
            self.testkit.log_fail(
                test_name = test_name, 
                issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                message = f"Error checking data age distribution: {str(e)}",
                metrics = self._with_permissions({"error": str(e)}, issue_owner, issue_ack_access)
            )
            return False

