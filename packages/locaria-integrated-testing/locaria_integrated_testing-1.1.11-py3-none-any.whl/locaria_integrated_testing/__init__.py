"""
Locaria Integrated Testing Framework

A lightweight, automated testing system for data pipelines and tools.
Focuses on business-logic validation, data quality checks, and operational sanity tests.

Usage:
    from modules.integrated_tests import create_testkit, SchemaTests, DataQualityTests, FreshnessTests, RowCountTests, DuplicateTests
    
    # Initialize testing framework
    testkit = create_testkit("locate_2_pulls", "daily_updates")
    
    # Initialize test classes
    schema_tests = SchemaTests(testkit)
    data_quality_tests = DataQualityTests(testkit)
    freshness_tests = FreshnessTests(testkit)
    row_count_tests = RowCountTests(testkit)
    duplicate_tests = DuplicateTests(testkit)
    
    # Run tests
    schema_tests.check_required_columns(df, ["employee_id", "date", "hours"])
    data_quality_tests.check_numeric_ranges(df, {"hours": (0, 24)})
    freshness_tests.check_data_freshness(df, "timestamp")
    row_count_tests.check_row_count_change(df, "table_name", "append")
    duplicate_tests.check_duplicate_records(df, ["employee_id", "date"])
    
    # Finalize run
    testkit.finalize_run()
"""

__version__ = "1.1.11"
__author__ = "Locaria Data Team"

from .main.testkit import TestKit, create_testkit, log_pass, log_warn, log_fail, TestFailureException
from .generic_tests import DataQualityTests, FreshnessTests, RowCountTests, DuplicateTests
from .utils.config_manager import ConfigManager

__all__ = [
    'TestKit',
    'create_testkit', 
    'log_pass',
    'log_warn', 
    'log_fail',
    'TestFailureException',
    'DataQualityTests',
    'FreshnessTests',
    'RowCountTests',
    'DuplicateTests',
    'ConfigManager'
]

