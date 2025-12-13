from typing import List, Dict, Any, Callable, Union
from .chunker import chunk_text
from .embedder import Embedder
from .vectorstore import VectorStore
from .retriever import retrieve
from .utils import build_context


def rag_answer(
    query: str,
    documents: Union[str, List[str]],
    llm_fn: Callable[[str], str],
    k=5,
    chunk_size=500,
    chunk_overlap=50,
    max_context_chars=4000,
    embedder: Embedder | None = None,
):
    """
    End-to-end RAG pipeline: chunk, embed, retrieve, and generate answer.
    
    Args:
        query: User question
        documents: Single document or list of documents
        llm_fn: Function that takes a prompt and returns LLM response
        k: Number of chunks to retrieve
        chunk_size: Size of text chunks
        chunk_overlap: Overlap between chunks
        max_context_chars: Maximum context length for LLM
        embedder: Optional pre-initialized Embedder instance
        
    Returns:
        LLM-generated answer
    """
    docs = [documents] if isinstance(documents, str) else documents

    # chunk all docs
    chunks = []
    for d in docs:
        chunks += chunk_text(d, size=chunk_size, overlap=chunk_overlap)

    embedder = embedder or Embedder()
    vectors = embedder.encode(chunks)

    store = VectorStore()
    store.add(chunks, vectors)

    results = retrieve(store, query, embedder.encode, k=k)
    top_texts = [r[0] for r in results]

    ctx = build_context(top_texts, max_chars=max_context_chars)

    prompt = f"""
You are a helpful RAG assistant.

Context:
{ctx}

Question: {query}

Answer using ONLY the above context.
"""

    return llm_fn(prompt)
