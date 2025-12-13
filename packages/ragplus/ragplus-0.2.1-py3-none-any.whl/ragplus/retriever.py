from typing import List, Dict, Tuple, Any
from .vectorstore import VectorStore


def retrieve(store: VectorStore, query: str, embed_fn, k=5):
    """
    Retrieve top-k most relevant texts for a query.
    
    Args:
        store: VectorStore instance
        query: Query string
        embed_fn: Function to embed the query
        k: Number of results to return
        
    Returns:
        List of tuples (text, metadata, score)
    """
    query_vec = embed_fn([query]).reshape(1, -1)
    return store.search(query_vec, k)
