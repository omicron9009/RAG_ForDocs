import json
from pathlib import Path
from typing import List, Dict
from scripts.input_loader import INPUT_DOCUMENTS 
def write_output_json(
    collection_dir: Path,
    metadata: Dict,
    top_chunks: Dict[str, List[Dict]],
    refined_outputs: Dict[str, str]
):
    output_path = collection_dir / "challenge1b_output.json"

    extracted_sections = []
    subsection_analysis = []

    for pdf_name, chunks in top_chunks.items():
        for rank, chunk in enumerate(chunks, start=1):
            extracted_sections.append({
                "document": chunk["pdf_name"],
                "section_title": chunk.get("chunk_text", ""),  # Optional heuristic for title
                "importance_rank": rank,
                "page_number": chunk.get("page_number", -1)
            })

        if pdf_name in refined_outputs:
            # Find the most common page number among chunks for this doc
            page_numbers = [c.get("page_number") for c in chunks if "page_number" in c]
            main_page = max(set(page_numbers), key=page_numbers.count) if page_numbers else -1

            subsection_analysis.append({
                "document": pdf_name,
                "refined_text": refined_outputs[pdf_name],
                "page_number": main_page
            })

    output_json = {
        "metadata": {
            "input_documents": INPUT_DOCUMENTS,
            "persona": metadata.get("persona", ""),
            "job_to_be_done": metadata.get("job_to_be_done", ""),
            "processing_timestamp": metadata.get("processing_timestamp", "")
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_json, f, indent=2, ensure_ascii=False)

    print(f"✅ Output saved to {output_path}")

