"""
Hybrid retriever combining BM25 and embedding-based search.
"""

import numpy as np
from typing import List, Tuple, Dict, Any
from ..vectorstore import VectorStore
from ..embedder import Embedder
from .bm25 import BM25Retriever


class HybridRetriever:
    """
    Hybrid retriever combining BM25 keyword search with embedding-based semantic search.
    """
    
    def __init__(
        self,
        vectorstore: VectorStore,
        embedder: Embedder,
        bm25_weight: float = 0.3,
        embedding_weight: float = 0.7
    ):
        """
        Initialize hybrid retriever.
        
        Args:
            vectorstore: VectorStore instance
            embedder: Embedder instance
            bm25_weight: Weight for BM25 scores (default: 0.3)
            embedding_weight: Weight for embedding scores (default: 0.7)
        """
        self.vectorstore = vectorstore
        self.embedder = embedder
        self.bm25_weight = bm25_weight
        self.embedding_weight = embedding_weight
        
        # Initialize BM25 retriever
        self.bm25 = BM25Retriever(vectorstore.texts)
    
    def search(
        self,
        query: str,
        k: int = 5,
        filter: Dict[str, Any] = None
    ) -> List[Tuple[str, Dict, float]]:
        """
        Hybrid search combining BM25 and embeddings.
        
        Args:
            query: Search query
            k: Number of results to return
            filter: Optional metadata filter
            
        Returns:
            List of (text, metadata, score) tuples
        """
        # Get BM25 results (retrieve more for reranking)
        bm25_results = self.bm25.search(query, k=k*2)
        
        # Get embedding results
        query_emb = self.embedder.encode([query])
        emb_results = self.vectorstore.search(query_emb, k=k*2, filter=filter)
        
        # Create score dictionaries
        bm25_scores = {text: score for text, score in bm25_results}
        emb_scores = {text: score for text, meta, score in emb_results}
        
        # Normalize scores to [0, 1]
        if bm25_scores:
            max_bm25 = max(bm25_scores.values()) or 1.0
            bm25_scores = {k: v/max_bm25 for k, v in bm25_scores.items()}
        
        if emb_scores:
            max_emb = max(emb_scores.values()) or 1.0
            emb_scores = {k: v/max_emb for k, v in emb_scores.items()}
        
        # Combine scores
        all_texts = set(bm25_scores.keys()) | set(emb_scores.keys())
        combined_scores = {}
        
        for text in all_texts:
            bm25_score = bm25_scores.get(text, 0.0)
            emb_score = emb_scores.get(text, 0.0)
            combined_scores[text] = (
                self.bm25_weight * bm25_score +
                self.embedding_weight * emb_score
            )
        
        # Sort by combined score
        sorted_texts = sorted(
            combined_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:k]
        
        # Get metadata for results
        text_to_meta = {text: meta for text, meta, _ in emb_results}
        
        results = []
        for text, score in sorted_texts:
            meta = text_to_meta.get(text, {})
            results.append((text, meta, score))
        
        return results
