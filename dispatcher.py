from extractor_1 import extract_invoice_type_1
from extractor_2 import extract_invoice_type_2

import pdfplumber

def select_extractor(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        first_page_text = pdf.pages[0].extract_text() or ""

    if "東京材料株式会社" in first_page_text:
        return extract_invoice_type_1
    elif "三井物産プラスチック株式会社" in first_page_text:
        return extract_invoice_type_2
    else:
        raise ValueError("❌ No extractor matched the content of the PDF.")
