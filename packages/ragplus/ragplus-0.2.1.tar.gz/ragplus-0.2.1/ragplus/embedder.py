import numpy as np
from typing import List, Optional

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


# Model presets for easy access
MODEL_PRESETS = {
    "minilm": "sentence-transformers/all-MiniLM-L6-v2",
    "bge-base": "BAAI/bge-base-en-v1.5",
    "bge-small": "BAAI/bge-small-en-v1.5",
    "bge-large": "BAAI/bge-large-en-v1.5",
    "e5-base": "intfloat/e5-base",
    "e5-large": "intfloat/e5-large-v2",
}


class Embedder:
    """
    Wrapper for sentence-transformers embedding models.
    Supports multiple model presets including BGE and E5 models.
    """
    
    def __init__(self, model_name="minilm", provider="local", device=None):
        """
        Initialize embedder with a sentence-transformers model.
        
        Args:
            model_name: Model preset name or full HuggingFace model name
                       Presets: minilm, bge-base, bge-small, bge-large, e5-base, e5-large
            provider: Provider type (default: "local" for offline models)
            device: Device to run model on (cpu/cuda)
        """
        if SentenceTransformer is None:
            raise ImportError("Install sentence-transformers: pip install sentence-transformers")

        # Resolve model name from preset or use as-is
        resolved_model = MODEL_PRESETS.get(model_name, model_name)
        
        self.model_name = model_name
        self.provider = provider
        self.model = SentenceTransformer(resolved_model)
        
        if device:
            self.model.to(device)

    def encode(self, texts: List[str]) -> np.ndarray:
        """
        Encode texts into embeddings.
        
        Args:
            texts: List of text strings to encode
            
        Returns:
            numpy array of embeddings (shape: [len(texts), embedding_dim])
        """
        if not texts:
            return np.zeros((0, 0), dtype="float32")

        emb = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False
        )

        return emb.astype("float32")
