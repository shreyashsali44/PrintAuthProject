import sqlite3

def authenticate(emp_id, password):
    conn = sqlite3.connect('print_auth.db')
    c = conn.cursor()
    c.execute('SELECT password FROM employees WHERE emp_id = ?', (emp_id,))
    row = c.fetchone()
    conn.close()
    if row:
        stored_password = row[0]
        return stored_password == password
    return False

if __name__ == "__main__":
    emp_id = input("Enter Employee ID: ")
    password = input("Enter Password: ")
    if authenticate(emp_id, password):
        print("Login successful")
    else:
        print("Invalid Employee ID or Password")
