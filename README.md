<<<<<<< HEAD
# PrintAuthProject
A Flask web app that requires employee login before printing PDF, DOCX, or PPTX files. Tracks page counts and logs print history by employee with timestamps. Sends authenticated print jobs to the connected physical printer for secure and audited printing.
=======
# Print Authentication System

A Python Flask web application that requires employee login before allowing document printing (PDF, DOCX, PPTX). The app counts pages, logs print jobs with employee ID and timestamps, and sends authorized print jobs to a connected physical printer.

## Features

- Employee authentication for printing
- Supports PDF, Word (.docx), and PowerPoint (.pptx) files
- Counts number of pages/slides/paragraphs before printing
- Logs print history with employee ID, document name, pages printed, date and time
- View print history via a web interface

## Requirements

- Python 3.x
- Flask
- PyPDF2
- python-docx
- python-pptx
- pywin32 (for Windows printing)
- A physical printer connected to your machine (Windows OS)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/PrintAuthProject.git
   cd PrintAuthProject
Create and activate a virtual environment:

On Windows:

bash
Copy
Edit
python -m venv venv
venv\Scripts\activate
On macOS/Linux:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
Install the required packages:

bash
Copy
Edit
pip install -r requirements.txt
Run the application:

bash
Copy
Edit
python app.py
Open your browser and go to:

cpp
Copy
Edit
http://127.0.0.1:5000/
Usage
Login with your employee ID and password.

Upload a PDF, DOCX, or PPTX file to print.

After successful authentication, the document will be sent to the default printer.

View print job history on the history page.

Notes
Ensure your default printer is properly connected and installed.

This app works on Windows due to pywin32 dependency for printing.

Temporary files are deleted shortly after printing.

Page counts are approximated for DOCX and PPTX files based on paragraphs and slides.

License
This project is licensed under the MIT License.
>>>>>>> 959d9b1 (Initial commit - Print Authentication System)
