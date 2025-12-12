# Integrated Testing Catalogue

This document provides a comprehensive overview of all integrated tests implemented across Locaria repositories. Each test is designed to detect data quality issues, business logic violations, and system problems that require manual intervention.

<!-- REPOSITORY: locate_2_pulls -->
## Repository: locate_2_pulls

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>

<!-- PIPELINE: plunet_employee_table.py -->
<tr>
<td rowspan="4"><strong><a href="https://github.com/Locaria/Locaria_Repo/blob/main/locate_2_pulls/UpdatesHourly/employee_table/plunet_employee_table.py">plunet_employee_table.py</a></strong><br><em>Pulls Plunet employee data and pushes it to BigQuery for time tracking and reporting</em></td>
<td>Business Logic</td>
<td>check_duplicate_employee_records</td>
<td>• Detects duplicate PlunetEmail entries in raw data before filtering<br>• Duplicated Emails mean there are multiple plunet IDs associated with a single Email<br>• Each employee should have only one, or maximum two accounts (one internal, one external)<br>• The test will not fail the pipeline, but send warnings</td>
</tr>
<tr>
<td>Business Logic</td>
<td>check_employee_data_quality</td>
<td>• Checks for missing PlunetEmail, PlunetEmployeeID, and PlunetEmployeeName<br>• Missing core employee identifiers prevent proper data processing and can cause downstream issues in time tracking and reporting systems</td>
</tr>
<tr>
<td>Generic</td>
<td>check_data_completeness</td>
<td>• Validates that no more than 0% of PlunetEmail records miss either Name or ID<br>• Ensures data completeness meets business requirements for reliable reporting and analytics</td>
</tr>
<tr>
<td>Generic</td>
<td>check_row_count_change</td>
<td>• Verifies that the rowcount meets the expected. Compares BQ table before & after push operation<br>• Confirms the ETL process completed successfully and no data was lost during the pipeline execution<br>• Threshold to trigger a warning is 20% more (or less). Threshold to fail the pipeline is 50%</td>
</tr>

<!-- PIPELINE: update_global_content_table.py -->
<tr>
<td rowspan="4"><strong><a href="https://github.com/Locaria/Locaria_Repo/blob/main/locate_2_pulls/UpdatesHourly/employee_table/update_global_content_table.py">update_global_content_table.py</a></strong><br><em>Enriches Firestore resource overview with HR and Plunet data for the Global Content team</em></td>
<td>Business Logic</td>
<td>check_plunet_duplicate_emails</td>
<td>• Detects duplicate PlunetEmail entries in raw Plunet data before deduplication<br>• Duplicated Emails mean there are multiple plunet IDs associated with a single Email<br>• Each employee should have only one, or maximum two accounts (one internal, one external)<br>• The test will not fail the pipeline, but send warnings</td>
</tr>
<tr>
<td>Business Logic</td>
<td>check_plunet_data_quality</td>
<td>• Checks for missing PlunetEmail, PlunetEmployeeID, and PlunetEmployeeName<br>• Missing core Plunet identifiers prevent proper employee data enrichment and can cause incomplete resource overviews</td>
</tr>
<tr>
<td>Business Logic</td>
<td>check_firestore_update_completeness</td>
<td>• Validates that all expected fields are populated in Firestore records after enrichment<br>• Ensures the enrichment process works correctly and all required employee data is available for the Global Content team<br>• Uses business logic to determine which fields are required based on employee status and billing type<br>• <strong>Always Required:</strong> <code>class</code>, <code>billing</code>, <code>team</code>, <code>email</code>, <code>CurrentEmployee</code>, <code>status</code>, <code>full_name</code>, <code>entry_date</code>, <code>plunet_id</code><br>• <strong>Payroll Employees Only:</strong> <code>weekly_hours</code>, <code>monthly_hours</code>, <code>FTEBob</code> (only required if <code>billing = "Payroll"</code>)<br>• <strong>Terminated Employees Only:</strong> <code>TerminationDate</code> (only required if <code>CurrentEmployee = False</code>)</td>
</tr>
<tr>
<td>Generic</td>
<td>check_data_completeness</td>
<td>• Validates that no more than 5% of PlunetEmail records are missing<br>• Ensures data completeness meets business requirements for reliable resource management</td>
</tr>

<!-- PIPELINE: capacity_tracker_linguists_days_off.py -->
<tr>
<td rowspan="6"><strong><a href="https://github.com/Locaria/Locaria_Repo/blob/main/locate_2_pulls/UpdatesHourly/capacity_tracker_linguists_days_off.py">capacity_tracker_linguists_days_off.py</a></strong><br><em>Calculates and stores monthly time capacity data for payroll-based linguists</em></td>
<td>Business Logic</td>
<td>check_consistent_daily_hours_per_person</td>
<td>• Validates that submitted monthly hours match expected weekly hours from whoisouttable<br>• Checks past 8 complete weeks (excluding current incomplete week)<br>• Flags inconsistencies when difference exceeds 10% of expected monthly hours<br>• Calculates expected monthly hours based on actual business days in each month</td>
</tr>
<tr>
<td>Business Logic</td>
<td>check_absent_time_thresholds</td>
<td>• Checks if absent time exceeds acceptable thresholds<br>• Threshold set to: 20% of total hours (warning only, does not fail pipeline)<br>• Calculates absent time as percentage of total hours year-to-date per person</td>
</tr>
<tr>
<td>Generic</td>
<td>check_duplicate_records</td>
<td>• Detects duplicate records in timesheet submissions data. Each month shall have only one submission per person. Submissions can have multiple rows, but just 1 date.</td>
</tr>
<tr>
<td>Generic</td>
<td>check_numeric_ranges</td>
<td>• Validates that numeric values are within expected ranges<br>• Checks WeeklyHours (10-50), DailyHours (3-10), MonthlyHours (40-200), HoursOff (0-200), ProductiveHours (0-200)<br>• Identifies outliers that may indicate data quality issues</td>
</tr>
<tr>
<td>Generic</td>
<td>check_data_completeness</td>
<td>• Validates that no more than 5% of capacity data records are missing<br</td>
</tr>
</tbody>
</table>

<!-- REPOSITORY: finance_scheduled_imports -->
## Repository: finance_scheduled_imports

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

<!-- REPOSITORY: FIN_profitability_gcp -->
## Repository: FIN_profitability_gcp

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: CAP_Quality_Checks

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: budget-tracker

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: App_Access_Permissions

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: firebase-auth

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: global-fx-rates

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: IMR_Cost_trackers

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: IMR_Verbatim_automation

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: incrementality

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: iom_keyword_classify

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: Keywords search volume and Ideas

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: Keywords-extraction-and-matching-tool-main

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: langchain_ai

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: LLMs-from-scratch

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: locaria_tools

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: locaria-integrated-testing-module

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: OML_video_transcription

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: penta-con

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: phrase_api

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: plotly_dash_example

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: rag_playground

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: SEO-analytics

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: SERP_monitor

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: sheet_logger

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: Stagwell-gcp-blueprint

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: streamlit_demo

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: tech_tests

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: Technical_interviews

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: thorsten_stuff

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: time_tracker

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

## Repository: xml-diffchecker

<table>
<thead>
<tr>
<th>Pipeline</th>
<th>Test Type</th>
<th>Test Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4"><em>No integrated tests implemented yet</em></td>
</tr>
</tbody>
</table>

---

## Test Categories

### Business Logic Tests
Tests that validate business rules and detect issues that require manual intervention in source systems.

### Generic Tests
Standard data quality tests that can be applied across different pipelines and data sources.

### Field Completeness Tests
Tests that validate required fields are populated based on business logic and conditional requirements.

---

## Adding New Tests

When adding new tests to this catalogue:

1. **Add the repository section** if it doesn't exist
2. **Add a new row** to the repository table with:
   - **Pipeline**: The script name and brief purpose
   - **Test Type**: Business Logic, Generic, or Field Completeness
   - **Test Name**: The exact method name
   - **What**: What the test checks
   - **Why**: Why this test is important for business operations
   - **Info**: Additional details, thresholds, or special behavior
3. **Include any special business rules** or field requirements
4. **Update the test categories** if new types are introduced

---

*Last Updated: 2025-10-23*
*Total Tests Implemented: 13*
*Repositories with Tests: 1 (locate_2_pulls)*