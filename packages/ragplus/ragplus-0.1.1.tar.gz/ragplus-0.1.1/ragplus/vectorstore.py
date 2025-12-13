import numpy as np
import pickle
import os
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


def cosine(a, b):
    """
    Compute cosine similarity between vectors.
    
    Args:
        a: Matrix of vectors (shape: [n, dim])
        b: Single vector (shape: [dim])
        
    Returns:
        Array of similarity scores
    """
    a_norm = a / (np.linalg.norm(a, axis=1, keepdims=True) + 1e-10)
    b_norm = b / (np.linalg.norm(b, keepdims=True) + 1e-10)
    return (a_norm @ b_norm.T).flatten()


@dataclass
class VectorStore:
    """
    In-memory vector store with cosine similarity search.
    """
    embeddings: np.ndarray = field(default_factory=lambda: np.zeros((0, 0), dtype="float32"))
    texts: List[str] = field(default_factory=list)
    metas: List[Dict[str, Any]] = field(default_factory=list)

    def add(self, texts: List[str], embeddings: np.ndarray, metas: Optional[List[Dict]] = None):
        """
        Add texts and their embeddings to the store.
        
        Args:
            texts: List of text strings
            embeddings: Corresponding embeddings
            metas: Optional metadata dictionaries for each text
        """
        if embeddings.shape[0] != len(texts):
            raise ValueError("Mismatch: texts vs embeddings")

        self.texts.extend(texts)
        self.metas.extend(metas or [{} for _ in texts])

        if self.embeddings.size == 0:
            self.embeddings = embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, embeddings])

    def search(self, query_emb: np.ndarray, k=5):
        """
        Search for top-k most similar texts.
        
        Args:
            query_emb: Query embedding vector
            k: Number of results to return
            
        Returns:
            List of tuples (text, metadata, score)
        """
        scores = cosine(self.embeddings, query_emb)
        idx = np.argsort(scores)[::-1][:k]

        return [(self.texts[i], self.metas[i], float(scores[i])) for i in idx]

    def save(self, path):
        """Save vector store to disk."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump((self.embeddings, self.texts, self.metas), f)

    @classmethod
    def load(cls, path):
        """Load vector store from disk."""
        with open(path, "rb") as f:
            emb, texts, metas = pickle.load(f)
        store = cls()
        store.embeddings = emb
        store.texts = texts
        store.metas = metas
        return store
