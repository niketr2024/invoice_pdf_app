import pdfplumber
import pandas as pd
import re

def extract_invoice_type_1(pdf_path):
    rows = []
    # open pdf
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')
            for line in lines:
                # pattern match with regular expressions
                match = re.search(r'(\d+\s*\w+)\s+(\w+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+(\w+)', line)
                if match:
                    parts = line.split()
                    item_name = " ".join(parts[0:len(parts)-7])
                    try:
                        entry = {
                            "品目名": item_name,
                            "入目": parts[-7],
                            "単位": parts[-6],
                            "旧単価": parts[-5],
                            "新単価": parts[-4],
                            "改定幅": parts[-3],
                            "通貨": parts[-2],
                            "備考": parts[-1] if len(parts) >= 8 else ""
                        }
                        rows.append(entry)
                    except IndexError:
                        pass
    # make into dataframe
    df = pd.DataFrame(rows)
    return df[['備考', '新単価']]

