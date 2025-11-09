"""
Integration tests for Elasticsearch repository.
These tests require a running Elasticsearch instance.
Run with: pytest tests/integration -m integration
"""
import pytest
from src.adapters.elasticsearch_repository import ElasticsearchRepository
from src.retrieval.chunker import chunk_texts
from src.config import settings


@pytest.mark.integration
def test_elasticsearch_search_integration():
    """Test search against a real Elasticsearch instance."""
    repo = ElasticsearchRepository()

    # Ensure index exists
    repo.create_index_if_not_exists()

    # Index some test documents
    test_chunks = [
        {"id": "test1", "doc_name": "test.pdf", "text": "This is a test document about name changes."},
        {"id": "test2", "doc_name": "test.pdf", "text": "You need to send your marriage certificate."},
    ]
    repo.index_documents(test_chunks)

    # Wait a moment for indexing
    import time
    time.sleep(1)

    # Search
    results = repo.search("name change", k=2)

    # Cleanup
    repo.delete_index()

    # Assertions
    assert len(results) > 0
    assert results[0]["doc_name"] == "test.pdf"


@pytest.mark.integration
def test_elasticsearch_index_creation_integration():
    """Test index creation against a real Elasticsearch instance."""
    repo = ElasticsearchRepository()

    # Delete index if it exists
    if repo.index_exists():
        repo.delete_index()

    # Create index
    repo.create_index_if_not_exists()
    assert repo.index_exists()

    # Cleanup
    repo.delete_index()
