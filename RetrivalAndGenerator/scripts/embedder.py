from typing import List, Dict
from sentence_transformers import SentenceTransformer
import numpy as np

class MiniLMEmbedder:
    def __init__(self, model_path: str = "./models/all-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_path)

    def embed_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """Embed each chunk's text and return with vector"""
        texts = [c["chunk_text"] for c in chunks]
        embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        results = []
        for chunk, vector in zip(chunks, embeddings):
            chunk_with_embedding = dict(chunk)  # clone
            chunk_with_embedding["embedding"] = vector.tolist()  # for JSON serializability
            results.append(chunk_with_embedding)
        return results
