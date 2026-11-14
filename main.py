employees = [
    {"EMP_ID": 101, "EMP_NAME": "Prem", "ANNUAL_PAY": 60000},
    {"EMP_ID": 102, "EMP_NAME": "Priya", "ANNUAL_PAY": None},
    {"EMP_ID": 103, "EMP_NAME": "Rahul", "ANNUAL_PAY": -5000},
    {"EMP_ID": 104, "ANNUAL_PAY": 72000},
    {"EMP_ID": 105, "EMP_NAME": "Kiran", "ANNUAL_PAY": 0},
    {"EMP_ID": 106, "EMP_NAME": "Divya", "ANNUAL_PAY": 84000}
]

valid_employees = []
invalid_employees = []

for employee in employees:
    name = employee.get("EMP_NAME")
    salary = employee.get("ANNUAL_PAY")

    if name is None or salary is None:
        invalid_employees.append(employee)
    elif salary < 0:
        invalid_employees.append(employee)
    else:
        valid_employees.append(employee)

print("Valid:", valid_employees)
print("Invalid:", invalid_employees) 

print("Valid Num:", len(valid_employees))
print("Invalid Num:", len(invalid_employees))
    