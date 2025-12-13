import numpy as np
from typing import List, Optional

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


class Embedder:
    """
    Wrapper for sentence-transformers embedding models.
    """
    
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2", device=None):
        """
        Initialize embedder with a sentence-transformers model.
        
        Args:
            model_name: HuggingFace model name
            device: Device to run model on (cpu/cuda)
        """
        if SentenceTransformer is None:
            raise ImportError("Install sentence-transformers")

        self.model = SentenceTransformer(model_name)
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
