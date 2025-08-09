import sqlite3

conn = sqlite3.connect('print_auth.db')
c = conn.cursor()

c.execute("PRAGMA table_info(print_logs);")
columns = c.fetchall()

print("Columns in print_logs table:")
for col in columns:
    print(col)

conn.close()
