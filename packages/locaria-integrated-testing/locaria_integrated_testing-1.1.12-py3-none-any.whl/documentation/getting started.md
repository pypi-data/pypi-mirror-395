# Complete User Guide

## Table of Contents

1. [Framework Overview](#framework-overview)
2. [Getting Started](#getting-started)
3. [Core Components](#core-components)
4. [Generic Test Classes](#generic-test-classes)
5. [Business Logic Tests](#business-logic-tests)
6. [Email Alerting System](#email-alerting-system)
7. [Acknowledgment System](#acknowledgment-system)
8. [Configuration Management](#configuration-management)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)
11. [Advanced Usage](#advanced-usage)

## Framework Overview

The Locaria Integrated Testing Framework is a comprehensive testing system designed specifically for data pipelines and business logic validation. It provides a unified approach to testing data quality, business rules, and operational sanity across multiple pipelines.

### Key Benefits

- **Unified Testing Approach**: Consistent testing patterns across all pipelines
- **Business Logic Focus**: Tests that validate actual business rules, not just data structure
- **Smart Alerting**: Intelligent email system that prevents spam through acknowledgments
- **Persistent Logging**: All test results stored in BigQuery for historical analysis
- **Dynamic Configuration**: Firestore-based configuration for easy threshold updates
- **Pipeline Integration**: Seamless integration with existing data pipelines

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Data Pipeline                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   TestKit Core                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │   Logging   │ │   Config    │ │  Acknowledgment     │   │
│  │   System    │ │  Manager    │ │     Manager         │   │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                Test Classes                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │   Generic   │ │  Business   │ │    Custom Tests     │   │
│  │    Tests    │ │ Logic Tests │ │                     │   │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              External Integrations                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │BigQuery     │ │Email Manager│ │    Firestore        │   │
│  │  Logging    │ │             │ │   Configuration     │   │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Getting Started

### Environment Setup

The framework is configstore-agnostic and accepts arguments directly. You can use it with any configstore implementation or without one entirely. TestKit requires a BigQuery client for logging test results.

#### Required Parameters

- **bigquery_client**: A Google Cloud BigQuery client instance. This is required for logging test results to the `locaria-dev-config-store.cross_project_logging.integrated_test_logs` table.

#### Optional Environment Variables

For configuration when not using a configstore:

```bash
# Email API configuration (fallback)
export EMAIL_API_URL="https://your-app.appspot.com/api/tools/send_email_direct"
```

#### Default Configuration

The framework uses sensible defaults when parameters are not provided:
- **Firestore Project**: `locaria-dev-config-store` (default, can be overridden via `firestore_project_id` parameter)
- **BigQuery Logging**: Test results are written to `locaria-dev-config-store.cross_project_logging.integrated_test_logs` during `finalize_run()` in a single batch operation
- **Email API**: Can be configured via environment variable `EMAIL_API_URL`

If you're using a configstore (like the one in locate_2_pulls), you can extract values from it and pass them to TestKit. The framework doesn't depend on any specific configstore implementation.

### Basic Pipeline Integration

#### Step 1: Import Required Modules

```python
from locaria_integrated_testing import create_testkit, DataQualityTests, FreshnessTests, RowCountTests, DuplicateTests
```

#### Step 2: Initialize TestKit

```python
class YourPipeline:
    def __init__(self):
        # Initialize testing framework (works with any configstore or no configstore)
        # If you have a configstore, extract values from it and pass them here
        # You need to provide a BigQuery client instance for logging test results
        from google.cloud import bigquery
        bigquery_client = bigquery.Client(project="your-project-id")
        
        self.testkit = create_testkit(
            repository_name="your_repo",
            pipeline_name="your_pipeline",
            bigquery_client=bigquery_client,  # Required: BigQuery client for test result logging
            firestore_project_id=None,  # Optional: defaults to "locaria-dev-config-store"
            fail_on_error=False  # Optional: if True, pipeline stops on test failures
        )
        
        # Initialize test classes
        self.data_quality_tests = DataQualityTests(self.testkit)
        self.freshness_tests = FreshnessTests(self.testkit)
        self.row_count_tests = RowCountTests(self.testkit)
        self.duplicate_tests = DuplicateTests(self.testkit)
```

#### Step 3: Add Tests to Your Pipeline

When adding tests to your pipeline, always include the `issue_owner` parameter (and, when needed, the optional `issue_ack_access` parameter) to ensure proper permission management. `issue_owner` controls who receives the email notification, while `issue_ack_access` controls who can acknowledge the issue inside the FIN Profitability acknowledgment manager. Both default to `"analytics_hub.data_team_ack"` if not specified.

```python
def run_pipeline(self):
    try:
        # Load your data
        df = self.load_data()
        
        # Stage 1: Data quality tests with explicit permissions
        self.data_quality_tests.check_numeric_ranges(
            df, 
            {"hours": (0, 24)},
            issue_owner="analytics_hub.data_team_ack",
            issue_ack_access="analytics_hub.ops_ack"
        )
        self.duplicate_tests.check_duplicate_records(
            df, 
            ["employee_id", "date"],
            issue_owner="analytics_hub.data_team_ack",
            issue_ack_access="analytics_hub.ops_ack"
        )
        
        # Stage 2: Transform and load
        df_transformed = self.transform_data(df)
        self.row_count_tests.check_row_count_change(
            df_transformed, 
            "table_name", 
            "append",
            issue_owner="analytics_hub.data_team_ack",
            issue_ack_access="analytics_hub.ops_ack"
        )
        
        # Stage 3: Freshness checks
        self.load_to_bq(df_transformed, table="finance.time_splits")
        self.freshness_tests.check_data_freshness(
            df_transformed, 
            "timestamp",
            issue_owner="analytics_hub.data_team_ack",
            issue_ack_access="analytics_hub.ops_ack"
        )
        
    finally:
        # Always finalize the test run
        test_summary = self.testkit.finalize_run()
        print(f"Pipeline completed. Test summary: {test_summary}")
```

For complete working examples, see the pipelines in the [locate_2_pulls repository](https://github.com/Locaria/locate_2_pulls/tree/main/UpdatesHourly), such as [plunet_employee_table.py](https://github.com/Locaria/locate_2_pulls/blob/main/UpdatesHourly/plunet_employee_table.py) or [update_global_content_table.py](https://github.com/Locaria/locate_2_pulls/blob/main/UpdatesHourly/update_global_content_table.py).

## Core Components

### TestKit

The TestKit is the core orchestration component that manages test execution, logging, and alerting.

#### Key Features

- **Test Result Aggregation**: Collects and organizes all test results
- **BigQuery Batch Logging**: Efficient batch storage of test results to BigQuery
- **Email Alerting**: Smart email notifications with acknowledgment filtering
- **Configuration Management**: Dynamic configuration from Firestore (`locaria-dev-config-store`)
- **Acknowledgment Integration**: Prevents email spam for known issues

#### Initialization

```python
# Basic initialization (requires BigQuery client)
from google.cloud import bigquery
bigquery_client = bigquery.Client(project="your-project-id")

testkit = create_testkit(
    repository_name="your_repository",
    pipeline_name="daily_updates",
    bigquery_client=bigquery_client,  # Required: BigQuery client for test result logging
    fail_on_error=False,  # Optional: Continue pipeline on test failures (default: False)
    firestore_project_id=None  # Optional: defaults to "locaria-dev-config-store"
)
```

#### Core Methods

```python
# Logging methods
testkit.log_pass(test_name, message, metrics=None)
testkit.log_warn(test_name, message, metrics=None, acknowledgeable=True)
testkit.log_fail(test_name, message, metrics=None, acknowledgeable=True)

# Configuration
testkit.is_test_enabled(test_name)  # Check if test is enabled
testkit.get_config_value(key, default=None)  # Get configuration value

# Finalization
testkit.finalize_run()  # Send emails and finalize run
```

### Test Result Types

#### PASS
- Test completed successfully
- No issues detected
- Logged for historical tracking

#### WARN
- Test detected potential issues
- Pipeline continues execution
- May trigger warning digest emails
- Can be acknowledged to prevent future emails

#### FAIL
- Test detected critical issues
- May stop pipeline execution (if `fail_on_error=True`)
- Triggers immediate failure alert emails
- Can be acknowledged to prevent future emails

## Generic Test Classes

### DataQualityTests

Data quality tests for common validation scenarios.

#### Available Methods

All generic test methods support an optional `issue_owner` parameter that controls who can acknowledge issues in the Analytics Hub. This parameter accepts either a single permission string or a list of permission strings. When a list is provided, users with any of the specified permissions can acknowledge the issue.

```python
# Numeric range validation
data_quality_tests.check_numeric_ranges(
    df, 
    {"hours": (0, 24), "percentage": (0, 100)},
    issue_owner="analytics_hub.data_team_ack"  # Single permission
)

# Data completeness checks with multiple permissions
data_quality_tests.check_data_completeness(
    df, 
    completeness_threshold=0.95,
    issue_owner=["analytics_hub.data_team_ack", "analytics_hub.engineering_ack"]  # Multiple permissions
)

# Date range validation
data_quality_tests.check_date_ranges(
    df,
    date_columns={"start_date": ("2020-01-01", "2025-12-31")},
    issue_owner="analytics_hub.data_team_ack"
)
```

The `issue_owner` parameter defaults to `"analytics_hub.data_team_ack"` if not specified, ensuring all issues are accessible to the data team by default. You can override this for specific tests that require different permission groups.

#### Example Usage

When integrating tests into your pipeline, always specify the `issue_owner` parameter explicitly to ensure proper permission management. This makes it clear who should handle issues from each test.

```python
def validate_timesheet_data(self, df):
    """Validate timesheet data quality."""
    
    # Check numeric ranges with explicit permission assignment
    self.data_quality_tests.check_numeric_ranges(
        df, 
        {
            "hours": (0, 24),  # Hours should be 0-24
            "overtime": (0, 20)  # Overtime should be 0-20
        },
        issue_owner="analytics_hub.data_team_ack"
    )
    
    # Check data completeness with explicit permission
    self.data_quality_tests.check_data_completeness(
        df,
        completeness_threshold=0.98,  # 98% completeness required
        issue_owner="analytics_hub.data_team_ack"
    )
    
    # Check date ranges
    self.data_quality_tests.check_date_ranges(
        df,
        date_columns={
            "date": ("2020-01-01", "2025-12-31"),
            "submission_date": ("2020-01-01", "2025-12-31")
        },
        issue_owner="analytics_hub.data_team_ack"
    )
```

For a complete working example, see the [plunet_employee_table pipeline](https://github.com/Locaria/locate_2_pulls/blob/main/UpdatesHourly/plunet_employee_table.py) in the locate_2_pulls repository.

### FreshnessTests

Data freshness tests for ensuring data is up-to-date.

#### Available Methods

All freshness test methods support the `issue_owner` parameter for permission management.

```python
# Data freshness validation
freshness_tests.check_data_freshness(
    df, 
    timestamp_column="updated_at",
    max_age_hours=24,
    issue_owner="analytics_hub.data_team_ack"
)

# Timestamp progression checks
freshness_tests.check_timestamp_progression(
    df,
    timestamp_column="created_at",
    issue_owner="analytics_hub.data_team_ack"
)

# Data consistency validation
freshness_tests.check_data_consistency(
    df,
    timestamp_column="date",
    expected_frequency="daily",
    issue_owner="analytics_hub.data_team_ack"
)
```

#### Example Usage

```python
def validate_data_freshness(self, df):
    """Validate data freshness and consistency."""
    
    # Check data freshness with explicit permission
    self.freshness_tests.check_data_freshness(
        df,
        timestamp_column="last_updated",
        max_age_hours=6,  # Data should be no older than 6 hours
        issue_owner="analytics_hub.data_team_ack"
    )
    
    # Check timestamp progression
    self.freshness_tests.check_timestamp_progression(
        df,
        timestamp_column="created_at",
        issue_owner="analytics_hub.data_team_ack"
    )
    
    # Check data consistency
    self.freshness_tests.check_data_consistency(
        df,
        timestamp_column="date",
        expected_frequency="daily",
        issue_owner="analytics_hub.data_team_ack"
    )
```

### RowCountTests

Row count tracking tests for monitoring data volume changes.

#### Available Methods

```python
# Row count change validation
row_count_tests.check_row_count_change(
    df, 
    table_name="employees",
    operation_type="append",  # or "truncate"
    issue_owner="analytics_hub.data_team_ack"
)
```

#### Example Usage

```python
def validate_data_volume(self, df):
    """Validate data volume changes."""
    
    # Check row count changes for append operations
    self.row_count_tests.check_row_count_change(
        df,
        table_name="daily_transactions",
        operation_type="append",
        issue_owner="analytics_hub.data_team_ack"
    )
```

See the [freelancer_rates_updater pipeline](https://github.com/Locaria/locate_2_pulls/blob/main/UpdatesDaily/freelancer_rates_updater.py) for a complete example of row count validation after BigQuery operations.

### DuplicateTests

Duplicate detection tests for data integrity validation.

#### Available Methods

```python
# Duplicate record detection
duplicate_tests.check_duplicate_records(
    df, 
    key_columns=["employee_id", "date"],
    issue_owner="analytics_hub.data_team_ack"
)

# Duplicate detection with detailed information
duplicate_tests.check_duplicate_records_with_details(
    df,
    key_columns=["Job_number"],
    issue_owner="analytics_hub.data_team_ack"
)
```

#### Example Usage

```python
def validate_data_integrity(self, df):
    """Validate data integrity and uniqueness."""
    
    # Check for duplicate records
    self.duplicate_tests.check_duplicate_records(
        df,
        key_columns=["employee_id", "date", "project_code"],
        issue_owner="analytics_hub.data_team_ack"
    )
```

For examples of duplicate detection in production pipelines, see the [plunet_jobs_main_pipeline](https://github.com/Locaria/locate_2_pulls/blob/main/UpdatesHourly/plunet_jobs_main_pipeline.py) and [capacity_tracker_linguists_days_off](https://github.com/Locaria/locate_2_pulls/blob/main/UpdatesHourly/capacity_tracker_linguists_days_off.py) pipelines.

## Business Logic Tests

Business logic tests validate domain-specific rules and requirements. These tests are typically custom-built for specific pipelines and business domains.

### Creating Business Logic Tests

#### Step 1: Create Test Class

```python
from locaria_integrated_testing import create_testkit

class YourBusinessTests:
    """Business logic tests for your specific domain."""
    
    def __init__(self, testkit=None):
        if testkit is None:
            # Initialize TestKit (works with any configstore or no configstore)
            # Requires a BigQuery client for logging test results
            from google.cloud import bigquery
            bigquery_client = bigquery.Client(project="your-project-id")
            
            self.testkit = create_testkit(
                repository_name="your_repo",
                pipeline_name="your_pipeline",
                bigquery_client=bigquery_client,  # Required: BigQuery client for test result logging
                firestore_project_id=None,  # Optional: defaults to "locaria-dev-config-store"
                fail_on_error=False  # Optional: if True, pipeline stops on test failures
            )
        else:
            self.testkit = testkit
```

#### Step 2: Implement Business Rules

When implementing business logic tests, include the `issue_owner` parameter in your method signature and pass it through to the `log_warn` and `log_fail` calls via the metrics dictionary. This ensures proper permission management for issues detected by your custom tests.

```python
def check_financial_ratios(self, financial_data, issue_owner="analytics_hub.data_team_ack"):
    """Check that financial ratios are within acceptable bounds."""
    
    try:
        for _, row in financial_data.iterrows():
            # Calculate ratio
            ratio = row['revenue'] / row['costs'] if row['costs'] > 0 else 0
            
            # Check if ratio is within acceptable range
            if ratio < 1.2 or ratio > 3.0:
                self.testkit.log_warn(
                    "check_financial_ratios",
                    f"financial_ratio_{row['company']}",  # Stable issue identifier
                    f"Financial ratio out of bounds: {row['company']} - {ratio:.2f} (expected 1.2-3.0)",
                    {
                        "company": row['company'],
                        "ratio": ratio,
                        "revenue": row['revenue'],
                        "costs": row['costs'],
                        "issue_details": f"Financial ratio {ratio:.2f} for {row['company']} is outside acceptable range",
                        "issue_owner": issue_owner  # Include in metrics
                    },
                    acknowledgeable=True
                )
            else:
                self.testkit.log_pass(
                    "check_financial_ratios",
                    f"Financial ratio acceptable: {row['company']} - {ratio:.2f}"
                )
                
    except Exception as e:
        self.testkit.log_fail(
            "check_financial_ratios",
            "check_financial_ratios_error",
            f"Error checking financial ratios: {str(e)}",
            {
                "error": str(e),
                "issue_owner": issue_owner
            }
        )
```

For real-world examples of business logic tests, see the [pipeline-specific tests](https://github.com/Locaria/locate_2_pulls/tree/main/modules/integrated_tests/pipeline_specific) in the locate_2_pulls repository, such as [plunet_employee_table.py](https://github.com/Locaria/locate_2_pulls/blob/main/modules/integrated_tests/pipeline_specific/plunet_employee_table.py).

#### Step 3: Integrate with Pipeline

When calling business logic tests from your pipeline, explicitly pass the `issue_owner` parameter to make permission assignment clear and consistent.

```python
class YourPipeline:
    def __init__(self):
        # Initialize TestKit (works with any configstore or no configstore)
        # Requires a BigQuery client for logging test results
        from google.cloud import bigquery
        bigquery_client = bigquery.Client(project="your-project-id")
        
        self.testkit = create_testkit(
            repository_name="your_repo",
            pipeline_name="your_pipeline",
            bigquery_client=bigquery_client,  # Required: BigQuery client for test result logging
            firestore_project_id=None,  # Optional: defaults to "locaria-dev-config-store"
            fail_on_error=False  # Optional: if True, pipeline stops on test failures
        )
        self.business_tests = YourBusinessTests(self.testkit)
    
    def run_pipeline(self):
        try:
            # Load data
            financial_data = self.load_financial_data()
            
            # Run business logic tests with explicit permission assignment
            self.business_tests.check_financial_ratios(
                financial_data,
                issue_owner="analytics_hub.data_team_ack"
            )
            
            # Continue with pipeline...
            
        finally:
            test_summary = self.testkit.finalize_run()
```

For complete pipeline integration examples, see the [plunet_employee_table pipeline](https://github.com/Locaria/locate_2_pulls/blob/main/UpdatesHourly/plunet_employee_table.py) which demonstrates both generic and business logic test integration.

### Example: Capacity Tracker Tests

The capacity tracker pipeline includes comprehensive business logic tests with proper permission management:

```python
from modules.integrated_tests.pipeline_specific.capacity_tracker_linguists_days_off import CapacityTrackerBusinessTests

class YourPipeline:
    def __init__(self):
        # Initialize TestKit (works with any configstore or no configstore)
        # Requires a BigQuery client for logging test results
        from google.cloud import bigquery
        bigquery_client = bigquery.Client(project="your-project-id")
        
        self.testkit = create_testkit(
            repository_name="your_repository",
            pipeline_name="capacity_tracker",
            bigquery_client=bigquery_client,  # Required: BigQuery client for test result logging
            firestore_project_id=None,  # Optional: defaults to "locaria-dev-config-store"
            fail_on_error=False  # Optional: if True, pipeline stops on test failures
        )
        self.capacity_tests = CapacityTrackerBusinessTests(self.testkit)
    
    def run_pipeline(self):
        try:
            # Load timesheet data
            timesheet_df = self.load_timesheet_data()
            
            # Run capacity tracker business tests with explicit permissions
            self.capacity_tests.check_consistent_daily_hours_per_person(
                timesheet_df,
                issue_owner="analytics_hub.data_team_ack"
            )
            self.capacity_tests.check_absent_time_thresholds(
                timesheet_df,
                issue_owner="analytics_hub.data_team_ack"
            )
            
            # Continue with pipeline...
            
        finally:
            test_summary = self.testkit.finalize_run()
```

See the [capacity_tracker_linguists_days_off pipeline](https://github.com/Locaria/locate_2_pulls/blob/main/UpdatesHourly/capacity_tracker_linguists_days_off.py) for the complete implementation.

## Email Alerting System

The framework includes a sophisticated email alerting system that provides intelligent notifications while preventing email spam.

### Alert Types

#### Failure Alerts
- **Trigger**: FAIL test results
- **Timing**: Immediate notification
- **Content**: Detailed error information, stack traces, context
- **Recipients**: Pipeline owners, data team

#### Warning Digests
- **Trigger**: WARN test results
- **Timing**: End of pipeline run
- **Content**: Grouped warnings, summary statistics
- **Recipients**: Pipeline owners, stakeholders

### Email Templates

The framework uses pre-configured email templates:

#### Test Failure Alert Template
```
🚨 Test Failure Alert

Repository: {repository}
Pipeline: {pipeline}
Run ID: {run_id}

FAILURE SUMMARY:
{detailed_failure_information}

Run Duration: {duration}
Timestamp: {timestamp}

Please review and take appropriate action.
```

#### Test Warning Digest Template
```
⚠️ Test Warning Digest

Repository: {repository}
Pipeline: {pipeline}
Run ID: {run_id}

WARNING SUMMARY:
Total Warnings: {warning_count}

Warning Details:
{detailed_warning_information}

Run Duration: {duration}
Timestamp: {timestamp}

Please review these warnings and take appropriate action if needed.
```

### Smart Filtering

The email system includes intelligent filtering to prevent spam:

- **Acknowledgment Filtering**: Excludes acknowledged issues from emails
- **Rate Limiting**: Limits emails per day per pipeline
- **Context Preservation**: Shows acknowledged issues in context
- **Team Coordination**: Clear visibility of who acknowledged what

## Acknowledgment System

The acknowledgment system prevents email spam by allowing users to acknowledge known issues, which mutes them for a configurable period.

### How It Works

1. **Issue Detection**: Tests detect issues and log them with acknowledgment metadata
2. **Email Filtering**: Email system checks acknowledgment status before sending
3. **User Acknowledgment**: Users can acknowledge issues through web interface
4. **Mute Period**: Acknowledged issues are muted for 7 days (configurable)
5. **Automatic Expiry**: Mute periods expire automatically

### Acknowledgment Metadata

When logging issues that can be acknowledged, you must provide a stable `issue_identifier` argument and a `metrics` dictionary that includes `issue_details` and optionally `issue_owner`. The `issue_owner` field in metrics controls who can acknowledge the issue in the Analytics Hub web interface.

The `issue_owner` can be a single permission string or a list of permission strings. When a list is provided, users with any of the specified permissions can acknowledge the issue. If not specified in metrics, the framework defaults to `"analytics_hub.data_team_ack"`.

Example with single permission:

```python
self.testkit.log_warn(
    test_name="check_data_quality",
    issue_identifier="user@example.com",  # used as the acknowledgment key
    message="Data quality issue detected for user@example.com",
    metrics={
        "issue_identifier": "user@example.com",   # same as issue_identifier arg
        "issue_type": "data_quality",
        "issue_details": "Missing mandatory fields for user@example.com",
        "issue_owner": "analytics_hub.data_team_ack",  # Single permission
        "person_name": "User Name",
        "missing_fields": ["email", "country"],
        "total_records": 42,
    },
    acknowledgeable=True,  # default; included here for clarity
)
```

Example with multiple permissions:

```python
self.testkit.log_warn(
    test_name="check_system_integration",
    issue_identifier="integration_api_001",
    message="API integration issue detected",
    metrics={
        "issue_identifier": "integration_api_001",
        "issue_details": "API response time exceeded threshold",
        "issue_owner": ["analytics_hub.data_team_ack", "analytics_hub.engineering_ack"],  # Multiple permissions
        "api_endpoint": "/api/v1/data",
        "response_time_ms": 5000,
        "threshold_ms": 2000,
    },
    acknowledgeable=True
)
```

Behind the scenes:

- All acknowledgeable warnings are stored in `self.warnings` during the run.
- When you call `finalize_run()`, the framework batches all warn results **per test** and writes them in one Firestore call through `batch_update_issue_detections(test_name, issues)`.
- The Firestore structure remains:

```text
Collection: pipeline_acknowledgments
└── Document: {repo}%{pipeline}%{test_name}
    └── issues: {
        "<issue_identifier>": {
            "acknowledged": true/false,
            "muted_until": timestamp,
            "identifier": "<issue_identifier>",
            "details": "<issue_details>",
            ...additional metadata...
        },
        ...
    }
```

This ensures:

- Each logical issue (per email, per person, per key) is a separate entry.
- Acknowledging one issue does not mute unrelated ones.
- Firestore writes are batched and efficient.

### Web Interface

The acknowledgment system includes a modern web interface accessible at `/tools/acknowledgment-manager` in the [Analytics Hub](https://locaria-dev-finance-reports.ew.r.appspot.com/tools/acknowledgment-manager). The interface automatically filters issues based on your user permissions, showing only issues where you have the required `issue_owner` permission.

The filtering logic handles both single permission strings and lists of permissions. When an issue has multiple permissions in its `issue_owner` field, you can acknowledge it if you have any of those permissions. Users with admin permissions (such as `tools.admin` or `tools.view_all`) can see and acknowledge all issues regardless of the `issue_owner` setting.

The web interface provides real-time filtering by repository, pipeline, and test type. You can acknowledge or unacknowledge individual issues, view comprehensive issue details including first and last occurrence timestamps, and see who acknowledged what for better team coordination. Bulk operations allow you to handle multiple issues at once, making it efficient to manage large numbers of issues.

For implementation details of the web interface, see the [acknowledgment manager routes](https://github.com/Locaria/FIN_profitability_gcp/blob/main/routes/tools_routes.py) and [acknowledgment manager module](https://github.com/Locaria/FIN_profitability_gcp/blob/main/modules/tools/acknowledgment_manager_simple.py) in the FIN_profitability_gcp repository.

## Configuration Management

The framework stores configuration in Firestore (`locaria-dev-config-store`) under the `integrated_testing_config` collection. Settings are split into:

- `global_testing_config`: shared defaults such as `api_config`, `bigquery_logging`, default thresholds, and email behavior.
- `repositories`: a single document where each key is a repository (`locate_2_pulls`, `finance_scheduled_imports`, etc.) containing only the overrides for that repo (threshold tweaks, test switches, repo-specific alerts).

This layout keeps all GCP project IDs and BigQuery dataset/table names inside Firestore. The TestKit `__init__` method only contains the fallback constants and resolves everything else from the Firestore config at runtime.

### Configuration Structure

```json
{
  "global_testing_config": {
    "api_config": {
      "base_url": "https://locaria-dev-finance-reports.ew.r.appspot.com",
      "timeout_seconds": 20
    },
    "bigquery_logging": {
      "project_id": "locaria-dev-config-store",
      "dataset_id": "cross_project_logging",
      "table_id": "integrated_test_logs"
    },
    "default_thresholds": {
      "completeness": 1.0,
      "duplicate_ratio_warn": 0.02
    },
    "email_alerts": {
      "max_emails_per_day": 1,
      "default_issue_owner": "analytics_hub.data_team_ack"
    }
  },
  "repositories": {
    "locate_2_pulls": {
      "thresholds": {
        "plunet_employee_table": {
          "duplicate_ratio_warn": 0.01
        }
      },
      "test_switches": {
        "check_absent_time_thresholds": true
      },
      "email_alerts": {
        "primary_recipients": [
          "analytics-hub@locaria.com"
        ]
      }
    }
  }
}
```

Need to (re)seed Firestore? Run `locate_2_pulls/scripts/write_testing_config.py` to push the embedded configuration objects to `global_testing_config` and `repositories` without relying on external files.

### Accessing Configuration

```python
# Check if test is enabled
if testkit.is_test_enabled("check_data_quality"):
    # Run test
    
# Get configuration value
threshold = testkit.get_config_value("test_config.check_data_quality.thresholds.completeness_threshold", 0.95)

# Update configuration
testkit.update_config_in_firestore({
    "test_config.check_data_quality.thresholds.completeness_threshold": 0.98
})
```

### Configuration Best Practices

- **Use Sensible Defaults**: Provide fallback values for all configuration
- **Document Thresholds**: Clearly document what each threshold controls
- **Version Control**: Track configuration changes
- **Test Changes**: Validate configuration changes before deployment

## Best Practices

### Test Design

#### Focus on Business Logic
- Test actual business rules, not just data structure
- Use descriptive test names that explain the business rule
- Include both positive and negative test cases
- Test at multiple stages: intake, transform, load, post-load

#### Error Handling
- Always use try/finally blocks to ensure test finalization
- Handle missing data gracefully
- Provide meaningful error messages
- Log sufficient context for debugging

#### Performance
- Batch test operations when possible
- Use efficient pandas operations
- Avoid unnecessary data copies
- Cache configuration when appropriate

### Pipeline Integration

#### Test Placement
- **Intake Tests**: Validate incoming data quality
- **Transform Tests**: Check business logic during transformation
- **Load Tests**: Validate data after loading
- **Post-Load Tests**: Check final data state

#### Error Handling
```python
def run_pipeline(self):
    try:
        # Your pipeline logic
        data = self.load_data()
        self.run_tests(data)
        self.process_data(data)
        
    except Exception as e:
        # Log the error
        self.testkit.log_fail("pipeline_execution", f"Pipeline failed: {str(e)}")
        raise
        
    finally:
        # Always finalize
        test_summary = self.testkit.finalize_run()
```

### Acknowledgment Management

#### For Users
- **Regular Review**: Check for new issues regularly
- **Meaningful Acknowledgments**: Only acknowledge issues you understand
- **Documentation**: Use the reason field when acknowledging
- **Team Coordination**: Coordinate with team members on acknowledgments

#### For Developers
- **Consistent Metadata**: Use consistent field names and values
- **Meaningful Context**: Include enough information for debugging
- **Error Handling**: Handle acknowledgment failures gracefully
- **Testing**: Test acknowledgment functionality thoroughly

## Troubleshooting

### Common Issues

#### Tests Not Running
**Symptoms**: Tests are not executing or logging results

**Causes**:
- Test not enabled in configuration
- Missing test initialization
- Configuration not loaded

**Solutions**:
1. Check test configuration in Firestore
2. Verify test initialization in pipeline
3. Check configuration loading

```python
# Debug test configuration
print(f"Test enabled: {testkit.is_test_enabled('your_test_name')}")
print(f"Configuration: {testkit.get_config_value('test_config.your_test_name')}")
```

#### Emails Not Sending
**Symptoms**: No email notifications for test failures or warnings

**Causes**:
- Email configuration missing
- API endpoint not accessible
- All issues acknowledged

**Solutions**:
1. Check email configuration
2. Verify API endpoint accessibility
3. Check acknowledgment status

```python
# Debug email configuration
email_config = testkit.get_config_value('email_config')
print(f"Email config: {email_config}")

# Check if issues are acknowledged
filtered_results = testkit.acknowledge_manager.filter_acknowledged_issues(testkit.failures)
print(f"New issues: {len(filtered_results['new_issues'])}")
print(f"Acknowledged issues: {len(filtered_results['acknowledged_issues'])}")
```

#### Acknowledgment Not Working
**Symptoms**: Issues remain in emails after acknowledgment

**Causes**:
- Missing acknowledgment metadata
- Issue key mismatch
- Acknowledgment not saved

**Solutions**:
1. Verify acknowledgment metadata
2. Check issue key consistency
3. Verify Firestore permissions

```python
# Debug acknowledgment metadata
testkit.log_warn(
    "test_name",
    "Test message",
    {
        "person_email": "user@example.com",  # Required
        "issue_type": "test_type",           # Required
        "issue_key": "unique_key"            # Required
    }
)
```

### Debug Commands

#### Check Test Configuration
```python
# Check if test is enabled
enabled = testkit.is_test_enabled("your_test_name")
print(f"Test enabled: {enabled}")

# Get test configuration
config = testkit.get_config_value("test_config.your_test_name")
print(f"Test config: {config}")
```

#### Check Acknowledgment Status
```python
# Check if issue is acknowledged
is_acknowledged = testkit.acknowledge_manager.check_issue_acknowledged(
    test_name="your_test",
    issue_identifier="user@example.com",
    issue_type="your_issue_type",
    issue_key="your_key"
)
print(f"Issue acknowledged: {is_acknowledged}")
```

#### Check Email Configuration
```python
# Check email configuration
email_config = testkit.get_config_value("email_config")
print(f"Email config: {email_config}")

# Check email API URL
email_api_url = testkit.get_config_value("api_config.email_api_url")
print(f"Email API URL: {email_api_url}")
```

### Permission-Aware Email Routing

- Include `issue_owner` (string or list of permission names) in `metrics`
  when calling `log_warn` / `log_fail`.
- During `finalize_run()`, TestKit queries the Access Controller Firestore
  (`locaria-prod-authenticator`) to determine which users have those
  permissions (bindings → roles → permissions).
- Resolved emails are appended via `append_recipients` when calling
  `/api/tools/send_email_direct`, so acknowledgment owners receive alerts
  automatically.
- Override the lookup project with the environment variable
  `TESTKIT_ACCESS_CONTROL_PROJECT=<project_id>`. If the lookup fails or
  no permissions are provided, the framework falls back to the static
  recipients configured in Firestore (`email_alerts.failure_recipients`,
  `email_alerts.warning_recipients`).

## Advanced Usage

### Custom Test Classes

#### Creating Custom Test Classes
```python
from locaria_integrated_testing import create_testkit

class CustomBusinessTests:
    """Custom business logic tests for your domain."""
    
    def __init__(self, testkit=None):
        if testkit is None:
            self.testkit = create_testkit("your_repo", "your_pipeline")
        else:
            self.testkit = testkit
    
    def check_custom_business_rule(self, data):
        """Check custom business rule with acknowledgment support."""
        
        try:
            for item in data:
                if not self._validate_business_rule(item):
                    self.testkit.log_warn(
                        "check_custom_business_rule",
                        f"Business rule violation: {item['id']} - {item['details']}",
                        {
                            "person_email": item['owner_email'],
                            "issue_type": "business_rule_violation",
                            "issue_key": item['rule_id'],
                            "person_name": item['owner_name'],
                            "rule_name": item['rule_name'],
                            "violation_details": item['details']
                        }
                    )
                else:
                    self.testkit.log_pass(
                        "check_custom_business_rule",
                        f"Business rule satisfied: {item['id']}"
                    )
                    
        except Exception as e:
            self.testkit.log_fail(
                "check_custom_business_rule",
                f"Error checking business rule: {str(e)}"
            )
    
    def _validate_business_rule(self, item):
        """Validate individual business rule."""
        # Your business logic here
        return True  # or False
```

### Batch Operations

#### Batch Test Execution
```python
def run_batch_tests(self, data_batches):
    """Run tests on multiple data batches."""
    
    for batch_name, batch_data in data_batches.items():
        try:
            # Run tests on this batch
            self.data_quality_tests.check_numeric_ranges(batch_data, {"value": (0, 100)})
            self.duplicate_tests.check_duplicate_records(batch_data, ["id"])
            
        except Exception as e:
            self.testkit.log_fail(
                f"batch_test_{batch_name}",
                f"Batch test failed for {batch_name}: {str(e)}"
            )
```

### Performance Optimization

#### Efficient Test Execution
```python
def run_optimized_tests(self, df):
    """Run tests efficiently on large datasets."""
    
    # Use vectorized operations when possible
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    # Batch numeric range checks
    for column in numeric_columns:
        if column in self.expected_ranges:
            min_val, max_val = self.expected_ranges[column]
            invalid_mask = (df[column] < min_val) | (df[column] > max_val)
            
            if invalid_mask.any():
                invalid_rows = df[invalid_mask]
                for _, row in invalid_rows.iterrows():
                    self.testkit.log_warn(
                        "check_numeric_ranges",
                        f"Value out of range: {column} = {row[column]} (expected {min_val}-{max_val})",
                        {
                            "column": column,
                            "value": row[column],
                            "min_expected": min_val,
                            "max_expected": max_val
                        }
                    )
```

### Integration with External Systems

#### Custom Logging Integration
```python
    def custom_logging_integration(self, testkit):
        """Integrate with external logging systems."""
        
        # Override the default logging method
        original_write = testkit._write_test_results_to_bigquery
        
        def enhanced_write():
            # Call original BigQuery write
            original_write()
            
            # Add custom logging
            self.log_to_external_system(testkit.test_results)
        
        testkit._write_test_results_to_bigquery = enhanced_write

def log_to_external_system(self, result):
    """Log to external system."""
    # Your custom logging logic here
    pass
```

---

This comprehensive user guide covers all aspects of the Locaria Integrated Testing Framework. For specific implementation details, refer to the API Reference and Test Classes guides. For questions or support, contact the development team.

