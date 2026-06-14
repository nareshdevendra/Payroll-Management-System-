import pandas as pd
import psycopg2

# Connect PostgreSQL
conn = psycopg2.connect(
    database="payroll_db",
    user="postgres",
    password="Naresh6602",
    host="localhost",
    port="5432"
)

print("Connected Successfully ✅")

# Fetch data
query = "SELECT * FROM payroll"
df = pd.read_sql(query, conn)

print(df.head())

# Recalculate salary (validation)
df["gross_salary_check"] = df["basic_salary"] + df["hra"] + df["other_allowance"]
df["tax_amount_check"] = df["gross_salary_check"] * df["tax_percent"] / 100
df["net_salary_check"] = df["gross_salary_check"] - df["tax_amount_check"] - df["deductions"]

print(df[["employee_id", "net_salary", "net_salary_check"]].head())

import os

os.makedirs("C:/Excel/Payroll_Project/output/payslips", exist_ok=True)
os.makedirs("C:/Excel/Payroll_Project/output/reports", exist_ok=True)

for index, row in df.iterrows():
    file_path = f"C:/Excel/Payroll_Project/output/payslips/Payslip_{row['employee_id']}.txt"
    
    with open(file_path, "w") as f:
        f.write(f"""
===== EMPLOYEE PAYSLIP =====

Employee ID: {row['employee_id']}
Name: {row['name']}
Department: {row['department']}

----- Earnings -----
Basic Salary: {row['basic_salary']}
HRA: {row['hra']}
Other Allowance: {row['other_allowance']}

----- Deductions -----
Tax: {row['tax_amount']}
Other Deductions: {row['deductions']}

----- Summary -----
Gross Salary: {row['gross_salary']}
Net Salary: {row['net_salary']}

============================
""")

print("✅ Payslips generated successfully!")

df.to_csv("C:/Excel/Payroll_Project/output/reports/full_payroll_report.csv", index=False)

dept_report = df.groupby("department")[["gross_salary", "net_salary"]].sum().reset_index()
dept_report.to_csv("C:/Excel/Payroll_Project/output/reports/department_report.csv", index=False)

tax_report = df[["employee_id", "tax_amount"]]
tax_report.to_csv("C:/Excel/Payroll_Project/output/reports/tax_report.csv", index=False)

summary = pd.DataFrame({
    "Total Employees": [len(df)],
    "Total Gross Salary": [df["gross_salary"].sum()],
    "Total Net Salary": [df["net_salary"].sum()],
    "Total Tax": [df["tax_amount"].sum()]
})

summary.to_csv("C:/Excel/Payroll_Project/output/reports/summary_report.csv", index=False)
