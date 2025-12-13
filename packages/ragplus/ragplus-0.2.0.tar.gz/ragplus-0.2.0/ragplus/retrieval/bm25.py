"""
BM25 retriever for keyword-based search (fully offline).
"""

import numpy as np
from typing import List, Tuple

try:
    from rank_bm25 import BM25Okapi
except ImportError:
    BM25Okapi = None


class BM25Retriever:
    """
    BM25-based keyword retriever for offline search.
    """
    
    def __init__(self, texts: List[str]):
        """
        Initialize BM25 retriever with documents.
        
        Args:
            texts: List of document texts
        """
        if BM25Okapi is None:
            raise ImportError("Install rank-bm25: pip install rank-bm25")
        
        self.texts = texts
        
        # Tokenize documents (simple whitespace tokenization)
        tokenized_docs = [doc.lower().split() for doc in texts]
        self.bm25 = BM25Okapi(tokenized_docs)
    
    def search(self, query: str, k: int = 5) -> List[Tuple[str, float]]:
        """
        Search for top-k documents using BM25.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of (text, score) tuples
        """
        # Tokenize query
        tokenized_query = query.lower().split()
        
        # Get BM25 scores
        scores = self.bm25.get_scores(tokenized_query)
        
        # Get top-k indices
        top_k_idx = np.argsort(scores)[::-1][:k]
        
        # Return results
        return [(self.texts[i], float(scores[i])) for i in top_k_idx]
