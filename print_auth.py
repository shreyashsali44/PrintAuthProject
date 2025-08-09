import sqlite3
from datetime import datetime
from PyPDF2 import PdfReader
import win32api
import win32print
import os

DB_PATH = 'print_auth.db'

def authenticate(emp_id, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT password FROM employees WHERE emp_id = ?', (emp_id,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == password:
        return True
    return False

def count_pdf_pages(pdf_path):
    reader = PdfReader(pdf_path)
    return len(reader.pages)

def log_print_job(emp_id, doc_name, pages):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO print_logs (emp_id, doc_name, pages, print_time) 
        VALUES (?, ?, ?, ?)
    ''', (emp_id, doc_name, pages, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def send_to_printer(pdf_path):
    printer_name = win32print.GetDefaultPrinter()
    print(f"Sending to printer: {printer_name}")
    try:
        win32api.ShellExecute(
            0,
            "print",
            pdf_path,
            f'/d:"{printer_name}"',
            ".",
            0
        )
    except Exception as e:
        print(f"ShellExecute print failed: {e}")
        print("Trying os.startfile print...")

        try:
            os.startfile(pdf_path, "print")
        except Exception as e2:
            print(f"os.startfile print failed: {e2}")

def main():
    pdf_path = input("Enter path of PDF to print: ").strip()
    if not os.path.isfile(pdf_path):
        print("File does not exist.")
        return

    emp_id = input("Enter Employee ID: ").strip()
    password = input("Enter Password: ").strip()

    if not authenticate(emp_id, password):
        print("Authentication failed! Print canceled.")
        return

    pages = count_pdf_pages(pdf_path)
    print(f"Number of pages in document: {pages}")

    log_print_job(emp_id, os.path.basename(pdf_path), pages)
    print(f"Print job logged for employee {emp_id}.")

    send_to_printer(pdf_path)
    print("Document sent to printer (or attempted).")

if __name__ == "__main__":
    main()
