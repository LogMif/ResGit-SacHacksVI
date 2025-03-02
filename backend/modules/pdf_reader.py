import PyPDF2
from io import BytesIO

def extract_text_from_pdf(pdf_binary):
    if pdf_binary == None:
        return ""
    
    # Create a PDF file reader object
    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_binary))
    
    # Initialize a variable to store the extracted text
    extracted_text = ""
    
    # Iterate through all the pages and extract text
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        extracted_text += page.extract_text()
    
    return extracted_text

if __name__ == "__main__":
    with open("resume.pdf", 'rb') as file:
        pdf_binary = file.read()

    print(extract_text_from_pdf(pdf_binary))