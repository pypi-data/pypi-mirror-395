from typing import List, Dict, Any, Callable, Union, Optional
import os
import tempfile
from .chunker import chunk_text
from .embedder import Embedder
from .vectorstore import VectorStore
from .retriever import retrieve
from .utils import build_context
from .loaders import load_document

try:
    from .retrieval import HybridRetriever, Reranker
    RETRIEVAL_AVAILABLE = True
except ImportError:
    RETRIEVAL_AVAILABLE = False

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False


def rag_answer(
    query: str,
    documents,
    llm_fn: Callable[[str], str],
    k=5,
    chunk_size=500,
    chunk_overlap=50,
    chunk_strategy="fixed",
    max_context_chars=4000,
    max_tokens: Optional[int] = None,
    embedder: Embedder | None = None,
    use_hybrid_search: bool = False,
    use_reranking: bool = False,
    persist_dir: Optional[str] = None,
    bm25_weight: float = 0.3,
    embedding_weight: float = 0.7,
):
    """
    End-to-end RAG pipeline with advanced features.
    
    AUTO-LOADER:
    - File paths → load clean text
    - Raw bytes → temp file → load clean text
    - Plain text → use as-is
    
    FEATURES:
    - Hybrid search (BM25 + embeddings)
    - Cross-encoder reranking
    - Persistent vector store
    - Multiple chunking strategies
    - Token-based truncation
    
    Args:
        query: User question
        documents: File path(s), bytes, or text string(s)
        llm_fn: Function that takes a prompt and returns LLM response
        k: Number of chunks to retrieve
        chunk_size: Size of text chunks
        chunk_overlap: Overlap between chunks
        chunk_strategy: Chunking strategy ("fixed", "sentence", "markdown", "heading")
        max_context_chars: Maximum context length in characters
        max_tokens: Maximum context length in tokens (overrides max_context_chars if set)
        embedder: Optional pre-initialized Embedder instance
        use_hybrid_search: Use BM25 + embedding hybrid search (better accuracy)
        use_reranking: Use cross-encoder reranking (20-40% accuracy boost)
        persist_dir: Directory for persistent vector store
        bm25_weight: Weight for BM25 scores in hybrid search
        embedding_weight: Weight for embedding scores in hybrid search
        
    Returns:
        LLM-generated answer
    """
    docs_text = []

    # --------------------------
    # 1) HANDLE DOCUMENT INPUT
    # --------------------------
    if isinstance(documents, bytes):
        # PDF UPLOAD CASE - bytes input
        temp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp.write(documents)
        temp.close()
        docs_text.append(load_document(temp.name))
        os.unlink(temp.name)

    elif isinstance(documents, str) and "\x00" not in documents:
        # STRING → CHECK IF PATH OR TEXT
        try:
            if len(documents) < 500 and os.path.exists(documents):
                docs_text.append(load_document(documents))
            else:
                docs_text.append(documents)
        except:
            docs_text.append(documents)

    elif isinstance(documents, list):
        # LIST OF DOCUMENTS
        for item in documents:
            if isinstance(item, bytes):
                temp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
                temp.write(item)
                temp.close()
                docs_text.append(load_document(temp.name))
                os.unlink(temp.name)
            elif isinstance(item, str):
                try:
                    if len(item) < 500 and os.path.exists(item):
                        docs_text.append(load_document(item))
                    else:
                        docs_text.append(item)
                except:
                    docs_text.append(item)
            else:
                docs_text.append(str(item))
    else:
        docs_text.append(str(documents))

    # --------------------------
    # 2) CHUNK DOCUMENTS
    # --------------------------
    chunks = []
    for d in docs_text:
        chunks += chunk_text(d, size=chunk_size, overlap=chunk_overlap, strategy=chunk_strategy)

    # --------------------------
    # 3) EMBED & STORE
    # --------------------------
    embedder = embedder or Embedder()
    vectors = embedder.encode(chunks)

    # Use persistent store if specified
    if persist_dir:
        store = VectorStore(persist_dir=persist_dir)
        store.add(chunks, vectors)
    else:
        store = VectorStore()
        store.add(chunks, vectors)

    # --------------------------
    # 4) RETRIEVE
    # --------------------------
    if use_hybrid_search and RETRIEVAL_AVAILABLE:
        # Hybrid search (BM25 + embeddings)
        try:
            hybrid = HybridRetriever(
                vectorstore=store,
                embedder=embedder,
                bm25_weight=bm25_weight,
                embedding_weight=embedding_weight
            )
            results = hybrid.search(query, k=k*2 if use_reranking else k)
            top_texts = [r[0] for r in results]
        except:
            # Fallback to regular retrieval
            results = retrieve(store, query, embedder.encode, k=k*2 if use_reranking else k)
            top_texts = [r[0] for r in results]
    else:
        # Regular embedding-based retrieval
        results = retrieve(store, query, embedder.encode, k=k*2 if use_reranking else k)
        top_texts = [r[0] for r in results]

    # --------------------------
    # 5) RERANK (Optional)
    # --------------------------
    if use_reranking and RETRIEVAL_AVAILABLE:
        try:
            reranker = Reranker()
            reranked = reranker.rerank(query, top_texts, top_k=k)
            top_texts = [doc for doc, score in reranked]
        except:
            # Fallback to non-reranked results
            top_texts = top_texts[:k]
    else:
        top_texts = top_texts[:k]

    # --------------------------
    # 6) BUILD CONTEXT
    # --------------------------
    if max_tokens and TIKTOKEN_AVAILABLE:
        # Token-based truncation
        ctx = _build_context_by_tokens(top_texts, max_tokens, query)
    else:
        # Character-based truncation
        ctx = build_context(top_texts, max_chars=max_context_chars)

    # --------------------------
    # 7) GENERATE ANSWER
    # --------------------------
    prompt = f"""
You are a helpful RAG assistant.

Context:
{ctx}

Question: {query}

Answer using ONLY the above context.
"""

    return llm_fn(prompt)


def _build_context_by_tokens(chunks: List[str], max_tokens: int, query: str) -> str:
    """
    Build context with token-based truncation.
    
    Args:
        chunks: List of text chunks
        max_tokens: Maximum number of tokens
        query: Query string (to account for prompt tokens)
        
    Returns:
        Truncated context string
    """
    if not TIKTOKEN_AVAILABLE:
        # Fallback to character-based (rough estimate: 1 token ≈ 4 chars)
        max_chars = max_tokens * 4
        return build_context(chunks, max_chars=max_chars)
    
    try:
        enc = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
    except:
        enc = tiktoken.get_encoding("gpt2")
    
    # Reserve tokens for prompt template and query
    prompt_overhead = len(enc.encode("You are a helpful RAG assistant.\n\nContext:\n\n\nQuestion: \n\nAnswer using ONLY the above context.\n"))
    query_tokens = len(enc.encode(query))
    available_tokens = max_tokens - prompt_overhead - query_tokens - 50  # 50 token buffer
    
    if available_tokens <= 0:
        return chunks[0][:500] if chunks else ""
    
    # Build context within token limit
    context_parts = []
    current_tokens = 0
    
    for chunk in chunks:
        chunk_tokens = len(enc.encode(chunk))
        if current_tokens + chunk_tokens + 10 > available_tokens:  # 10 for separator
            break
        context_parts.append(chunk)
        current_tokens += chunk_tokens + 10
    
    return "\n---\n".join(context_parts)
