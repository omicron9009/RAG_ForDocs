import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer

class SemanticSearcher:
    def __init__(self, embedded_chunks: List[Dict], model_path: str = "./models/all-MiniLM-L12-v2"):
        self.embedded_chunks = embedded_chunks
        self.model = SentenceTransformer(model_path)

        # Build embedding matrix
        self.embedding_matrix = np.array([chunk["embedding"] for chunk in embedded_chunks])

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for the most relevant chunks for a query"""
        query_vec = self.model.encode([query], convert_to_numpy=True)[0]

        # Cosine similarity
        dot_product = np.dot(self.embedding_matrix, query_vec)
        norm_product = np.linalg.norm(self.embedding_matrix, axis=1) * np.linalg.norm(query_vec)
        scores = dot_product / norm_product

        top_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for idx in top_indices:
            chunk = self.embedded_chunks[idx]
            results.append({
                "score": float(scores[idx]),
                "pdf_name": chunk["pdf_name"],
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"],
                "chunk_text": chunk["chunk_text"]
            })
        return results
