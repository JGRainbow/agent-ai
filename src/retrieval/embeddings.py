from typing import List
from sentence_transformers import SentenceTransformer
from src.config import settings

_model = None


def get_model() -> SentenceTransformer:
    """Get or create the sentence transformer model."""
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.embedding_model)
    return _model


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Embed a list of texts into vectors.
    Args:
        texts: List of text strings to embed
    Returns:
        List of embedding vectors, where each vector is a list of floats
    """
    model = get_model()
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
    return embeddings.tolist()
