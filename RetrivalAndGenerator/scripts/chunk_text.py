from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict

# Set your desired chunk configuration
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=768,
    chunk_overlap=100,
    separators=["\n\n", "\n", ".", "?", "!", ""]
)

def chunk_pdf_pages(pages: List[Dict]) -> List[Dict]:
    """Chunk each page text into overlapping semantic units"""
    chunks = []
    for page in pages:
        splits = text_splitter.split_text(page["text"])
        for i, chunk in enumerate(splits):
            chunks.append({
                "pdf_name": page["pdf_name"],
                "page_number": page["page_number"],
                "chunk_index": i,
                "chunk_text": chunk
            })
    return chunks
