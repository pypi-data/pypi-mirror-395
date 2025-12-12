# How to Design New Tests

This guide explains how to create custom business logic tests for your specific pipeline requirements. Business logic tests validate domain-specific rules that generic tests cannot cover, such as financial ratio calculations, capacity planning constraints, or data consistency rules unique to your domain.

## Understanding Test Structure

Business logic tests follow a consistent pattern that makes them easy to write and maintain. Each test method accepts your data as input, validates it against business rules, and uses the TestKit to log results. The TestKit handles all the infrastructure concerns like logging, email alerts, and acknowledgment tracking, so you can focus on the business logic.

Tests can produce three types of results: pass, warn, or fail. Pass results indicate the data meets all business rules. Warn results indicate potential issues that should be investigated but don't necessarily stop the pipeline. Fail results indicate critical issues that may require stopping the pipeline depending on your configuration.

All test results are automatically logged to BigQuery for historical tracking (written in a single batch operation during finalize_run()), and failures and warnings trigger email alerts. The acknowledgment system allows users to mute known issues through the Analytics Hub web interface, preventing email spam while maintaining visibility of issues that need attention.

## Creating a Test Class

Start by creating a new Python file in your pipeline-specific tests directory. The file should contain a class that encapsulates all business logic tests for your pipeline. In the locate_2_pulls repository, tests are organized in `modules/integrated_tests/pipeline_specific/`, but you can organize your tests however makes sense for your repository structure.

The class constructor accepts a TestKit instance, which provides all the logging and configuration functionality. The TestKit is created once per pipeline run and shared across all tests, ensuring consistent run IDs and efficient resource usage.

```python
"""
Business logic tests for your_pipeline_name.
These tests validate business rules specific to this pipeline's data and operations.
"""

import pandas as pd
from typing import Dict, Union, List

class YourPipelineBusinessTests:
    """Business logic tests for your pipeline."""
    
    def __init__(self, testkit):
        """
        Initialize YourPipelineBusinessTests with a TestKit instance.
        
        Args:
            testkit: TestKit instance for logging and configuration (required).
                     Should be created via `create_testkit()` from the locaria_integrated_testing package.
                     TestKit accepts arguments directly and works with any configstore or no configstore.
        """
        if testkit is None:
            raise ValueError("testkit is required. Use create_testkit() from locaria_integrated_testing to create a TestKit instance.")
        self.testkit = testkit
```

The constructor validates that a TestKit instance is provided, which helps catch configuration errors early. This pattern ensures that tests always have access to the framework's logging and configuration capabilities.

## Implementing Test Methods

Each test method should follow a consistent structure: validate inputs, perform business logic checks, and log results appropriately. Include the `issue_owner` parameter (and, when necessary, the optional `issue_ack_access` parameter) in your method signature to support permission management, and pass them through to the logging calls via the metrics dictionary:

Test methods should handle edge cases gracefully. Check for None or empty DataFrames before processing, validate that required columns exist, and catch exceptions to prevent test failures from crashing your pipeline.

```python
def check_your_business_rule(self, 
                            data: pd.DataFrame,
                            test_name: str = "check_your_business_rule",
                            issue_owner: Union[str, List[str]] = "analytics_hub.data_team_ack",
                            issue_ack_access: Union[str, List[str], None] = None) -> bool:
    """
    Check that your business rule is satisfied.
    
    This business rule validates that [describe what the rule checks].
    [Explain why this rule matters and what issues it detects.]
    
    Args:
        data: DataFrame containing the data to validate
        test_name: Name of the test for logging
        issue_owner: Permission string or list of permission strings (e.g., "analytics_hub.data_team_ack" 
                    or ["analytics_hub.data_team_ack", "analytics_hub.engineering_ack"]) 
                    to set who receives the alert email. Defaults to "analytics_hub.data_team_ack".
        issue_ack_access: Optional permission string or list defining who can acknowledge the issue in the FIN Profitability UI.
                    Defaults to issue_owner when omitted.
        
    Returns:
        True if the rule is satisfied, False otherwise
    """
    try:
        # Check if test is enabled
        if not self.testkit.is_test_enabled('enable_business_logic_checks'):
            self.testkit.log_warn(
                test_name, 
                f"{test_name}_disabled", 
                "Business logic checks disabled - validation skipped"
            )
            return True
        
        # Validate input data
        if data is None or data.empty:
            self.testkit.log_warn(
                test_name, 
                f"{test_name}_no_data", 
                "No data to validate - check data pipeline"
            )
            return True
        
        # Check required columns exist
        required_columns = ["column1", "column2"]
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            self.testkit.log_fail(
                test_name,
                f"{test_name}_missing_columns",
                f"Required columns missing: {missing_columns}",
            metrics={
                "missing_columns": missing_columns,
                "issue_owner": issue_owner,
                "issue_ack_access": issue_ack_access or issue_owner,
            }
            )
            return False
        
        # Perform business logic validation
        # [Your validation logic here]
        
        # If validation passes
        self.testkit.log_pass(
            test_name,
            "Business rule satisfied - all checks passed"
        )
        return True
        
    except Exception as e:
        self.testkit.log_fail(
            test_name,
            f"{test_name}_error",
            f"Error checking business rule: {str(e)}",
            metrics={
                "error": str(e),
                "issue_owner": issue_owner,
                "issue_ack_access": issue_ack_access or issue_owner,
            }
        )
        return False
```

This structure provides a solid foundation for any business logic test. The try/except block ensures that unexpected errors don't crash your pipeline, and the early validation checks prevent processing invalid data.

## Logging Test Results

The TestKit provides three methods for logging test results: `log_pass`, `log_warn`, and `log_fail`. Each method serves a specific purpose and should be used appropriately based on the severity of the issue detected.

Use `log_pass` when your validation succeeds completely. Pass results are logged for historical tracking but don't trigger alerts or require acknowledgment. They help you understand test coverage and track when issues are resolved.

```python
self.testkit.log_pass(
    test_name="check_data_quality",
    message="All records meet quality standards"
)
```

Use `log_warn` when you detect potential issues that should be investigated but don't necessarily indicate a critical problem. Warnings allow the pipeline to continue running while still notifying stakeholders about potential concerns. Warnings are acknowledgeable, so known issues can be muted to prevent email spam.

```python
self.testkit.log_warn(
    test_name="check_data_quality",
    issue_identifier="user@example.com",  # Stable identifier for acknowledgment
    message="Data quality issue detected for user@example.com",
    metrics={
        "issue_identifier": "user@example.com",
        "issue_details": "Missing mandatory fields for user@example.com",
        "issue_owner": issue_owner,  # Include in metrics
        "issue_ack_access": issue_owner,  # Or a different permission group
        "person_name": "User Name",
        "missing_fields": ["email", "country"],
        "total_records": 42,
    },
    acknowledgeable=True
)
```

Use `log_fail` when you detect critical issues that may require stopping the pipeline. Failures trigger immediate email alerts and can be configured to stop pipeline execution. Like warnings, failures are acknowledgeable, allowing known issues to be muted.

```python
self.testkit.log_fail(
    test_name="check_data_quality",
    issue_identifier="critical_error_001",
    message="Critical data quality issue detected",
    metrics={
        "issue_identifier": "critical_error_001",
        "issue_details": "More than 50% of records have missing critical fields",
        "issue_owner": issue_owner,
        "issue_ack_access": issue_owner,
        "missing_percentage": 0.65,
        "total_records": 1000,
    },
    stop_pipeline=False,  # Set to True to stop pipeline on failure
    acknowledgeable=True
)
```

The `issue_identifier` parameter is crucial for the acknowledgment system. It should be a stable, unique identifier for each distinct issue. For per-record issues, use the record's unique key (like an email address or ID). For aggregate issues, use a descriptive identifier that remains consistent across runs.

## Handling Multiple Issues

When your test detects multiple issues, such as multiple records violating a business rule, you have two options: log each issue individually or aggregate them into a single warning or failure.

Logging each issue individually provides the most granular tracking and acknowledgment. Each issue can be acknowledged separately, which is useful when some issues are known and acceptable while others need attention. This approach works well when the number of issues is manageable, typically under a few hundred.

```python
# Log each duplicate email individually
for email, email_records in duplicate_emails.groupby('PlunetEmail'):
    issue_identifier = str(email).lower().strip()
    
    self.testkit.log_warn(
        test_name="check_duplicate_employee_records",
        issue_identifier=issue_identifier,
        message=f"Found {len(email_records)} duplicate records for email: {email}",
        metrics={
            "issue_identifier": issue_identifier,
            "issue_details": f"Duplicate records for {email}",
            "issue_owner": issue_owner,
            "email": email,
            "record_count": len(email_records),
            "statuses": email_records['PlunetEmployeeStatus'].unique().tolist(),
        },
        acknowledgeable=True
    )
```

For a real-world example of per-issue logging, see the [plunet_employee_table business tests](https://github.com/Locaria/locate_2_pulls/blob/main/modules/integrated_tests/pipeline_specific/plunet_employee_table.py), which log each duplicate email as a separate issue.

Aggregating issues into a single warning or failure works well when you have many issues that are all variations of the same problem. This approach reduces noise in the acknowledgment interface and makes it easier to handle large numbers of similar issues. Use this approach when the individual issues don't need separate tracking or acknowledgment.

```python
# Aggregate multiple issues into a single warning
if len(violations) > 0:
    self.testkit.log_warn(
        test_name="check_numeric_ranges",
        issue_identifier="numeric_range_violations",
        message=f"Found {len(violations)} records with values outside expected ranges",
        metrics={
            "issue_identifier": "numeric_range_violations",
            "issue_details": f"{len(violations)} records violate numeric range constraints",
                "issue_owner": issue_owner,
                "issue_ack_access": issue_owner,
            "violation_count": len(violations),
            "violations": violations[:20],  # Limit for JSON serialization
        },
        acknowledgeable=True
    )
```

Choose the approach that best fits your use case. Per-issue logging provides better granularity but can create many acknowledgment entries. Aggregated logging is simpler but provides less detail about individual issues.

## Permission Management

All test methods should accept an `issue_owner` parameter that controls who receives alerts as well as an optional `issue_ack_access` parameter that controls who can acknowledge issues in the Analytics Hub. Include both in the method signature with sensible defaults, and pass them through to logging calls via the metrics dictionary.

Both parameters accept either a single permission string or a list of permission strings. When a list is provided, users with any of the specified permissions can act. This enables flexible permission management for issues that affect multiple teams (for example, emailing the data team but allowing operations to acknowledge the issue).

```python
def check_your_business_rule(self, 
                            data: pd.DataFrame,
                            test_name: str = "check_your_business_rule",
                            issue_owner: Union[str, List[str]] = "analytics_hub.data_team_ack",
                            issue_ack_access: Union[str, List[str], None] = None) -> bool:
    # ... validation logic ...
    
    if issue_detected:
        self.testkit.log_warn(
            test_name,
            issue_identifier,
            message,
            metrics=self._with_permissions(
                {
                    "issue_identifier": issue_identifier,
                    "issue_details": "Description of the issue",
                    # ... other metrics ...
                },
                issue_owner,
                issue_ack_access or issue_owner,
            ),
            acknowledgeable=True
        )
```

When calling test methods from your pipeline, explicitly pass the `issue_owner` parameter to make permission assignment clear. This ensures consistent permission management across your codebase and makes it easy to see who should handle issues from each test.

```python
# In your pipeline
self.business_tests.check_your_business_rule(
    data=df,
    issue_owner="analytics_hub.data_team_ack",
    issue_ack_access="analytics_hub.ops_ack"
)
```

For issues that require acknowledgment from multiple teams, pass a list of permissions. This is useful when an issue affects both data quality and system integration, or when multiple teams need visibility into the same issue.

```python
self.business_tests.check_system_integration_issue(
    data=df,
    issue_owner=["analytics_hub.data_team_ack", "analytics_hub.engineering_ack"],
    issue_ack_access=["analytics_hub.data_team_ack", "analytics_hub.ops_ack"]
)
```

## Real-World Examples

The locate_2_pulls repository contains several examples of well-designed business logic tests. These examples demonstrate best practices for test structure, error handling, and permission management.

The [plunet_employee_table business tests](https://github.com/Locaria/locate_2_pulls/blob/main/modules/integrated_tests/pipeline_specific/plunet_employee_table.py) demonstrate per-issue logging for duplicate detection. Each duplicate email is logged as a separate issue with detailed metadata, allowing individual acknowledgment and tracking.

The [capacity_tracker_linguists_days_off business tests](https://github.com/Locaria/locate_2_pulls/blob/main/modules/integrated_tests/pipeline_specific/capacity_tracker_linguists_days_off.py) demonstrate validation of business rules across multiple data sources. The tests compare timesheet data against days-off data to validate consistency, showing how to handle complex multi-source validations.

The [update_global_content_table business tests](https://github.com/Locaria/locate_2_pulls/blob/main/modules/integrated_tests/pipeline_specific/update_global_content_table.py) demonstrate validation of data completeness and consistency across different systems. The tests validate that Firestore updates are complete and that data from different sources is consistent.

Study these examples to understand how to structure your own business logic tests. They demonstrate patterns for handling edge cases, providing detailed error messages, and managing permissions appropriately.

## Testing Your Tests

Before deploying your tests to production, validate that they work correctly with both valid and invalid data. Test with empty DataFrames, None values, missing columns, and data that violates your business rules. Ensure that your tests handle edge cases gracefully and provide meaningful error messages.

Test that the acknowledgment system works correctly by verifying that issues appear in the Analytics Hub with the correct permissions. Test that you can acknowledge issues and that they're properly muted in subsequent runs. Verify that email alerts are sent appropriately and that acknowledged issues are excluded from emails.

Test the integration with your pipeline to ensure that tests don't interfere with normal pipeline execution. Verify that test failures stop the pipeline when configured to do so, and that warnings allow the pipeline to continue. Ensure that the finally block always executes and that `finalize_run()` is called even when exceptions occur.

## Best Practices

Keep test methods focused on a single business rule. If you need to validate multiple related rules, create separate test methods for each. This makes tests easier to understand, maintain, and debug. It also enables more granular acknowledgment, as users can acknowledge issues with one rule while still being alerted about issues with another.

Use descriptive test names that clearly explain what business rule is being validated. Good test names make it easy to understand what the test does without reading the implementation. They also make it easier to find relevant tests when investigating issues.

Include comprehensive metadata in your metrics dictionary. The metadata should provide enough context for someone to understand and fix the issue without needing to investigate further. Include identifiers, values, thresholds, and any other relevant information that helps diagnose the problem.

Handle errors gracefully. Your tests should never crash your pipeline, even when they encounter unexpected data or errors. Use try/except blocks to catch exceptions and log them as test failures rather than letting them propagate.

Validate inputs before processing. Check for None values, empty DataFrames, and missing columns before attempting to validate business rules. This prevents cryptic errors and provides clear feedback about data quality issues.

Use stable issue identifiers. The `issue_identifier` should remain consistent across pipeline runs for the same logical issue. This enables the acknowledgment system to track issues over time and properly mute acknowledged issues.

## Integration with Pipelines

Once you've created your business logic tests, integrate them into your pipeline following the patterns established in the locate_2_pulls repository. Import your test class in your pipeline file, initialize it in the `__init__` method, and call test methods at appropriate points in your pipeline flow.

Always pass the `issue_owner` parameter explicitly when calling test methods, even though it has a default value. This makes permission assignment clear and consistent. Wrap your pipeline logic in a try/finally block to ensure `testkit.finalize_run()` always executes.

```python
class YourPipeline:
    def __init__(self):
        # Initialize TestKit (works with any configstore or no configstore)
        # If you have a configstore, extract the BigQuery client from it
        # Example: bigquery_client = self.config_store.bigquery_client
        from google.cloud import bigquery
        from locaria_integrated_testing import create_testkit
        bigquery_client = bigquery.Client(project="your-project-id")  # Or get from configstore
        
        self.testkit = create_testkit(
            repository_name="your_repository",
            pipeline_name="your_pipeline",
            bigquery_client=bigquery_client,  # Required: BigQuery client for test result logging
            firestore_project_id=None,  # Optional: defaults to "locaria-dev-config-store"
            fail_on_error=False  # Optional: if True, pipeline stops on test failures
        )
        self.business_tests = YourPipelineBusinessTests(testkit=self.testkit)
    
    def run_pipeline(self):
        try:
            df = self.load_data()
            
            # Run business logic tests with explicit permissions
            self.business_tests.check_your_business_rule(
                df,
                issue_owner="analytics_hub.data_team_ack"
            )
            
            # Continue with pipeline processing...
            
        finally:
            self.testkit.finalize_run()
```

For complete integration examples, see the [plunet_employee_table pipeline](https://github.com/Locaria/locate_2_pulls/blob/main/UpdatesHourly/plunet_employee_table.py) or the [update_global_content_table pipeline](https://github.com/Locaria/locate_2_pulls/blob/main/UpdatesHourly/update_global_content_table.py) in the locate_2_pulls repository.

## Documentation

Document your business logic tests clearly so other team members can understand what each test validates and why it matters. Include docstrings that explain the business rule, what issues the test detects, and what actions should be taken when issues are found.

Update your pipeline's documentation to describe the tests that are run and what they validate. This helps team members understand the quality checks that are in place and what to expect from the testing framework.

Consider adding comments in your test code to explain non-obvious validation logic or business rules that might not be immediately clear to someone reading the code later. Good documentation makes it easier to maintain and extend your tests over time.

## Next Steps

After creating your business logic tests, monitor their results through the Analytics Hub acknowledgment interface. Review issues regularly to understand data quality patterns and identify areas where business rules might need adjustment.

Consider creating additional tests as you discover new data quality issues or business rule violations. The framework makes it easy to add new tests incrementally, so you can start with the most critical validations and expand coverage over time.

For more information about using existing tests, see the [How to Add Existing Tests to Pipelines](how_to_add_existing_tests_to_pipelines.md) guide. For details about the framework's capabilities, see the [Complete User Guide](user_guide.md).

