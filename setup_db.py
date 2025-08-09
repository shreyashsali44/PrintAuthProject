import sqlite3
from datetime import datetime

# Connect (or create) database
conn = sqlite3.connect('print_auth.db')
c = conn.cursor()

# Create employees table
c.execute('''
CREATE TABLE IF NOT EXISTS employees (
    emp_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    department TEXT
)
''')

# Create print_logs table
c.execute('''
CREATE TABLE IF NOT EXISTS print_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_id TEXT NOT NULL,
    doc_name TEXT NOT NULL,
    pages INTEGER NOT NULL,
    print_time TEXT NOT NULL,
    FOREIGN KEY(emp_id) REFERENCES employees(emp_id)
)
''')

# Insert 10 sample employees (replace passwords as needed)
employees = [
    ('E001', 'John Smith', 'pass123', 'HR'),
    ('E002', 'Alice Brown', 'alice@12', 'IT'),
    ('E003', 'Bob Johnson', 'bobpass', 'Finance'),
    ('E004', 'Clara Davis', 'clara456', 'Marketing'),
    ('E005', 'David Lee', 'david789', 'Operations'),
    ('E006', 'Eva Green', 'eva321', 'Sales'),
    ('E007', 'Frank Moore', 'frank111', 'IT'),
    ('E008', 'Grace Hall', 'grace222', 'HR'),
    ('E009', 'Hank Adams', 'hank333', 'Finance'),
    ('E010', 'Ivy Scott', 'ivy444', 'Marketing')
]

# Insert employees if not exists
for emp in employees:
    c.execute('''
    INSERT OR IGNORE INTO employees (emp_id, name, password, department) VALUES (?, ?, ?, ?)
    ''', emp)

conn.commit()
print("Database and employees table created with sample data.")
conn.close()
