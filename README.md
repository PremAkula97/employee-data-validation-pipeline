# Employee Data Validation & ETL Pipeline

A Python-based data engineering project that demonstrates data extraction, validation, transformation, source-to-target mapping, and reconciliation using Pandas.

## Project Overview

This project processes employee records from a CSV source file, identifies data quality issues, transforms valid records into a standardized target structure, and exports the results for downstream analysis.

It demonstrates foundational ETL (Extract, Transform, Load) concepts commonly used in data analytics and data warehouse workflows.

## Technologies Used

- Python
- Pandas
- CSV
- Git and GitHub

## ETL Workflow

1. **Extract:** Read employee records from `data/employees.csv`.
2. **Validate:** Check for missing employee IDs, missing names, missing salaries, and negative salaries.
3. **Transform:** Map source fields to standardized target fields and calculate monthly salary.
4. **Load:** Export valid and invalid records to separate CSV files.
5. **Reconcile:** Verify that valid and invalid record counts equal the total source record count.

## Source-to-Target Mapping

| Source Field | Target Field | Transformation |
|---|---|---|
| EMP_ID | employee_id | Direct mapping |
| EMP_NAME | employee_name | Direct mapping |
| DEPARTMENT | department | Direct mapping |
| ANNUAL_PAY | annual_salary | Direct mapping |
| ANNUAL_PAY | monthly_salary | Annual salary / 12 |

## Validation Rules

Records are rejected when:

- Employee ID is missing.
- Employee name is missing or blank.
- Annual salary is missing or nonnumeric.
- Annual salary is negative.

A salary of zero is accepted.

Rejected records include a `rejection_reason` column explaining the validation failure.

## Sample Results

The sample dataset contains 10 employee records.

| Metric | Result |
|---|---|
| Total records | 10 |
| Valid records | 7 |
| Invalid records | 3 |
| Validation pass rate | 70% |
| Reconciliation | Passed |

All sample records are synthetic.

## Output Files

The pipeline generates three CSV files in the `output` directory:

- `valid_employees.csv` — validated and transformed employee records.
- `invalid_employees.csv` — rejected records with reasons.
- `data_quality_report.csv` — record counts and validation pass rate.

## How to Run

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the pipeline:

```bash
python main.py
```

## Future Enhancements

- Add automated unit tests.
- Detect duplicate employee IDs.
- Add SQL database integration.
- Implement more advanced data quality checks.

## Author

Prem Sai Akula