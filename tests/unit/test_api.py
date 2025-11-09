from unittest.mock import Mock, patch
from src.api.main import app
from src.adapters.repository import AbstractDatabaseRepository


def test_query_endpoint_returns_structured_response(client):
    """Test that the API endpoint returns a properly structured response."""
    # Create a mock repository
    mock_repo = Mock(spec=AbstractDatabaseRepository)
    mock_repo.search.return_value = [
        {
            "chunk_id": "1",
            "doc_name": "test.pdf",
            "text": "Sample text about name change.",
            "score": 0.95
        }
    ]

    # Patch the default repository in the API
    with patch("src.api.main._default_repository", mock_repo):
        payload = {"query": "How do I change my name after marriage?"}
        response = client.post("/query", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "confidence" in data
        assert isinstance(data["sources"], list)
        assert len(data["sources"]) > 0
        assert data["sources"][0]["doc_name"] == "test.pdf"


def test_query_endpoint_validates_empty_query(client):
    """Test that the API endpoint rejects empty queries."""
    payload = {"query": ""}
    response = client.post("/query", json=payload)
    assert response.status_code == 422  # Validation error


def test_query_endpoint_handles_errors(client):
    """Test that the API endpoint handles errors gracefully."""
    # Test with an error that occurs during graph execution (not caught by retrieve_node)
    # We'll make run_agent itself raise an exception
    from unittest.mock import patch

    with patch("src.api.main.run_agent") as mock_run_agent:
        mock_run_agent.side_effect = Exception("Unexpected error")

        payload = {"query": "test query"}
        response = client.post("/query", json=payload)
        assert response.status_code == 500
        assert "error" in response.json()["detail"].lower()


def test_query_endpoint_handles_retrieval_failure_gracefully(client):
    """Test that retrieval failures are handled gracefully (returns 200 with empty sources)."""
    mock_repo = Mock(spec=AbstractDatabaseRepository)
    mock_repo.search.side_effect = Exception("Database error")

    with patch("src.api.main._default_repository", mock_repo):
        payload = {"query": "test query"}
        response = client.post("/query", json=payload)
        # retrieve_node catches the error, so we get 200 with empty sources
        assert response.status_code == 200
        data = response.json()
        assert len(data["sources"]) == 0  # Empty sources due to retrieval failure


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
