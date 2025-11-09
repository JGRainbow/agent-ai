from unittest.mock import Mock
from src.agent.graph import run_agent, retrieve_node, reason_node, build_graph
from src.models.types import GraphState, RetrievedChunk
from src.adapters.repository import AbstractDatabaseRepository


def test_retrieve_node():
    """Test that retrieve_node correctly fetches chunks from the repository."""
    # Create a mock repository
    mock_repo = Mock(spec=AbstractDatabaseRepository)
    mock_repo.search.return_value = [
        {"chunk_id": "1", "doc_name": "test.pdf", "text": "chunk1", "score": 0.9},
        {"chunk_id": "2", "doc_name": "test.pdf", "text": "chunk2", "score": 0.8}
    ]

    state: GraphState = {
        "query": "test query",
        "retrieved_chunks": [],
        "result": {"answer": "", "confidence": 0.0, "sources": []}
    }
    new_state = retrieve_node(state, repository=mock_repo)

    assert len(new_state["retrieved_chunks"]) == 2
    assert new_state["retrieved_chunks"][0]["chunk_id"] == "1"
    assert new_state["query"] == "test query"  # Query should be preserved
    mock_repo.search.assert_called_once_with("test query", k=3)


def test_reason_node():
    """Test that reason_node generates the expected result structure."""
    state: GraphState = {
        "query": "test",
        "retrieved_chunks": [
            {"chunk_id": "1", "doc_name": "test.pdf", "text": "Sample text", "score": 0.9}
        ],
        "result": {"answer": "", "confidence": 0.0, "sources": []}
    }
    new_state = reason_node(state)

    result = new_state["result"]
    assert "answer" in result
    assert "confidence" in result
    assert isinstance(result["sources"], list)
    assert len(result["sources"]) > 0
    # Fixed: should use actual doc_name from chunk, not "fake.pdf"
    # Sources are Pydantic models, access as attributes
    assert result["sources"][0].doc_name == "test.pdf"
    assert result["sources"][0].content == "Sample text"
    assert result["sources"][0].score == 0.9
    assert result["sources"][0].chunk_id == "1"


def test_graph_returns_structured_output():
    """Test the full graph execution returns the expected structure."""
    # Create a mock repository
    mock_repo = Mock(spec=AbstractDatabaseRepository)
    mock_repo.search.return_value = [
        {"chunk_id": "1", "doc_name": "test.pdf", "text": "Sample chunk", "score": 0.95}
    ]

    # Act
    result = run_agent("How do I change my name?", repository=mock_repo)

    # Assert
    assert "answer" in result
    assert "confidence" in result
    assert "sources" in result
    assert len(result["sources"]) == 1
    # Sources are Pydantic models
    assert result["sources"][0].doc_name == "test.pdf"
    assert result["sources"][0].chunk_id == "1"
    assert result["sources"][0].score == 0.95
    assert result["sources"][0].content == "Sample chunk"


def test_build_graph():
    """Test that the graph can be built and compiled successfully."""
    app = build_graph()
    assert app is not None


def test_retrieve_node_handles_errors():
    """Test that retrieve_node handles repository errors gracefully."""
    mock_repo = Mock(spec=AbstractDatabaseRepository)
    mock_repo.search.side_effect = Exception("Connection error")

    state: GraphState = {
        "query": "test",
        "retrieved_chunks": [],
        "result": {"answer": "", "confidence": 0.0, "sources": []}
    }

    new_state = retrieve_node(state, repository=mock_repo)
    # Should have empty chunks on error
    assert new_state["retrieved_chunks"] == []
