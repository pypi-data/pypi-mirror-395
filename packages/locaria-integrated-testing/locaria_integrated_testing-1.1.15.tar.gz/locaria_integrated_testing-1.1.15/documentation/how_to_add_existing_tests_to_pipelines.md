# How to Add Existing Tests to Pipelines

This guide walks you through integrating the Locaria Integrated Testing Framework into your data pipeline. Whether you're working with an existing pipeline or creating a new one, this guide will help you add comprehensive testing with minimal effort.

## Overview

The framework provides two types of tests: generic tests that work across any pipeline, and business logic tests that are specific to your domain. Generic tests handle common data quality checks like completeness, duplicates, numeric ranges, and freshness. Business logic tests validate domain-specific rules that are unique to your pipeline's purpose.

Both types of tests integrate seamlessly with your existing pipeline code. They run alongside your data processing logic, log results to BigQuery for historical tracking, and send email alerts when issues are detected. The framework also includes an acknowledgment system that prevents email spam by allowing users to mute known issues.

## Initial Setup

Before adding tests to your pipeline, you need to initialize the testing framework. The framework is configstore-agnostic and accepts arguments directly, so it works with any configstore implementation or without one entirely.

Start by importing the necessary modules at the top of your pipeline file. You'll need the generic test classes you plan to use, and if you have business logic tests, import those as well. The framework is available as a Python package, so you import it like any other dependency.

```python
from locaria_integrated_testing import DataQualityTests, RowCountTests, DuplicateTests, FreshnessTests, create_testkit
```

If you're using a configstore (like the one in locate_2_pulls), you can extract values from it and pass them to TestKit. However, the framework doesn't require any specific configstore implementation.

Next, initialize the test framework in your pipeline class's `__init__` method. Create a TestKit instance, which serves as the central orchestrator for all tests in your pipeline. The TestKit manages test results, handles logging, and coordinates email alerts.

```python
class YourPipeline:
    def __init__(self):
        import inspect, os
        
        # Initialize TestKit directly (works with any configstore or no configstore)
        # If you have a configstore, you can extract values from it and pass them here
        # Requires a BigQuery client for logging test results
        from google.cloud import bigquery
        bigquery_client = bigquery.Client(project="your-project-id")
        
        self.testkit = create_testkit(
            repository_name="your_repository",
            pipeline_name=os.path.splitext(os.path.basename(inspect.getfile(inspect.currentframe())))[0],
            bigquery_client=bigquery_client,  # Required: BigQuery client for test result logging
            firestore_project_id=None,  # Optional: defaults to "locaria-dev-config-store"
            fail_on_error=False  # Optional: if True, pipeline stops on test failures
        )
        
        # Initialize generic test classes
        caller_script = os.path.basename(inspect.getfile(inspect.currentframe()))
        self.data_quality_tests = DataQualityTests(self.testkit, caller_script=caller_script)
        self.row_count_tests = RowCountTests(self.testkit, caller_script=caller_script)
        self.duplicate_tests = DuplicateTests(self.testkit, caller_script=caller_script)
        self.freshness_tests = FreshnessTests(self.testkit, caller_script=caller_script)
```

The `caller_script` parameter helps the framework identify which pipeline is running the tests, which is useful for logging and debugging. The framework automatically extracts the pipeline name from the file path, but providing it explicitly ensures consistency.

## Adding Generic Tests

Generic tests are ready to use out of the box and require minimal configuration. They handle common data quality scenarios that apply to most pipelines. The key is knowing which tests to use and where to place them in your pipeline flow.

### Data Completeness Tests

Data completeness tests check that your data meets minimum quality thresholds. Use `check_data_completeness` to validate overall data quality, or `check_column_completeness` to validate specific critical columns.

Place completeness tests early in your pipeline, right after you load or fetch your data. This catches data quality issues before you spend time processing bad data. The test accepts a completeness threshold between 0 and 1, where 1.0 means no missing values are allowed.

```python
def run_pipeline(self):
    try:
        # Load your data
        df = self.load_data()
        
        # Check overall data completeness
        self.data_quality_tests.check_data_completeness(
            df=df,
            completeness_threshold=0.95,  # Allow up to 5% missing values
            issue_owner="analytics_hub.data_team_ack",
            issue_ack_access="analytics_hub.ops_ack"
        )
        
        # Check critical columns have no missing values
        self.data_quality_tests.check_column_completeness(
            df=df,
            columns=["employee_id", "date", "hours"],
            completeness_threshold=1.0,  # No missing values allowed
            issue_owner="analytics_hub.data_team_ack",
            issue_ack_access="analytics_hub.ops_ack"
        )
        
        # Continue with data processing...
        
    finally:
        self.testkit.finalize_run()
```

For a real-world example, see how the [global_content_main_data_sources_updater pipeline](https://github.com/Locaria/locate_2_pulls/blob/main/UpdatesHourly/global_content_main_data_sources_updater.py) uses completeness tests to validate multiple DataFrames before processing.

### Duplicate Detection Tests

Duplicate detection tests identify records that violate uniqueness constraints. Use these tests when your data should have unique keys, such as employee IDs, transaction IDs, or composite keys like employee ID plus date.

Place duplicate tests after data loading but before any deduplication logic runs. This helps you catch duplicates that come from the source system, which may indicate upstream data quality issues.

```python
# Check for duplicate records based on key columns
self.duplicate_tests.check_duplicate_records(
    df=df,
    key_columns=["employee_id", "date"],  # These columns should uniquely identify records
    issue_owner="analytics_hub.data_team_ack",
    issue_ack_access="analytics_hub.ops_ack"
)

# For more detailed duplicate information
self.duplicate_tests.check_duplicate_records_with_details(
    df=df,
    key_columns=["Job_number"],
    issue_owner="analytics_hub.data_team_ack",
    issue_ack_access="analytics_hub.ops_ack"
)
```

The `check_duplicate_records_with_details` method provides more comprehensive information about duplicates, which is useful when you need to investigate and fix duplicate issues. See the [plunet_jobs_main_pipeline](https://github.com/Locaria/locate_2_pulls/blob/main/UpdatesHourly/plunet_jobs_main_pipeline.py) for an example of detailed duplicate detection.

### Numeric Range Tests

Numeric range tests validate that numeric values fall within expected bounds. Use these tests to catch data entry errors, calculation mistakes, or unexpected data distributions.

Place numeric range tests after data loading and any necessary type conversions. The test accepts a dictionary mapping column names to expected ranges, where each range is a tuple of (minimum, maximum) values.

```python
self.data_quality_tests.check_numeric_ranges(
    df=df,
    column_ranges={
        "hours": (0, 24),  # Hours should be between 0 and 24
        "overtime": (0, 20),  # Overtime should be between 0 and 20
        "percentage": (0, 100)  # Percentage should be between 0 and 100
    },
    issue_owner="analytics_hub.data_team_ack",
    issue_ack_access="analytics_hub.ops_ack"
)
```

The test will log a warning for each value that falls outside the expected range, including details about which record and column violated the constraint. This makes it easy to identify and fix data quality issues.

### Row Count Tests

Row count tests validate that data volume changes are within expected thresholds. Use these tests after loading data to BigQuery to ensure your pipeline processed the expected amount of data.

Row count tests track historical row counts in Firestore, so they can detect both sudden drops and unexpected increases in data volume. The test supports both append and truncate operations, adjusting its validation logic accordingly.

```python
# After pushing data to BigQuery
self.push_to_bigquery(df, table_name="employee_table", overwrite=True)

# Validate row count change
self.row_count_tests.check_row_count_change(
    df=df,
    table_name="employee_table",
    operation_type="truncate",  # or "append" for incremental loads
    issue_owner="analytics_hub.data_team_ack",
    issue_ack_access="analytics_hub.ops_ack"
)
```

The test compares the current row count against historical values and flags significant changes. This helps catch issues like missing data sources, failed joins, or incorrect filtering logic. See the [freelancer_rates_updater pipeline](https://github.com/Locaria/locate_2_pulls/blob/main/UpdatesDaily/freelancer_rates_updater.py) for an example of row count validation after BigQuery operations.

### Freshness Tests

Freshness tests validate that your data is up-to-date. Use these tests to ensure your pipeline is running on schedule and that data sources are providing recent data.

Place freshness tests after data loading, using a timestamp column that indicates when each record was created or updated. The test checks the maximum age of data and flags records that are older than the specified threshold.

```python
self.freshness_tests.check_data_freshness(
    df=df,
    timestamp_column="updated_at",
    max_age_hours=24,  # Data should be no older than 24 hours
    issue_owner="analytics_hub.data_team_ack",
    issue_ack_access="analytics_hub.ops_ack"
)
```

You can also use freshness tests to validate timestamp progression, ensuring that timestamps move forward in time and don't contain future dates. This helps catch timezone issues, clock synchronization problems, or data entry errors.

## Adding Business Logic Tests

Business logic tests validate domain-specific rules that are unique to your pipeline. These tests are custom-built for your specific use case, but they follow the same patterns as generic tests.

If your pipeline has business logic tests, you can import and use them directly. In the locate_2_pulls repository, tests are located in the `modules/integrated_tests/pipeline_specific` directory, but you can organize your tests however makes sense for your repository structure.

```python
from modules.integrated_tests.pipeline_specific.plunet_employee_table import PlunetEmployeeTableBusinessTests

class YourPipeline:
    def __init__(self):
        # ... initialization code ...
        self.business_tests = PlunetEmployeeTableBusinessTests(testkit=self.testkit)
```

When calling business logic tests, always pass the `issue_owner` parameter (and, if needed, `issue_ack_access`) explicitly to ensure proper permission management. This makes it clear who receives alerts and who can acknowledge them.

```python
def run_pipeline(self):
    try:
        df = self.load_data()
        
        # Run business logic tests with explicit permissions
        self.business_tests.check_duplicate_employee_records(
            df,
            issue_owner="analytics_hub.data_team_ack",
            issue_ack_access="analytics_hub.ops_ack"
        )
        self.business_tests.check_employee_data_quality(
            df,
            issue_owner="analytics_hub.data_team_ack",
            issue_ack_access="analytics_hub.ops_ack"
        )
        
        # Continue with pipeline...
        
    finally:
        self.testkit.finalize_run()
```

For examples of business logic tests, see the [pipeline-specific tests directory](https://github.com/Locaria/locate_2_pulls/tree/main/modules/integrated_tests/pipeline_specific) in the locate_2_pulls repository. These examples demonstrate how to structure business logic tests with proper permission management, but the framework works with any repository structure.

## Test Placement Strategy

Where you place tests in your pipeline matters. Tests should run at strategic points to catch issues as early as possible while still having access to the data they need to validate.

Run data quality tests immediately after loading data from your source systems. This catches upstream issues before you invest time in processing bad data. Run completeness and duplicate tests at this stage, as they validate the raw input data.

Run transformation tests after any data transformations or enrichments. If you're joining multiple data sources, validate the results of those joins. If you're calculating derived fields, validate those calculations fall within expected ranges.

Run load validation tests after pushing data to BigQuery or other destination systems. Use row count tests to ensure the expected amount of data was loaded, and use freshness tests to validate that the loaded data is current.

Run post-load tests to validate the final state of your data. These tests check that all business rules are satisfied in the final output, which may differ from intermediate validation steps.

## Permission Management

All test methods support an `issue_owner` parameter that controls who can acknowledge issues in the Analytics Hub. This parameter accepts either a single permission string or a list of permission strings.

When you specify a single permission, only users with that permission can see and acknowledge the issue. When you specify a list of permissions, users with any of those permissions can acknowledge the issue. Users with admin permissions can always see and acknowledge all issues.

The default value is `"analytics_hub.data_team_ack"`, which is appropriate for most data quality issues. However, you should explicitly specify this parameter in all test calls to make permission assignment clear and consistent.

```python
# Single permission
self.data_quality_tests.check_data_completeness(
    df=df,
    issue_owner="analytics_hub.data_team_ack"
)

# Multiple permissions
self.data_quality_tests.check_data_completeness(
    df=df,
    issue_owner=["analytics_hub.data_team_ack", "analytics_hub.engineering_ack"]
)
```

For issues that require acknowledgment from multiple teams, use a list of permissions. For example, if an issue affects both data quality and system integration, you might want both the data team and engineering team to be able to acknowledge it.

## Error Handling and Finalization

Always wrap your pipeline logic in a try/finally block to ensure `testkit.finalize_run()` executes even when exceptions occur. The finalize method is idempotent, so it's safe to call multiple times if needed.

The finalize method sends email alerts for failures and warnings, logs test results to BigQuery in a single batch operation, and stores acknowledgment metadata in Firestore. It returns a summary dictionary with test statistics that you can use for logging or monitoring.

```python
def run_pipeline(self):
    try:
        # Your pipeline logic here
        df = self.load_data()
        self.run_tests(df)
        self.process_data(df)
        self.push_to_bigquery(df)
        
    finally:
        # Always finalize, even if pipeline fails
        test_summary = self.testkit.finalize_run()
        
        if test_summary:
            print(f"Pipeline completed. Tests: {test_summary.get('total_tests', 0)}, "
                  f"Passed: {test_summary.get('passed', 0)}, "
                  f"Warnings: {test_summary.get('warnings', 0)}, "
                  f"Failures: {test_summary.get('failures', 0)}")
```

The ExecutionManager integrates with the test framework to handle `TestFailureException` properly. When a test fails with `stop_pipeline=True`, the framework raises a `TestFailureException` that the ExecutionManager catches and logs appropriately. This ensures that test failures are properly tracked in BigQuery execution logs.

## Integration with ExecutionManager

If you're using the ExecutionManager decorator on your pipeline method, the integration is seamless. The ExecutionManager automatically handles test framework exceptions and ensures proper logging.

```python
from modules.utility.execution_manager import ExecutionManager

execution_manager = ExecutionManager()

@execution_manager.log_and_retry_execution(
    freshness_keyword="your_pipeline",
    frequency="HOURLY"
)
def run_pipeline(self):
    try:
        # Your pipeline logic and tests
        df = self.load_data()
        self.data_quality_tests.check_data_completeness(
            df=df,
            issue_owner="analytics_hub.data_team_ack"
        )
        # Continue processing...
        
    finally:
        self.testkit.finalize_run()
```

The ExecutionManager detects `TestFailureException` and stops retries immediately when tests fail, preventing unnecessary retry attempts for data quality issues that won't resolve themselves.

## Complete Example

Here's a complete example showing how to integrate tests into a pipeline, based on the [plunet_employee_table pipeline](https://github.com/Locaria/locate_2_pulls/blob/main/UpdatesHourly/plunet_employee_table.py). Note that this example uses the locate_2_pulls ConfigStore convenience method, but you can use TestKit directly with any configstore or no configstore:

```python
import pandas as pd
from pathlib import Path
import sys
import inspect, os
from locaria_integrated_testing import DataQualityTests, RowCountTests, create_testkit
from modules.integrated_tests.pipeline_specific.plunet_employee_table import PlunetEmployeeTableBusinessTests

class PlunetEmployeeTablePipeline:
    def __init__(self):
        # Initialize TestKit directly (works with any configstore or no configstore)
        # If you have a configstore, extract the BigQuery client from it
        # Example: bigquery_client = self.config_store.bigquery_client
        from google.cloud import bigquery
        bigquery_client = bigquery.Client(project="your-project-id")  # Or get from configstore
        
        self.testkit = create_testkit(
            repository_name="locate_2_pulls",
            pipeline_name=os.path.splitext(os.path.basename(inspect.getfile(inspect.currentframe())))[0],
            bigquery_client=bigquery_client,  # Required: BigQuery client for test result logging
            firestore_project_id=None,  # Optional: defaults to "locaria-dev-config-store"
            fail_on_error=False  # Optional: if True, pipeline stops on test failures
        )
        
        # Initialize test classes
        caller_script = os.path.basename(inspect.getfile(inspect.currentframe())))
        self.business_tests = PlunetEmployeeTableBusinessTests(testkit=self.testkit)
        self.data_quality_tests = DataQualityTests(self.testkit, caller_script=caller_script)
        self.row_count_tests = RowCountTests(self.testkit, caller_script=caller_script)
    
    @execution_manager.log_and_retry_execution(
        freshness_keyword="plunet_employee_table",
        frequency="HOURLY"
    )
    def run_employee_table_pipeline(self):
        try:
            # Load data
            employee_df = self.pull_plunet_employee_table()
            
            # Run tests on raw data
            self.business_tests.check_duplicate_employee_records(
                employee_df,
                issue_owner="analytics_hub.data_team_ack"
            )
            self.business_tests.check_employee_data_quality(
                employee_df,
                issue_owner="analytics_hub.data_team_ack"
            )
            
            if 'PlunetEmployeeID' in employee_df.columns:
                self.data_quality_tests.check_data_completeness(
                    employee_df,
                    test_name="check_employee_data_completeness",
                    issue_owner="analytics_hub.data_team_ack"
                )
            
            # Process and filter data
            employee_df = self.filter_employee_data(employee_df)
            
            # Push to BigQuery
            self.push_to_bigquery(employee_df)
            
            # Validate row count after load
            self.row_count_tests.check_row_count_change(
                employee_df,
                "plunet_employee_table",
                "truncate",
                "check_employee_table_row_count_post_bq",
                issue_owner="analytics_hub.data_team_ack"
            )
            
        finally:
            # Always finalize
            test_summary = self.testkit.finalize_run()
            if test_summary:
                print(f"Pipeline complete. Tests: {test_summary.get('total_tests', 0)}")
```

This example demonstrates the complete integration pattern: initialization in `__init__`, test execution at appropriate points in the pipeline flow, explicit permission assignment, and proper finalization in a finally block.

## Next Steps

Once you've added tests to your pipeline, monitor the results through the Analytics Hub acknowledgment interface. The interface shows all issues from your tests, filtered by your permissions. You can acknowledge known issues to prevent email spam, and track acknowledgment rates to understand which issues are being actively managed.

For more advanced usage, see the [How to Design New Tests](how_to_design_new_tests.md) guide, which covers creating custom business logic tests for your specific domain requirements.

