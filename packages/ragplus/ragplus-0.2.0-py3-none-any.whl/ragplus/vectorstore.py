import numpy as np
import pickle
import os
import json
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
    In-memory vector store with cosine similarity search, persistence, and metadata filtering.
    """
    embeddings: np.ndarray = field(default_factory=lambda: np.zeros((0, 0), dtype="float32"))
    texts: List[str] = field(default_factory=list)
    metas: List[Dict[str, Any]] = field(default_factory=list)
    persist_dir: Optional[str] = None

    def __post_init__(self):
        """Auto-load from persist_dir if it exists."""
        if self.persist_dir and os.path.exists(self.persist_dir):
            self._load_from_dir()

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
        
        # Auto-save if persist_dir is set
        if self.persist_dir:
            self._save_to_dir()

    def add_documents(
        self,
        texts: List[str],
        embeddings: np.ndarray,
        doc_id: str,
        metas: Optional[List[Dict]] = None
    ):
        """
        Add documents with a document ID for tracking.
        
        Args:
            texts: List of text strings
            embeddings: Corresponding embeddings
            doc_id: Document identifier (e.g., filename)
            metas: Optional metadata dictionaries
        """
        # Add doc_id to metadata
        if metas is None:
            metas = [{"doc_id": doc_id} for _ in texts]
        else:
            for meta in metas:
                meta["doc_id"] = doc_id
        
        self.add(texts, embeddings, metas)

    def search(self, query_emb: np.ndarray, k=5, filter: Optional[Dict[str, Any]] = None):
        """
        Search for top-k most similar texts with optional metadata filtering.
        
        Args:
            query_emb: Query embedding vector
            k: Number of results to return
            filter: Optional metadata filter (e.g., {"source": "file.pdf"})
            
        Returns:
            List of tuples (text, metadata, score)
        """
        if self.embeddings.size == 0:
            return []
        
        # Apply metadata filter if provided
        if filter:
            valid_indices = []
            for i, meta in enumerate(self.metas):
                if all(meta.get(key) == value for key, value in filter.items()):
                    valid_indices.append(i)
            
            if not valid_indices:
                return []
            
            # Filter embeddings and compute scores
            filtered_emb = self.embeddings[valid_indices]
            scores = cosine(filtered_emb, query_emb)
            
            # Get top-k from filtered results
            top_k_filtered = np.argsort(scores)[::-1][:k]
            
            return [
                (self.texts[valid_indices[i]], self.metas[valid_indices[i]], float(scores[i]))
                for i in top_k_filtered
            ]
        else:
            # No filter - search all
            scores = cosine(self.embeddings, query_emb)
            idx = np.argsort(scores)[::-1][:k]
            return [(self.texts[i], self.metas[i], float(scores[i])) for i in idx]

    def save(self, path):
        """Save vector store to a single pickle file."""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump((self.embeddings, self.texts, self.metas), f)

    @classmethod
    def load(cls, path):
        """Load vector store from a single pickle file."""
        with open(path, "rb") as f:
            emb, texts, metas = pickle.load(f)
        store = cls()
        store.embeddings = emb
        store.texts = texts
        store.metas = metas
        return store

    def _save_to_dir(self):
        """Save to persist_dir with structured format."""
        if not self.persist_dir:
            return
        
        os.makedirs(self.persist_dir, exist_ok=True)
        
        # Save embeddings as numpy array
        np.save(os.path.join(self.persist_dir, "embeddings.npy"), self.embeddings)
        
        # Save texts and metadata as JSON
        with open(os.path.join(self.persist_dir, "texts.json"), "w", encoding="utf-8") as f:
            json.dump(self.texts, f, ensure_ascii=False, indent=2)
        
        with open(os.path.join(self.persist_dir, "metadata.json"), "w", encoding="utf-8") as f:
            json.dump(self.metas, f, ensure_ascii=False, indent=2)

    def _load_from_dir(self):
        """Load from persist_dir."""
        if not self.persist_dir or not os.path.exists(self.persist_dir):
            return
        
        emb_path = os.path.join(self.persist_dir, "embeddings.npy")
        texts_path = os.path.join(self.persist_dir, "texts.json")
        meta_path = os.path.join(self.persist_dir, "metadata.json")
        
        if os.path.exists(emb_path):
            self.embeddings = np.load(emb_path)
        
        if os.path.exists(texts_path):
            with open(texts_path, "r", encoding="utf-8") as f:
                self.texts = json.load(f)
        
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                self.metas = json.load(f)
