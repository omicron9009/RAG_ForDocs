from pathlib import Path

# Step modules
from scripts.input_loader import traverse_and_load_inputs
from scripts.parse_pdf import parse_pdf_to_pages
from scripts.chunk_text import chunk_pdf_pages
from scripts.embedder import MiniLMEmbedder
from scripts.searcher import SemanticSearcher
from scripts.prioritizer import prioritize_chunks
from scripts.llm_generator import TinyLlamaGenerator
from scripts.output_formatter import write_output_json
job_to_be_done=None
def process_single_collection(collection_dir: Path, input_json: dict, pdf_paths: list[Path]):
    print(f"\n🔍 Processing: {collection_dir.name}")

    # 1. Parse & Chunk
    all_chunks = []
    for pdf_path in pdf_paths:
        print(pdf_path)
        pages = parse_pdf_to_pages(pdf_path)
        chunks = chunk_pdf_pages(pages)
        all_chunks.extend(chunks)
    print(f"🔹 Total parsed chunks: {len(all_chunks)}")
    # 2. Embed Chunks
    embedder = MiniLMEmbedder()
    embedded_chunks = embedder.embed_chunks(all_chunks)

    # 3. Semantic Search
    searcher = SemanticSearcher(embedded_chunks)
    query = input_json["job_to_be_done"]["task"]
    # job_to_be_done=query
    raw_results = searcher.search(query, top_k=25)  # expand for more coverage

    # 4. Prioritize per PDF
    top_chunks = prioritize_chunks(raw_results, top_k_per_pdf=3)

    # 5. Generate Answer using LLM
    llama = TinyLlamaGenerator()
    role = input_json["persona"]["role"]

    refined_outputs = {
        pdf_name: llama.generate_response(
            role=role,
            task=query,
            chunks=chunks
        )
        for pdf_name, chunks in top_chunks.items()
    }

    # 6. Save Final Output
    write_output_json(
        collection_dir=collection_dir,
        metadata={
        **input_json["challenge_info"],
        **input_json["job_to_be_done"],
        **input_json["persona"]
    },
        top_chunks=top_chunks,
        refined_outputs=refined_outputs
    )

def main():
    print("📂 Scanning input directory...\n")
    collections = traverse_and_load_inputs()

    for collection_dir, input_json, pdf_paths in collections:
        print(pdf_paths)
        process_single_collection(collection_dir, input_json, pdf_paths)

    print("\n✅ All collections processed!")

if __name__ == "__main__":
    main()
