<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Make the Readme Visuallly Appealing!

and the Project has 2 parts

- so treat it like one only !
make it Easy to understand
And Clearly DEfines the Logic and Flow first !


# \#  Document Hierarchical Classification

## Overview

This project provides a pipeline for analyzing and classifying the hierarchical structure of documents (such as research papers or reports) using both statistical and semantic methods. It leverages font size, text length, and semantic similarity (via transformer-based embeddings) to identify and organize document headings (Title, H1, H2, H3) and content.

The solution is designed to process extracted document data, classify headings, and generate a structured outline in JSON format.

---

## Features

- **Text Length Analysis:** Groups document lines and selects relevant groups based on average text length.
- **Semantic Classification:** Uses transformer embeddings to classify lines into Title, H1, H2, H3, or Content.
- **Font Size Weighting:** Incorporates font size statistics to improve heading detection.
- **Hierarchical Mapping:** Dynamically assigns heading levels based on font size and semantic similarity.
- **JSON Output:** Produces a structured outline with heading levels and page numbers.

---

## Project Structure

- `src/sanitization.py`: Analyzes text lengths in document groups and selects groups for further processing.
- `src/classify.py`: Classifies document lines into hierarchical headings using semantic similarity and font size logic.
- `all-MiniLM-L12-v2/config.json`: Configuration for the transformer model used for semantic embedding.
- `classified_document.json`: Output file containing the final structured outline.

---

## Logic \& Workflow

1. **Text Group Analysis (`sanitization.py`):**
    - Loads document data (groups of lines).
    - Computes average text length per group and overall.
    - Selects groups where the overall average text length exceeds the group's average.
2. **Hierarchical Classification (`classify.py`):**
    - Loads a transformer model (`all-MiniLM-L12-v2`).
    - Loads or simulates heading embeddings for Title, H1, H2, H3.
    - For each selected group:
        - Classifies each line by semantic similarity to heading embeddings.
        - Applies font size weighting to boost heading detection.
        - Assigns a heading level (Title, H1, H2, H3, Content).
    - Identifies the title group using font size and average character length.
    - Dynamically maps font sizes to heading levels for remaining groups.
    - Outputs a hierarchical outline sorted by page number.

---

## Parameters \& Configuration

- **Model Path:** Path to the transformer model (`all-MiniLM-L12-v2`).
- **Embeddings Directory:** Subdirectories (`title`, `h1`, `h2`, `h3`) containing `.pt` files for heading embeddings.
- **Classification Threshold:** Minimum semantic similarity score to assign a heading level (default: 0.4).
- **Font Size Weighting:** Logic to boost heading detection based on font size statistics.
- **Input Data:** JSON structure with groups, lines, font sizes, and text.
- **Output File:** Name of the JSON file to save the classified outline.

---

## Usage

1. **Prepare Input Data:**
    - Ensure your document data is structured as groups with lines, font sizes, and text.
2. **Run Text Length Analysis:**
```bash
python src/sanitization.py
```

    - (Modify to load your JSON file as needed.)
    3. **Run Hierarchical Classification:**
```bash
python src/classify.py
```

    - Outputs `classified_document.json` with the document outline.
    
---

## Output Example

```json
{
  "title": "A Cyber Bridge Experiment",
  "outline": [
    { "level": "H1", "text": "I. INTRODUCTION", "page": 0 },
    { "level": "H1", "text": "II. BACKGROUND", "page": 0 },
    { "level": "H1", "text": "III. RELATED WORKS", "page": 1 },
    ...
  ]
}
```


---

## Requirements

- Python 3.8+
- `sentence-transformers`
- `torch`
- `numpy`
- `pandas`

---

## Customization

- Adjust the classification threshold or font size logic in `classify.py` for different document types.
- Replace simulated heading embeddings with your own `.pt` files for improved accuracy.

---

## Context

This project was developed for the Adobe India Hackathon 2025 to automate document structure extraction, enabling downstream tasks such as summarization, navigation, and semantic search.

---

## License

This project is for hackathon/demo purposes. Please review and adapt for production use as needed.

This is a Readme

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
2. **PDF Parsing \& Chunking:**
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

## File \& Module Structure

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

## Customization \& Extensibility

- **LLM Model:** You can swap out TinyLlama for another model in `llm_generator.py`.
- **Embeddings:** The embedder can be replaced or upgraded for better semantic understanding.
- **Chunking Strategy:** Adjust chunk size or overlap in `chunk_text.py` for different granularity.

---

## Notes

- The system is designed for efficiency and modularity, making it easy to adapt for other document QA tasks.
- Ensure all PDFs are text-based or OCR-processed for best results.

---

## Authors \& Credits

- Developed for research and academic purposes.
- Team Segfault

this is the second readme
without including any reference of the Adobe India Hackathon
Create a Summarized Readme In Visulally appealing way -
Which is Really simple to understand
And Shows the Flow and all of the Logic of the Solution presented

Of course. Here is a summarized and visually organized README that combines the logic and workflow of both projects into a single, easy-to-understand system.

# Semantic Document Analysis \& QA System

This system analyzes a collection of documents to first understand their hierarchical structure and then perform automated question-answering based on a specific task. It combines semantic analysis with a lightweight LLM to extract, structure, and synthesize information into concise, relevant answers.

### Key Features

* **Hierarchical Structuring:** Automatically identifies the document's outline (Title, Headings, Content) by analyzing font styles, text length, and semantic context.
* **Automated Question Answering:** Processes a collection of documents to find the most relevant information that answers a user-defined task or question.
* **Semantic Search:** Goes beyond simple keywords by using transformer-based embeddings to understand the meaning behind the user's query and the document content.
* **Persona-Aware Summaries:** Generates answers tailored to a specific role or style (e.g., "summarize as a financial analyst").
* **Structured JSON Output:** Produces a clean, machine-readable output containing the document's detected outline and the generated answer.


### How It Works: The Workflow

The system follows a multi-stage pipeline to process documents from start to finish.

1. **➡️ Input:** The process begins with a collection of documents (e.g., PDFs) and a defined task, such as "Find the key methodologies used in these research papers."
2. **📄 Document Structuring:** Each document is analyzed to identify its structure.
    * It uses font size, text length, and semantic similarity to classify each line as a **Title**, **H1**, **H2**, **H3**, or **Content**.
    * This creates a hierarchical map or outline of the document.
3. **🧩 Chunking \& Embedding:** The structured content is broken down into smaller, meaningful text chunks.
    * Each chunk is then converted into a numerical vector (embedding) using a transformer model like `all-MiniLM-L12-v2`.
4. **🔍 Semantic Search \& Prioritization:**
    * The user's task is also converted into an embedding.
    * The system performs a vector search to find the most semantically relevant text chunks from across all documents.
    * The top N chunks are selected to serve as the context for the final answer.
5. **💡 Answer Generation:**
    * A lightweight Large Language Model (like TinyLlama) takes the user's task and the most relevant chunks as input.
    * It synthesizes this information to generate a concise, context-aware answer in the specified persona.
6. **⬅️ Output:** The final result is saved as a single JSON file containing both the structured outline of the document and the generated answer to the task.

### Project Structure

The codebase is organized into modular components for clarity and maintainability.

* `app.py`: The main script that orchestrates the entire workflow.
* `/input`: The directory where you place your document collections and task descriptions.
* `/output`: The directory where the final JSON results are saved.
* `/src`: Contains the core logic for each step of the pipeline.
    * `document_parser.py`: Handles PDF parsing and hierarchical structure analysis.
    * `qa_engine.py`: Manages text chunking, embedding, semantic search, and LLM-based answer generation.
    * `utils.py`: Contains helper functions and configurations.
* `/models`: Directory to store the transformer and language models.


### How to Use

1. **Setup:** Install the required Python packages.
```bash
pip install -r requirements.txt
```

2. **Prepare Data:** Place your document collections and a JSON file defining your task inside the `/input` directory.
3. **Run:** Execute the main application script.
```bash
python app.py
```


### Example Output

The system generates a structured JSON file that combines the document's outline with the final answer.

```json
{
  "task": "Find the key methodologies used in this research",
  "generated_answer": "The primary methodology identified is the Cyber Bridge Experiment, which involves...",
  "document_outline": {
    "title": "A Cyber Bridge Experiment",
    "structure": [
      { "level": "H1", "text": "I. INTRODUCTION", "page": 0 },
      { "level": "H1", "text": "II. BACKGROUND", "page": 0 },
      { "level": "H2", "text": "2.1 Related Works", "page": 1 }
    ]
  },
  "relevant_chunks": [
    { "text": "Our experiment, the Cyber Bridge, was designed to...", "page": 3},
    { "text": "The background for this methodology is based on...", "page": 1}
  ]
}
```


### Requirements

* Python 3.8+
* `torch`
* `sentence-transformers`
* `numpy`
* `pandas`
* `PyPDF2` (or another PDF parsing library)

Of course! Here is a visually appealing, simplified, and unified README that clearly explains the logic and flow of your project.

# 🧠 Semantic Document Analysis \& QA System 🤖

This advanced system analyzes any document collection to first understand its structure and then intelligently answer questions about its content. It combines statistical analysis with modern AI to turn unstructured documents into organized, queryable knowledge.

***

### ✨ Key Features

* **Hierarchical Structuring:** Automatically identifies the document's outline (Title, Headings, Content) by analyzing font styles, text length, and semantic context.
* **Automated Question Answering:** Processes a collection of PDFs to find the most relevant information that answers a user-defined task or question.
* **Deep Semantic Search:** Goes beyond simple keywords by using transformer-based embeddings to understand the *meaning* behind your query and the document content.
* **Persona-Aware Summaries:** Generates answers tailored to a specific role or style (e.g., "summarize as a financial analyst").
* **Structured JSON Output:** Produces a clean, machine-readable JSON file containing the document's detected outline and the generated answer, ready for any downstream application.

***

### 🚀 How It Works: The End-to-End Workflow

The system follows a sophisticated multi-stage pipeline to process documents from start to finish.

**1. ➡️ Input: The Task**
The process begins with a collection of documents (e.g., PDFs) and a defined task, such as *"Find the key methodologies used in these research papers."*

**2. 📄 Document Structuring: Understanding the Layout**
Each document is automatically analyzed to reverse-engineer its structure.

* It uses font size, text length, and semantic similarity to classify each line as a **Title**, **H1**, **H2**, **H3**, or **Content**.
* This creates a hierarchical map or a "table of contents" for the document.

**3. 🧩 Chunking \& Embedding: Making Sense of the Content**
The structured content is broken down into smaller, meaningful text chunks.

* Each chunk is then converted into a numerical vector (an "embedding") using a powerful transformer model like `all-MiniLM-L12-v2`. This captures its semantic meaning.

**4. 🔍 Semantic Search \& Prioritization: Finding the Gold**

* Your task or question is also converted into an embedding.
* The system performs a high-speed vector search to find the most semantically similar text chunks from across all documents.
* The top N most relevant chunks are selected to serve as the core context for the final answer.

**5. 💡 Answer Generation: Synthesizing the Knowledge**

* A lightweight but powerful Large Language Model (like TinyLlama) takes your task and the most relevant chunks as input.
* It synthesizes this information to generate a concise, context-aware, and persona-driven answer.

**6. ⬅️ Output: The Structured Result**
The final result is neatly packaged into a single JSON file containing both the structured outline of the document and the intelligently generated answer to your task.

***

### 📂 Project Structure

The codebase is organized into modular components for clarity, maintainability, and easy extension.

* `app.py`: The main script that orchestrates the entire workflow.
* `/input`: The directory where you place your document collections and task descriptions.
* `/output`: The directory where the final JSON results are saved.
* `/scripts`: Contains the core logic for each step of the pipeline.
    * `document_parser.py`: Handles PDF parsing and hierarchical structure analysis.
    * `qa_engine.py`: Manages text chunking, embedding, semantic search, and LLM-based answer generation.
    * `utils.py`: Contains helper functions and configurations.
* `/models`: Directory to store the transformer and language models.

***

### 🛠️ How to Use

**1. Setup:** Install the required Python packages.

```bash
pip install -r requirements.txt
```

**2. Prepare Data:** Place your document collections and a JSON file defining your task inside the `/input` directory.

**3. Run:** Execute the main application script.

```bash
python app.py
```


***

### 📊 Example Output

The system generates a structured JSON file that combines the document's outline with the final answer.

```json
{
  "task": "Find the key methodologies used in this research",
  "generated_answer": "The primary methodology identified is the Cyber Bridge Experiment, which involves a multi-stage process of data collection and analysis to evaluate network security protocols.",
  "document_outline": {
    "title": "A Cyber Bridge Experiment",
    "structure": [
      { "level": "H1", "text": "I. INTRODUCTION", "page": 0 },
      { "level": "H1", "text": "II. BACKGROUND", "page": 0 },
      { "level": "H2", "text": "2.1 Related Works", "page": 1 }
    ]
  },
  "relevant_chunks": [
    { "text": "Our experiment, the Cyber Bridge, was designed to test vulnerabilities...", "page": 3},
    { "text": "The background for this methodology is based on prior research in network analysis...", "page": 1}
  ]
}
```


***

### ✅ Requirements

* Python 3.8+
* `torch`
* `sentence-transformers`
* `numpy`
* `pandas`
* `PyPDF2` (or another PDF parsing library)

