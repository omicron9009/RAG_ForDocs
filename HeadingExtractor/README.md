#  Document Hierarchical Classification

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

## Logic & Workflow

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

## Parameters & Configuration

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

