import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict

def parse_pdf_to_pages(pdf_path: Path) -> List[Dict]:
    """Extract text from each page in the PDF"""
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        pages.append({
            "pdf_name": pdf_path.name,
            "page_number": i,
            "text": text.strip()
        })
    doc.close()
    return pages
