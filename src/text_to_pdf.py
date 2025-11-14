from fpdf import FPDF
import os

def text_to_pdf(input_txt_path, output_pdf_path):
    if not os.path.exists(input_txt_path):
        print("❌ Transcript file not found!")
        return
    
    with open(input_txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in lines:
        pdf.multi_cell(0, 10, line)

    pdf.output(output_pdf_path)
    print(f"✅ PDF saved to: {output_pdf_path}")
