from typing import List, Dict
from collections import defaultdict

def prioritize_chunks(results: List[Dict], top_k_per_pdf: int = 3) -> Dict[str, List[Dict]]:
    """Group chunks by PDF and return top-K scored chunks per PDF"""
    grouped: Dict[str, List[Dict]] = defaultdict(list)

    # Group by PDF name
    for res in results:
        grouped[res["pdf_name"]].append(res)

    # Sort within each PDF and take top-K
    top_chunks_by_pdf = {}
    for pdf_name, chunks in grouped.items():
        sorted_chunks = sorted(chunks, key=lambda c: c["score"], reverse=True)
        top_chunks_by_pdf[pdf_name] = sorted_chunks[:top_k_per_pdf]

    return top_chunks_by_pdf
