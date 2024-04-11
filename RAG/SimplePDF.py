from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import os

def extract_text_from_pdf(filename, page_numbers = None, min_line_length = 1):
    '''Read PDF（page No in page_numbers） and return a list of paragraphs.'''
    paragraphs = []
    buffer = ''
    full_text = ''
    for i, page_layout in enumerate(extract_pages(filename)):
        if page_numbers is not None and i not in page_numbers:
            continue
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                full_text += element.get_text() + '\n'
    lines = full_text.split('\n')
    for text in lines:
        if len(text) >= min_line_length:
            buffer += (' '+text) if not text.endswith('-') else text.strip('-')
        elif buffer:
            paragraphs.append(buffer)
            buffer = ''
    if buffer:
        paragraphs.append(buffer)
    return paragraphs

pdf_file = "RAG/Xi Wang Backend Engineer 2024.pdf"
if os.path.exists(pdf_file):
    paragraphs = extract_text_from_pdf(pdf_file, min_line_length=10)
else:
    print(f"Error: File '{pdf_file}' does not exist.")

for para in paragraphs[:3]:
    print(para+"\n")