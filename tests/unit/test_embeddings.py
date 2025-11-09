from src.retrieval.embeddings import embed_texts, get_model


def test_embed_texts_produces_vectors():
    """Test that embed_texts produces correct vector format."""
    # Arrange
    texts = ["Cat", "Dog"]

    # Act
    vectors = embed_texts(texts)

    # Assert
    assert vectors is not None
    assert isinstance(vectors, list)
    assert len(vectors) == 2  # One vector per text
    assert isinstance(vectors[0], list)  # Each vector is a list
    assert len(vectors[0]) > 100  # Should have many dimensions
    assert len(vectors[0]) == len(vectors[1])  # Same dimensions


def test_get_model_returns_sentence_transformer():
    """Test that get_model returns a SentenceTransformer instance."""
    model = get_model()
    assert model is not None
    # Verify it has the encode method
    assert hasattr(model, "encode")
