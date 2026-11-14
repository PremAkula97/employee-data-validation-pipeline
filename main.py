from pathlib import Path
import pandas as pd

# Project folders
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "employees.csv"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# EXTRACT: Read employee data from CSV
employees = pd.read_csv(INPUT_FILE)

print("EMPLOYEE DATA VALIDATION PIPELINE")
print("---------------------------------")
print(f"Total source records: {len(employees)}")

# TRANSFORM: Check data quality
missing_id = employees["EMP_ID"].isna()
missing_name = (
    employees["EMP_NAME"].isna()
    | employees["EMP_NAME"].astype("string").str.strip().eq("").fillna(False)
)

salary = pd.to_numeric(employees["ANNUAL_PAY"], errors="coerce")
missing_salary = salary.isna()
negative_salary = salary < 0

# A record is invalid if any validation rule fails
invalid_mask = (
    missing_id
    | missing_name
    | missing_salary
    | negative_salary
)

valid_employees = employees.loc[~invalid_mask].copy()
invalid_employees = employees.loc[invalid_mask].copy()

# Add explanations for rejected records
def rejection_reason(row):
    reasons = []

    if pd.isna(row["EMP_ID"]):
        reasons.append("Missing employee ID")

    if pd.isna(row["EMP_NAME"]) or not str(row["EMP_NAME"]).strip():
        reasons.append("Missing employee name")

    row_salary = pd.to_numeric(
        pd.Series([row["ANNUAL_PAY"]]), errors="coerce"
    ).iloc[0]

    if pd.isna(row_salary):
        reasons.append("Missing or invalid salary")
    elif row_salary < 0:
        reasons.append("Negative salary")

    return "; ".join(reasons)


invalid_employees["rejection_reason"] = invalid_employees.apply(
    rejection_reason, axis=1
)

# MAP: Convert source fields into target fields
mapped_employees = pd.DataFrame({
    "employee_id": valid_employees["EMP_ID"].values,
    "employee_name": valid_employees["EMP_NAME"].values,
    "department": valid_employees["DEPARTMENT"].values,
    "annual_salary": pd.to_numeric(
        valid_employees["ANNUAL_PAY"]
    ).values
})

# TRANSFORM: Calculate monthly salary
mapped_employees["monthly_salary"] = (
    mapped_employees["annual_salary"] / 12
).round(2)

# LOAD: Export results to CSV files
mapped_employees.to_csv(
    OUTPUT_DIR / "valid_employees.csv", index=False
)

invalid_employees.to_csv(
    OUTPUT_DIR / "invalid_employees.csv", index=False
)

# RECONCILIATION: Check all source records are accounted for
source_count = len(employees)
valid_count = len(mapped_employees)
invalid_count = len(invalid_employees)

assert source_count == valid_count + invalid_count, (
    "Reconciliation failed: record counts do not match"
)

# Generate data quality report
report = pd.DataFrame([{
    "total_records": source_count,
    "valid_records": valid_count,
    "invalid_records": invalid_count,
    "validation_pass_rate": round(
        valid_count / source_count * 100, 2
    ) if source_count else 0
}])

report.to_csv(OUTPUT_DIR / "data_quality_report.csv", index=False)

print(f"Valid records: {valid_count}")
print(f"Invalid records: {invalid_count}")
print(f"Validation pass rate: {report.iloc[0]['validation_pass_rate']}%")
print("Reconciliation: PASSED")
print("Output files generated successfully!")