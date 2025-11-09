import pytest
from src.retrieval.embedder import embed_text

def test_embed_text_produces_vector():
    # Arrange
    text = "Hello, world!"

    # Act
    vector = embed_text(text)

    # Assert
    assert vector is not None
    assert len(vector) == 1536
