# ragplus

Lightweight, production-ready RAG toolkit with **fully offline** capabilities.

## ✨ Features

### Core RAG
- 🔹 **Text chunking** (fixed, sentence, markdown, heading-based)
- 🔹 **Multiple embedding models** (MiniLM, BGE, E5)
- 🔹 **In-memory vector store** with persistence
- 🔹 **Cosine similarity search** with metadata filtering
- 🔹 **High-level RAG pipeline** (`rag_answer`)

### v0.2.0 New Features
- 📄 **Document loaders** (PDF, DOCX, TXT) - fully offline
- 🔍 **Hybrid search** (BM25 + embeddings)
- 🎯 **Cross-encoder reranking** for better accuracy
- 💾 **Persistent vector store** with auto-save
- 🏷️ **Metadata filtering** by source, page, etc.
- 📝 **Semantic chunking** strategies

### Key Advantages
- ✅ **100% Offline** - no API keys required
- ✅ **Lightweight** - minimal dependencies
- ✅ **Production-ready** - proper error handling
- ✅ **Plug-in ANY LLM** (OpenAI, local models, etc.)

## Installation

```bash
pip install ragplus
```

## Quick Example

```python
from ragplus import rag_answer, Embedder

def llm(prompt: str):
    return "Your LLM response here"

docs = ["RAG means retrieving before generating."]
query = "What is RAG?"

answer = rag_answer(query, docs, llm_fn=llm, embedder=Embedder())
print(answer)
```

## Advanced Usage

### Load Documents

```python
from ragplus import load_document, load_pdf

# Auto-detect format
text = load_document("report.pdf")

# Specific loaders
text = load_pdf("document.pdf")
```

### Use Better Embeddings

```python
from ragplus import Embedder

# BGE model (higher accuracy)
embedder = Embedder(model_name="bge-base")

# E5 model
embedder = Embedder(model_name="e5-large")
```

### Hybrid Search

```python
from ragplus import HybridRetriever, VectorStore, Embedder

embedder = Embedder()
store = VectorStore()
# ... add documents ...

hybrid = HybridRetriever(
    vectorstore=store,
    embedder=embedder,
    bm25_weight=0.3,
    embedding_weight=0.7
)

results = hybrid.search("query", k=5)
```

### Semantic Chunking

```python
from ragplus import chunk_text

# Markdown-aware
chunks = chunk_text(text, strategy="markdown")

# Sentence-based
chunks = chunk_text(text, strategy="sentence")
```

### Persistent Storage

```python
from ragplus import VectorStore

# Auto-save and auto-load
store = VectorStore(persist_dir="./my_index")
store.add_documents(texts, embeddings, doc_id="file1.pdf")
```

## Examples

See `examples/` directory:
- `basic_rag.py` - Simple RAG pipeline
- `advanced_rag.py` - All v0.2.0 features

## License

MIT License
