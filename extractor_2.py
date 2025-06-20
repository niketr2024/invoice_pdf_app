# used to open and read texts from pdf
import pdfplumber
import pandas as pd

def extract_invoice_type_2(pdf_path):
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            #breaks pages into lines
            lines = text.split('\n')
            for line in lines:
                parts = line.strip().split()
                #find position of numbers
                price_indexes = [i for i, p in enumerate(parts) if p.replace(',', '').replace('.', '').isdigit()]
                if len(parts) >= 2 and len(price_indexes) >= 1:
                    try:
                        new_price = parts[price_indexes[-1]]
                        old_price = parts[price_indexes[-2]] if len(price_indexes) >= 2 else ""
                        remarks = " ".join(parts[price_indexes[-1] + 1:]) if price_indexes[-1] + 1 < len(parts) else ""
                        product_name = " ".join(parts[:price_indexes[0]])
                        entry = {
                            "品目名": product_name,
                            "旧単価": old_price,
                            "新単価": new_price,
                            "備考": remarks
                        }
                        rows.append(entry)
                    except:
                        pass

    # create dataframe
    df = pd.DataFrame(rows)
    return df[['備考', '新単価']]
