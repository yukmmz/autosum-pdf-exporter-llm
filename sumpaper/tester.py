from pathlib import Path
import os

import summerize_paper_gemini as sp



def test_md2pdf_pdfkit():
    # filepath = "../data/markdown_text.md"
    filepath = "../BU/md_sample.md"
    with open(filepath, 'r', encoding='utf-8') as f:
        markdown_text = f.read()
    output_pdf_path = Path(filepath).parent / "markdown_output.pdf"
    sp.md2pdf_pdfkit(markdown_text, output_pdf_path, font_size=30)
    print(f"Generated PDF at: {output_pdf_path}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test_md2pdf_pdfkit()