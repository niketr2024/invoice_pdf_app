import gradio as gr
import pandas as pd
import tempfile
from dispatcher import select_extractor

def process_multiple_invoice(files):
    all_rows = []

    try:
        # runs the appropriate extractor based on the invoice from dispatcher.py
        for tmp_path in files:
            extractor = select_extractor(tmp_path)
            df = extractor(tmp_path)
            all_rows.append(df)

        # combines results
        combined_df = pd.concat(all_rows, ignore_index=True)

        # converts to Excel file and saves path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_excel:
            excel_path = tmp_excel.name
            combined_df.to_excel(excel_path, index=False)

        return combined_df, excel_path


    except Exception as e:
        print(f"Error: {e}")
        empty_df = pd.DataFrame(columns=["備考", "新単価"])
        return empty_df, None

# app interface
iface = gr.Interface(
    fn=process_multiple_invoice,
    inputs=gr.File(label="Upload Multiple Invoice PDF", type="filepath", file_types=['.pdf'], file_count="multiple"),
    outputs=[
        gr.Dataframe(label="Combined Extracted Table"),
        gr.File(label="Download Combined Excel")
    ],
    title="Multi Invoice PDF Extractor",
    description="Upload multiple PDFs from 東京材料株式会社 or 三井物産プラスチック株式会社"
)


if __name__ == "__main__":
    iface.launch()

