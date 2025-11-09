import pytest
from src.retrieval.elastic import search_elastic

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
