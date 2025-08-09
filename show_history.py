import sqlite3

conn = sqlite3.connect('print_auth.db')
c = conn.cursor()

c.execute('SELECT * FROM print_logs ORDER BY print_time DESC')
rows = c.fetchall()

print("Print History:")
print("Log ID | Employee ID | Document Name | Pages | Print Time")
print("-"*60)
for row in rows:
    print(f"{row[0]:6} | {row[1]:11} | {row[2]:13} | {row[3]:5} | {row[4]}")

conn.close()
