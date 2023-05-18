import PyPDF2

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        text = ''

        for page in range(num_pages):
            pdf_page = pdf_reader.pages[page]
            text += pdf_page.extract_text()

        return text

# Usage example
pdf_file = 'testDrawing.pdf'
extracted_text = extract_text_from_pdf(pdf_file)
print(extracted_text)
