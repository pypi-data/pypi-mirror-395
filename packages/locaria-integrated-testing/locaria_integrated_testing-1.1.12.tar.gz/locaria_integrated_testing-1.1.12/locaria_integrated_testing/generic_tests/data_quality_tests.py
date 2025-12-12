"""
DataQualityTests - Common data quality validation checks.

Provides reusable tests for numeric ranges, data completeness (overall and column-level),
and date range validation. All tests support configurable thresholds and permission-based
issue ownership for acknowledgment management.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union, Tuple
import inspect, os
from ..main.testkit import TestKit

class DataQualityTests:
    """
    Reusable data quality validation tests.
    
    Validates numeric ranges, completeness thresholds, and date constraints.
    All methods support optional issue_owner parameter for permission-based
    acknowledgment management.
    """
    
    def __init__(self, testkit: TestKit, caller_script: Optional[str] = None): 
        """
        Initialize DataQualityTests with a TestKit instance.
        
        Args:
            testkit: TestKit instance for logging and configuration
        """
        self.testkit = testkit

        # Set caller script for easier identification in logs
        self.caller_script = caller_script if caller_script else os.path.basename(inspect.getfile(inspect.currentframe()))
    
    #########################################################################################
    def check_numeric_ranges(self, df: Optional[pd.DataFrame], column_ranges: Dict[str, Tuple[float, float]] = None, 
                           test_name: str = "check_numeric_ranges",
                           issue_owner: Union[str, List[str]] = "analytics_hub.data_team_ack",
                           issue_ack_access: Union[str, List[str], None] = None) -> bool:
        """
        Check that numeric columns contain values within expected ranges.
        
        Validates each specified column against min/max bounds. Logs warnings for
        violations with detailed information about which records failed.
        
        Args:
            df: DataFrame to validate
            column_ranges: Dictionary mapping column names to (min, max) tuples.
                          If None, attempts to load from config.
                          Example: {'hours': (0, 24), 'overtime': (0, 20)}
            test_name: Name of the test for logging
            issue_owner: Permission string or list of permission strings for acknowledgment
            issue_ack_access: Optional additional permission(s) with the same acknowledgment access
            
        Returns:
            True if all values within ranges (warnings logged for violations), False on error
            
        Example:
            >>> df = pd.DataFrame({
            ...     'hours': [8, 9, 25, 7],  # 25 is out of range
            ...     'overtime': [0, 2, 5, 0]
            ... })
            >>> tests.check_numeric_ranges(
            ...     df,
            ...     column_ranges={'hours': (0, 24), 'overtime': (0, 20)},
            ...     issue_owner='analytics_hub.data_team_ack'
            ... )
            >>> # Logs warning: "hours: 1 values above 24"
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
            
            # Load ranges from config if not explicitly provided (allows dynamic threshold updates)
            if column_ranges is None:
                config_ranges = self.testkit.get_threshold(f"{test_name}.numeric_ranges", {})
                if not config_ranges:
                    self.testkit.log_fail(
                        test_name = test_name, 
                        issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                        message = "No numeric ranges configured and none provided",
                        metrics = {"issue_owner": issue_owner}
                    )
                    return False
                
                # Transform config dict format {col: {min: x, max: y}} to tuple format {col: (x, y)}
                column_ranges = {}
                for column, range_config in config_ranges.items():
                    if 'min' in range_config and 'max' in range_config:
                        column_ranges[column] = (range_config['min'], range_config['max'])
            
            range_violations = []
            detailed_violations = []
            
            # Validate each column against its expected range
            for column, (min_val, max_val) in column_ranges.items():
                if column not in df.columns:
                    range_violations.append(f"{column}: column not found")
                    continue
                
                # Skip non-numeric columns (can't validate ranges on strings/dates)
                if not pd.api.types.is_numeric_dtype(df[column]):
                    range_violations.append(f"{column}: column is not numeric")
                    continue
                
                # Find records that violate min/max bounds (catches data entry errors, calculation bugs)
                below_min = df[df[column] < min_val]
                above_max = df[df[column] > max_val]
                
                # Build detailed violation report for below-min values (helps identify which records need fixing)
                if len(below_min) > 0:
                    range_violations.append(f"{column}: {len(below_min)} values below {min_val}")
                    for idx, row in below_min.iterrows():
                        name = row.get('Name', 'Unknown')
                        email = row.get('Email', 'Unknown')
                        month = row.get('ReportingMonth', 'Unknown')
                        value = float(row[column])
                        detailed_violations.append(f"{name} ({email}) in {month}: {value} (below {min_val})")
                
                # Build detailed violation report for above-max values
                if len(above_max) > 0:
                    range_violations.append(f"{column}: {len(above_max)} values above {max_val}")
                    for idx, row in above_max.iterrows():
                        name = row.get('Name', 'Unknown')
                        email = row.get('Email', 'Unknown')
                        month = row.get('ReportingMonth', 'Unknown')
                        value = float(row[column])
                        detailed_violations.append(f"{name} ({email}) in {month}: {value} (above {max_val})")
            
            if range_violations:
                # Create detailed message with line breaks
                detailed_summary = "<br/>".join(detailed_violations[:10])  # Limit to first 10 for readability
                if len(detailed_violations) > 10:
                    detailed_summary += f"<br/>... and {len(detailed_violations) - 10} more violations"
                
                metrics = {
                    "range_violations": range_violations, 
                    "total_checked": int(len(column_ranges)),  # Convert to int
                    "violation_count": int(len(detailed_violations)),  # Convert to int
                    "detailed_violations": detailed_violations[:20],  # Limit for JSON serialization
                    "threshold_source": "pipeline_config" if column_ranges != {} else "provided",
                    "issue_owner": issue_owner,
                    "issue_ack_access": ack_access_value,
                }
                self.testkit.log_warn(
                    test_name = test_name,
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Numeric range violations detected:<br/>{detailed_summary}",
                    metrics = metrics
                )
                return True  # Warning, not failure
            else:
                self.testkit.log_pass(
                    test_name,
                    f"All {len(column_ranges)} numeric columns within expected ranges",
                    {
                        "column_ranges": column_ranges,
                        "threshold_source": "pipeline_config" if column_ranges != {} else "provided"
                    }
                )
                return True
                
        except Exception as e:
            self.testkit.log_fail(
                test_name = test_name, 
                issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                message = f"Error checking numeric ranges: {str(e)}",
                metrics = {"issue_owner": issue_owner}
            )
            return False
    
    #########################################################################################
    def check_data_completeness(self, df: Optional[pd.DataFrame], completeness_threshold: float = None, 
                               test_name: str = "check_data_completeness",
                               issue_owner: Union[str, List[str]] = "analytics_hub.data_team_ack",
                               issue_ack_access: Union[str, List[str], None] = None) -> bool:
        """
        Check that overall data completeness is above a threshold.
        
        Calculates percentage of non-null values across entire DataFrame. Fails if
        completeness drops below threshold (default 95%).
        
        Args:
            df: DataFrame to validate
            completeness_threshold: Minimum percentage of non-null values (0.0-1.0).
                                   If None, uses config default (0.95).
            test_name: Name of the test for logging
            issue_owner: Permission string or list of permission strings for acknowledgment
            issue_ack_access: Optional additional permission(s) with the same acknowledgment access
            
        Returns:
            True if completeness >= threshold, False otherwise
            
        Example:
            >>> df = pd.DataFrame({
            ...     'col1': [1, 2, None, 4],
            ...     'col2': [5, None, 7, 8]
            ... })
            >>> # 6 non-null values out of 8 total = 75% completeness
            >>> tests.check_data_completeness(df, completeness_threshold=0.95)
            >>> # Logs failure: "Data completeness 75.00% below threshold 95.00%"
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
            
            # Load threshold from config if not provided (enables dynamic threshold tuning without code changes)
            if completeness_threshold is None:
                completeness_threshold = self.testkit.get_threshold(
                    f"{test_name}.completeness_threshold", 0.95
                )
            
            # Calculate overall completeness: percentage of non-null values across entire DataFrame
            total_cells = df.size
            null_cells = df.isnull().sum().sum()
            completeness = (total_cells - null_cells) / total_cells
            
            # Fail if too much data is missing (indicates upstream data quality issues or pipeline failures)
            if completeness < completeness_threshold:
                # Calculate column-level completeness for detailed diagnostics
                column_null_counts = df.isnull().sum()
                column_completeness = (1 - (column_null_counts / len(df))).to_dict()
                column_null_counts_dict = column_null_counts.to_dict()
                
                # Sort columns by null count (most problematic first) and filter to only columns with nulls
                columns_with_issues = {
                    col: {
                        "null_count": int(null_count),
                        "null_percentage": float(null_count / len(df)),
                        "completeness": float(column_completeness[col])
                    }
                    for col, null_count in column_null_counts_dict.items()
                    if null_count > 0
                }
                # Sort by null count descending
                columns_with_issues = dict(
                    sorted(columns_with_issues.items(), key=lambda x: x[1]["null_count"], reverse=True)
                )
                
                # Create summary message with top problematic columns
                top_columns = list(columns_with_issues.keys())[:5]  # Top 5 most problematic
                column_summary = ", ".join([
                    f"{col} ({columns_with_issues[col]['null_percentage']:.1%} missing)"
                    for col in top_columns
                ])
                
                metrics = {
                    "completeness": float(completeness),
                    "threshold": float(completeness_threshold),
                    "total_cells": int(total_cells),
                    "null_cells": int(null_cells),
                    "threshold_source": "pipeline_config" if completeness_threshold != 0.95 else "default",
                    "columns_with_issues": columns_with_issues,  # All columns with nulls, sorted by severity
                    "total_columns_with_issues": len(columns_with_issues),
                    "issue_owner": issue_owner,
                    "issue_ack_access": ack_access_value,
                }
                
                message = f"Data completeness {completeness:.2%} below threshold {completeness_threshold:.2%}"
                if column_summary:
                    message += f". Columns with missing data: {column_summary}"
                    if len(columns_with_issues) > 5:
                        message += f" (and {len(columns_with_issues) - 5} more)"
                
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = message,
                    metrics = metrics
                )
                return False
            else:
                self.testkit.log_pass(
                    test_name,
                    f"Data completeness {completeness:.2%} above threshold {completeness_threshold:.2%}",
                    {
                        "completeness": float(completeness),
                        "threshold": float(completeness_threshold),
                        "total_cells": int(total_cells),
                        "null_cells": int(null_cells),
                        "threshold_source": "pipeline_config" if completeness_threshold != 0.95 else "default"
                    }
                )
                return True
                
        except Exception as e:
            self.testkit.log_fail(
                test_name = test_name, 
                issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                message = f"Error checking data completeness: {str(e)}",
                metrics = {
                    "issue_owner": issue_owner,
                    "issue_ack_access": ack_access_value if 'ack_access_value' in locals() else issue_owner,
                }
            )
            return False
    
    #########################################################################################
    def check_column_completeness(self, df: Optional[pd.DataFrame], 
                                columns: Union[str, List[str]], 
                                completeness_threshold: float = None,
                                test_name: str = "check_column_completeness",
                                issue_owner: Union[str, List[str]] = "analytics_hub.data_team_ack",
                                issue_ack_access: Union[str, List[str], None] = None) -> bool:
        """
        Check that data completeness in specified columns is above a threshold.
        
        Validates individual columns rather than entire DataFrame. Useful for checking
        critical columns that must be complete (e.g., employee_id, email).
        
        Args:
            df: DataFrame to validate
            columns: Single column name or list of column names to check.
                    Example: 'employee_id' or ['employee_id', 'email', 'date']
            completeness_threshold: Minimum percentage of non-null values (0.0-1.0).
                                   Default 0.95 if None.
            test_name: Name of the test for logging
            issue_owner: Permission string or list of permission strings for acknowledgment
            issue_ack_access: Optional additional permission(s) with the same acknowledgment access
            
        Returns:
            True if all specified columns meet threshold, False if any column fails
            
        Example:
            >>> df = pd.DataFrame({
            ...     'employee_id': [1, 2, 3, None],  # 75% complete
            ...     'email': ['a@b.com', 'b@b.com', 'c@b.com', 'd@b.com']  # 100% complete
            ... })
            >>> tests.check_column_completeness(
            ...     df,
            ...     columns=['employee_id', 'email'],
            ...     completeness_threshold=0.95
            ... )
            >>> # Logs failure: "employee_id: 75.00% complete (1 nulls)"
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
                
            # Normalize input: handle both single column string and list of columns
            if isinstance(columns, str):
                columns = [columns]
                
            # Fail early if required columns don't exist (prevents confusing errors later)
            missing_columns = [col for col in columns if col not in df.columns]
            if missing_columns:
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                    message = f"Columns not found in DataFrame: {missing_columns}",
                    metrics = {
                        "missing_columns": missing_columns,
                        "issue_owner": issue_owner,
                        "issue_ack_access": ack_access_value,
                    }
                )
                return False
            
            # Load threshold from config if not provided
            if completeness_threshold is None:
                completeness_threshold = self.testkit.get_threshold(
                    f"{test_name}.completeness_threshold", 0.95
                )
            
            # Validate each column individually (critical columns must be complete for downstream processing)
            results = {}
            violations = []
            
            for column in columns:
                total_rows = len(df)
                null_count = df[column].isnull().sum()
                completeness = (total_rows - null_count) / total_rows
                
                results[column] = {
                    "completeness": float(completeness),
                    "total_rows": int(total_rows),
                    "null_count": int(null_count)
                }
                
                # Flag columns that don't meet threshold (missing critical data breaks joins/filters)
                if completeness < completeness_threshold:
                    violations.append(f"{column}: {completeness:.2%} complete ({null_count} nulls)")
            
            if violations:
                metrics = {
                    "results": results,
                    "threshold": float(completeness_threshold),
                    "violations": violations,
                    "threshold_source": "pipeline_config" if completeness_threshold != 0.95 else "default",
                    "issue_owner": issue_owner,
                    "issue_ack_access": ack_access_value,
                }
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Column completeness below threshold {completeness_threshold:.2%}: {violations}",
                    metrics = metrics
                )
                return False
            else:
                self.testkit.log_pass(
                    test_name,
                    f"All specified columns above completeness threshold {completeness_threshold:.2%}",
                    {
                        "results": results,
                        "threshold": float(completeness_threshold),
                        "threshold_source": "pipeline_config" if completeness_threshold != 0.95 else "default"
                    }
                )
                return True
                
        except Exception as e:
            self.testkit.log_fail(
                test_name = test_name, 
                issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                message = f"Error checking column completeness: {str(e)}",
                metrics = {
                    "issue_owner": issue_owner,
                    "issue_ack_access": ack_access_value if 'ack_access_value' in locals() else issue_owner,
                }
            )
            return False
    
    #########################################################################################    
    def check_date_ranges(self, df: Optional[pd.DataFrame], date_columns: Dict[str, Dict[str, Any]], 
                         test_name: str = "check_date_ranges",
                         issue_owner: Union[str, List[str]] = "analytics_hub.data_team_ack",
                         issue_ack_access: Union[str, List[str], None] = None) -> bool:
        """
        Check that date columns contain values within expected ranges.
        
        Args:
            df: DataFrame to validate
            date_columns: Dictionary mapping column names to date validation rules
                         Rules can include: 'min_date', 'max_date', 'future_allowed'
            test_name: Name of the test for logging
            issue_owner: Permission string or list of permission strings (e.g., "analytics_hub.data_team_ack" 
                        or ["analytics_hub.data_team_ack", "analytics_hub.engineering_ack"]) 
                        to set who can acknowledge this issue. Defaults to "analytics_hub.data_team_ack".
            issue_ack_access: Optional additional permission(s) with the same acknowledgment access
            
        Returns:
            True if all date values are within ranges, False otherwise
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
            
            date_violations = []
            
            for column, rules in date_columns.items():
                if column not in df.columns:
                    date_violations.append(f"{column}: column not found")
                    continue
                
                # Convert string dates to datetime (handles various formats, invalid dates become NaT)
                try:
                    date_series = pd.to_datetime(df[column], errors='coerce')
                except Exception:
                    date_violations.append(f"{column}: cannot convert to datetime")
                    continue
                
                # Flag unparseable dates (indicates data quality issues in source system)
                invalid_dates = date_series.isnull().sum()
                if invalid_dates > 0:
                    date_violations.append(f"{column}: {invalid_dates} invalid dates")
                
                # Validate dates aren't before business start date (catches historical data errors, wrong year entries)
                if 'min_date' in rules:
                    min_date = pd.to_datetime(rules['min_date'])
                    below_min = date_series[date_series < min_date]
                    if len(below_min) > 0:
                        date_violations.append(f"{column}: {len(below_min)} dates before {min_date}")
                
                # Validate dates aren't after business end date (catches data entry errors, wrong year entries)
                if 'max_date' in rules:
                    max_date = pd.to_datetime(rules['max_date'])
                    above_max = date_series[date_series > max_date]
                    if len(above_max) > 0:
                        date_violations.append(f"{column}: {len(above_max)} dates after {max_date}")
                
                # Flag future dates if not allowed (catches timezone bugs, clock sync issues, data entry mistakes)
                if not rules.get('future_allowed', True):
                    now = pd.Timestamp.now()
                    future_dates = date_series[date_series > now]
                    if len(future_dates) > 0:
                        date_violations.append(f"{column}: {len(future_dates)} future dates found")
            
            if date_violations:
                metrics = {
                    "date_violations": date_violations, 
                    "total_checked": len(date_columns),
                    "issue_owner": issue_owner,
                    "issue_ack_access": ack_access_value,
                }
                self.testkit.log_fail(
                    test_name = test_name, 
                    issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}",
                    message = f"Date range violations: {date_violations}",
                    metrics = metrics
                )
                return False
            else:
                self.testkit.log_pass(
                    test_name,
                    f"All {len(date_columns)} date columns within expected ranges",
                    {"date_columns": date_columns}
                )
                return True
                
        except Exception as e:
            self.testkit.log_fail(
                test_name = test_name, 
                issue_identifier = f"{self.caller_script}-{inspect.currentframe().f_code.co_name}", 
                message = f"Error checking date ranges: {str(e)}",
                metrics = {
                    "issue_owner": issue_owner,
                    "issue_ack_access": ack_access_value if 'ack_access_value' in locals() else issue_owner,
                }
            )
            return False
    