from ragplus import chunk_text, Embedder, VectorStore

def test_chunker():
    """Test text chunking functionality."""
    ch = chunk_text("hello " * 50)
    assert len(ch) > 0

def test_store():
    """Test vector store functionality."""
    texts = ["hello", "world"]
    emb = Embedder().encode(texts)
    store = VectorStore()
    store.add(texts, emb)
    assert len(store.texts) == 2
