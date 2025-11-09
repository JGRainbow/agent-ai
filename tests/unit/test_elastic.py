import pytest
from unittest.mock import Mock, patch
from src.adapters.elasticsearch_repository import ElasticsearchRepository
from src.retrieval.embeddings import embed_texts


def test_search_produces_results(monkeypatch):
    """Test that repository search produces results."""
    # Create a mock Elasticsearch client
    mock_client = Mock()
    fake_hits = {
        "hits": {
            "hits": [
                {
                    "_id": "1",
                    "_score": 0.95,
                    "_source": {"doc_name": "Cat.pdf", "text": "Cat is a cat."}
                },
            ]
        }
    }
    mock_client.search.return_value = fake_hits

    # Mock embed_texts to return a simple vector
    monkeypatch.setattr("src.adapters.elasticsearch_repository.embed_texts",
                       lambda texts: [[1.0] * 384])

    # Create repository with mock client
    repo = ElasticsearchRepository(client=mock_client)

    # Act
    results = repo.search("cat", k=1)

    # Assert
    assert results is not None
    assert len(results) == 1
    assert results[0]["doc_name"] == "Cat.pdf"
    assert results[0]["text"] == "Cat is a cat."
    assert results[0]["score"] == 0.95
    assert results[0]["chunk_id"] == "1"


def test_index_documents(monkeypatch):
    """Test that index_documents works correctly."""
    mock_client = Mock()
    monkeypatch.setattr("src.adapters.elasticsearch_repository.embed_texts",
                       lambda texts: [[1.0] * 384, [2.0] * 384])

    repo = ElasticsearchRepository(client=mock_client)
    chunks = [
        {"id": "1", "doc_name": "test.pdf", "text": "First chunk"},
        {"id": "2", "doc_name": "test.pdf", "text": "Second chunk"}
    ]

    repo.index_documents(chunks)

    # Verify index was called twice
    assert mock_client.index.call_count == 2


def test_create_index_if_not_exists():
    """Test index creation."""
    from elasticsearch.exceptions import NotFoundError

    mock_client = Mock()
    mock_client.indices.get.side_effect = NotFoundError("Index not found", {}, {})
    mock_client.indices.create.return_value = {"acknowledged": True}

    repo = ElasticsearchRepository(client=mock_client)
    repo.create_index_if_not_exists(dims=384)

    mock_client.indices.create.assert_called_once()


def test_index_exists():
    """Test index_exists method."""
    from elasticsearch.exceptions import NotFoundError

    mock_client = Mock()

    # Test when index exists
    repo = ElasticsearchRepository(client=mock_client)
    assert repo.index_exists() == True

    # Test when index doesn't exist
    mock_client2 = Mock()
    mock_client2.indices.get.side_effect = NotFoundError("Index not found", {}, {})
    repo2 = ElasticsearchRepository(client=mock_client2)
    assert repo2.index_exists() == False
