import gradio as gr
import pandas as pd
import tempfile
from dispatcher import select_extractor

def process_invoice(file):
    try:
        # file is a bytes object, no need to call .read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file)
            tmp_path = tmp.name

        #retreives appropriate extractor from dispatcher.py
        extractor = select_extractor(tmp_path)
        #runs the appropriate extractor ( 1 or 2)
        df = extractor(tmp_path)

        #converts extracted file to xlsx and saves it as excel file
        excel_path = tmp_path.replace(".pdf", ".xlsx")
        df.to_excel(excel_path, index=False)

        return df, excel_path

    except Exception as e:
        print(f"Error: {e}")
        empty_df = pd.DataFrame(columns=["備考", "新単価"])
        return empty_df, None

iface = gr.Interface(
    fn=process_invoice,
    inputs=gr.File(label="Upload Invoice PDF", type="binary"),  # this returns file-like object
    outputs=[
        gr.Dataframe(label="Extracted Table"),
        gr.File(label="Download Excel")
    ],
    title="Invoice PDF Extractor",
    description="Upload a PDF from 東京材料株式会社 or 三井物産プラスチック株式会社"
)

# if running script directly, start app in browser
if __name__ == "__main__":
    iface.launch()

