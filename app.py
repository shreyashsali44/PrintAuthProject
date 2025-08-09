from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import os
import tempfile
import time
from PyPDF2 import PdfReader
from docx import Document
from pptx import Presentation
import win32api
import win32print

app = Flask(__name__)
DB_PATH = 'print_auth.db'

# --- Authentication ---
def authenticate(emp_id, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT password FROM employees WHERE emp_id = ?', (emp_id,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == password:
        return True
    return False

# --- Count pages for different file types ---
def count_pages(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        reader = PdfReader(file_path)
        return len(reader.pages)
    elif ext == '.docx':
        doc = Document(file_path)
        # Approximate pages by paragraphs count
        return len(doc.paragraphs)
    elif ext == '.pptx':
        prs = Presentation(file_path)
        return len(prs.slides)
    else:
        return 0  # unsupported

# --- Log print job ---
def log_print_job(emp_id, doc_name, pages):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO print_logs (emp_id, doc_name, pages, print_time) 
        VALUES (?, ?, ?, ?)
    ''', (emp_id, doc_name, pages, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

# --- Send to printer (updated for debugging) ---
def send_to_printer(file_path):
    printer_name = win32print.GetDefaultPrinter()
    print(f"Sending to printer: {printer_name}")
    try:
        ret = win32api.ShellExecute(
            0,
            "print",
            file_path,
            f'/d:"{printer_name}"',
            ".",
            0
        )
        print(f"ShellExecute returned: {ret}")
    except Exception as e:
        print(f"Printing failed: {e}")

# --- Routes ---

@app.route('/', methods=['GET'])
def login_form():
    return render_template('login.html')

@app.route('/print', methods=['POST'])
def print_document():
    emp_id = request.form.get('emp_id')
    password = request.form.get('password')
    uploaded_file = request.files.get('pdf_file')

    if not (emp_id and password and uploaded_file):
        return render_template('login.html', error="Please fill all fields and upload a file.")

    if not authenticate(emp_id, password):
        return render_template('login.html', error="Invalid Employee ID or Password.")

    # Save uploaded file temporarily
    ext = os.path.splitext(uploaded_file.filename)[1].lower()
    if ext not in ['.pdf', '.docx', '.pptx']:
        return render_template('login.html', error="Unsupported file type! Only PDF, DOCX, PPTX allowed.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        temp_path = tmp.name
        uploaded_file.save(temp_path)

    try:
        pages = count_pages(temp_path)
        log_print_job(emp_id, uploaded_file.filename, pages)
        send_to_printer(temp_path)

        time.sleep(5)  # <-- Wait 5 seconds so printer app can open the file before deletion

    except Exception as e:
        os.unlink(temp_path)
        return render_template('dashboard.html', error=f"Error during printing: {e}")

    os.unlink(temp_path)
    return render_template('dashboard.html', success="Document sent to printer successfully.", doc_name=uploaded_file.filename, pages=pages)

@app.route('/history', methods=['GET'])
def view_history():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT log_id, emp_id, doc_name, pages, print_time 
        FROM print_logs 
        ORDER BY print_time DESC
        LIMIT 50
    ''')
    logs = c.fetchall()
    conn.close()
    return render_template('history.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True)
