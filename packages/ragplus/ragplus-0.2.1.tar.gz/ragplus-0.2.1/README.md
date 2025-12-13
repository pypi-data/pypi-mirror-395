# ragplus

[![PyPI version](https://badge.fury.io/py/ragplus.svg)](https://badge.fury.io/py/ragplus)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/ragplus)](https://pepy.tech/project/ragplus)

**Lightweight, production-ready RAG (Retrieval-Augmented Generation) toolkit with 100% offline capabilities.**

Build powerful RAG applications with document loading, hybrid search, reranking, and semantic chunking - all without API keys or internet connectivity.

---

## 🎯 Why ragplus?

- **🔒 100% Offline** - No API keys, no internet required, perfect for air-gapped environments
- **⚡ Production-Ready** - Proper error handling, type hints, comprehensive testing
- **🎨 Flexible** - Plug in any LLM (OpenAI, Anthropic, local models, Ollama)
- **📦 Lightweight** - Minimal dependencies, easy to integrate
- **🚀 High Performance** - Hybrid search + reranking for 20-40% accuracy boost

---

## ✨ Features

### Core RAG Capabilities
- 🔹 **Smart Document Loading** - Auto-detects and loads PDF, DOCX, TXT files
- 🔹 **Multiple Embedding Models** - MiniLM, BGE, E5 (all offline)
- 🔹 **Advanced Chunking** - Fixed, sentence-based, markdown-aware, heading-based
- 🔹 **Vector Storage** - In-memory with persistence and metadata filtering
- 🔹 **Semantic Search** - Cosine similarity with optional hybrid BM25

### v0.2.1 Advanced Features
- 🔍 **Hybrid Search** - Combines BM25 keyword + embedding semantic search
- 🎯 **Cross-Encoder Reranking** - 20-40% accuracy improvement
- 💾 **Persistent Storage** - Cache embeddings for instant reloads
- 🏷️ **Metadata Filtering** - Filter by source, page, section, custom fields
- 📝 **Token-Based Truncation** - Accurate context limits with tiktoken
- 🤖 **Auto-Loader** - Handles file paths, bytes, and text automatically

---

## 📦 Installation

```bash
pip install ragplus
```

**Requirements:** Python 3.9+

---

## 🚀 Quick Start

### Basic RAG Pipeline

```python
from ragplus import rag_answer, Embedder

def my_llm(prompt: str) -> str:
    # Use any LLM: OpenAI, Anthropic, Ollama, local models
    return "Your LLM response here"

# Works with text, file paths, or PDF bytes
documents = "RAG combines retrieval with generation for better AI responses."
query = "What is RAG?"

answer = rag_answer(query, documents, llm_fn=my_llm)
print(answer)
```

### Advanced Usage with All Features

```python
from ragplus import rag_answer, Embedder

# Maximum accuracy configuration
answer = rag_answer(
    query="What are the key findings?",
    documents="report.pdf",  # or PDF bytes from upload
    llm_fn=my_llm,
    
    # Advanced features
    use_hybrid_search=True,      # BM25 + embeddings
    use_reranking=True,           # Cross-encoder reranking
    chunk_strategy="sentence",    # Better chunking
    max_tokens=4096,              # Token-based truncation
    persist_dir="./rag_cache",    # Cache for fast reloads
    
    # Fine-tuning
    k=10,                         # Retrieve top 10 chunks
    embedder=Embedder("bge-base") # High-accuracy embeddings
)
```

---

## 📚 Documentation

### Load Documents

```python
from ragplus import load_document, load_pdf, load_docx

# Auto-detect format
text = load_document("report.pdf")

# Specific loaders
pdf_text = load_pdf("document.pdf")
docx_text = load_docx("report.docx")
```

### Choose Embedding Models

```python
from ragplus import Embedder

# High accuracy (recommended)
embedder = Embedder(model_name="bge-base")

# Fastest
embedder = Embedder(model_name="minilm")

# Best accuracy
embedder = Embedder(model_name="e5-large")
```

### Hybrid Search (BM25 + Embeddings)

```python
from ragplus import HybridRetriever, VectorStore, Embedder

embedder = Embedder()
store = VectorStore()
# ... add documents ...

hybrid = HybridRetriever(
    vectorstore=store,
    embedder=embedder,
    bm25_weight=0.3,        # 30% keyword matching
    embedding_weight=0.7     # 70% semantic similarity
)

results = hybrid.search("your query", k=5)
```

### Semantic Chunking Strategies

```python
from ragplus import chunk_text

# Markdown-aware (preserves structure)
chunks = chunk_text(text, strategy="markdown")

# Sentence-based (natural boundaries)
chunks = chunk_text(text, strategy="sentence")

# Heading-based (section-aware)
chunks = chunk_text(text, strategy="heading")

# Fixed-size (default)
chunks = chunk_text(text, size=500, overlap=50)
```

### Persistent Vector Store

```python
from ragplus import VectorStore

# Auto-save and auto-load
store = VectorStore(persist_dir="./my_index")
store.add_documents(texts, embeddings, doc_id="file1.pdf")

# Reload instantly on next run
store = VectorStore(persist_dir="./my_index")  # Auto-loads existing data
```

---

## 🎓 Examples

See the [`examples/`](examples/) directory:
- [`basic_rag.py`](examples/basic_rag.py) - Simple RAG pipeline
- [`advanced_rag.py`](examples/advanced_rag.py) - All v0.2.1 features

---

## 🔑 Keywords

RAG, Retrieval Augmented Generation, LLM, embeddings, vector search, semantic search, document QA, offline RAG, Python RAG, BM25, hybrid search, cross-encoder, reranking, PDF extraction, DOCX parsing, sentence transformers, BGE embeddings, E5 embeddings, local RAG, air-gapped AI, private AI, document intelligence

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🌟 Star History

If you find ragplus useful, please consider giving it a star on [GitHub](https://github.com/vishwa7890/ragplus)!

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/vishwa7890/ragplus/issues)
- **Discussions**: [GitHub Discussions](https://github.com/vishwa7890/ragplus/discussions)
- **PyPI**: [https://pypi.org/project/ragplus/](https://pypi.org/project/ragplus/)

---

**Made with ❤️ for the AI community**
