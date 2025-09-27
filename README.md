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

