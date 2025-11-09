import pytest
from src.retriever import embed_text, search_elastic

def test_embed_text_produces_vector():
    # Arrange
    text = "Hello, world!"

    # Act
    vector = embed_text(text)

    # Assert
    assert vector is not None
    assert len(vector) == 1536


@pytest.mark.integration
def test_search_elastic_produces_results():
    # Arrange
    query = "Change driving licence"

    # Act
    results = search_elastic(query, k=3)

    # Assert
    assert results is not None
    assert len(results) >= 0
    assert len(results) <= 3
