# ragplus

Lightweight, simple, production-ready RAG utilities.

## Features
- 🔹 Text chunking  
- 🔹 Embedding (Sentence Transformers)  
- 🔹 In-memory vector store  
- 🔹 Cosine similarity search  
- 🔹 High-level RAG pipeline (`rag_answer`)  
- 🔹 Plug-in ANY LLM (OpenAI, Together, local models, etc.)

## Installation

```bash
pip install ragplus
```

## Quick Example

```python
from ragplus import rag_answer, Embedder

def llm(prompt: str):
    return "Fake answer.\n" + prompt

docs = ["RAG means retrieving before generating."]
query = "What is RAG?"

print(
    rag_answer(query, docs, llm_fn=llm, embedder=Embedder())
)
```


## License

MIT License.
# ragplus
