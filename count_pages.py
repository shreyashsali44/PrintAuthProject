from PyPDF2 import PdfReader

def count_pdf_pages(file_path):
    reader = PdfReader(file_path)
    return len(reader.pages)

if __name__ == "__main__":
    pdf_file = input("Enter PDF file path: ")
    pages = count_pdf_pages(pdf_file)
    print(f"Number of pages: {pages}")
