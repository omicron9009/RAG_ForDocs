# Semantic PDF QA System for Research

## Overview
This project is a research-oriented system for automated question answering (QA) over collections of PDFs. It processes document collections to answer a specific 'job to be done' (task) for each set, using semantic search and a lightweight LLM (TinyLlama). The system extracts, chunks, embeds, searches, prioritizes, and summarizes content from the PDFs to generate concise, context-aware answers tailored to a given persona and task.

---

## Key Features
- **Automated PDF QA:** Given a set of PDFs and a task (e.g., "Find the best travel tips"), the system finds the most relevant information and generates a summarized answer for each PDF.
- **Semantic Understanding:** Uses embeddings and semantic search to go beyond keyword matching, understanding the context of the task and the content.
- **Persona-Aware Summaries:** Generates answers in the style or role specified (e.g., "as a travel guide").
- **Structured Output:** Produces a JSON output with metadata, top relevant chunks, and refined answers per PDF.

---

## System Workflow
### 1. Input Structure
- Each collection (e.g., `Collection 1/`) contains:
  - `challenge1b_input.json`: Specifies the task, persona, and collection info.
  - `PDFs/`: Folder with all relevant PDF files.

### 2. Processing Pipeline
1. **Input Loading:**
   - Scans the input directory for all collections and loads their input JSON and PDF paths.
2. **PDF Parsing & Chunking:**
   - Each PDF is parsed into pages, then split into smaller text chunks for finer-grained analysis.
3. **Embedding:**
   - Each chunk is embedded using a MiniLM-based embedder, converting text into semantic vectors.
4. **Semantic Search:**
   - For the given task, the system retrieves the most relevant chunks across all PDFs using vector similarity.
5. **Prioritization:**
   - Selects the top N chunks per PDF to ensure coverage and diversity.
6. **LLM Generation:**
   - Uses TinyLlama to generate a persona-aware answer for each PDF, based on the top chunks and the task.
7. **Output Formatting:**
   - Writes a structured JSON output with metadata, selected chunks, and generated answers.

---

## File & Module Structure
- `app.py`: Main entry point; orchestrates the pipeline.
- `scripts/`
  - `input_loader.py`: Loads collections, input JSON, and PDF paths.
  - `parse_pdf.py`: Extracts text from PDF pages.
  - `chunk_text.py`: Splits pages into manageable text chunks.
  - `embedder.py`: Embeds text chunks using MiniLM.
  - `searcher.py`: Performs semantic search over embedded chunks.
  - `prioritizer.py`: Picks top chunks per PDF.
  - `llm_generator.py`: Generates answers using TinyLlama.
  - `output_formatter.py`: Formats and writes the output JSON.

---

## How To Run
1. **Install Requirements:**
   - Ensure Python 3.8+ is installed.
   - Install dependencies (if any, e.g., PyPDF2, transformers, etc.).
     ```bash
     pip install -r requirements.txt
     ```
2. **Prepare Input:**
   - Place your collections in the `input/` directory, each with its own `challenge1b_input.json` and `PDFs/` folder.
3. **Run the Pipeline:**
   - Execute the main script:
     ```bash
     python app.py
     ```
   - Outputs will be saved as `my_challenge1b_output.json` in each collection folder.

---

## Customization & Extensibility
- **LLM Model:** You can swap out TinyLlama for another model in `llm_generator.py`.
- **Embeddings:** The embedder can be replaced or upgraded for better semantic understanding.
- **Chunking Strategy:** Adjust chunk size or overlap in `chunk_text.py` for different granularity.

---

## Notes
- The system is designed for efficiency and modularity, making it easy to adapt for other document QA tasks.
- Ensure all PDFs are text-based or OCR-processed for best results.

---

## Authors & Credits
- Developed for research and academic purposes.
- Team Segfault
