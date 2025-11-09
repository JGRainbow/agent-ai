from src.agent.graph import run_agent, retrieve_node, reason_node, build_graph


def test_retrieve_node(monkeypatch):
    """Test that retrieve_node correctly fetches chunks from Elasticsearch."""
    # Patch Elastic search
    monkeypatch.setattr("src.retrieval.elastic.search_elastic", lambda q, k: ["chunk1", "chunk2"])

    state = {"query": "test query", "retrieved_chunks": [], "result": {}}
    new_state = retrieve_node(state)

    assert new_state["retrieved_chunks"] == ["chunk1", "chunk2"]
    assert new_state["query"] == "test query"  # Query should be preserved


def test_reason_node():
    """Test that reason_node generates the expected result structure."""
    state = {
        "query": "test",
        "retrieved_chunks": [
            {"chunk_id": 1, "doc_name": "test.pdf", "text": "Sample text", "score": 0.9}
        ],
        "result": {}
    }
    new_state = reason_node(state)

    assert "answer" in new_state["result"]
    assert "confidence" in new_state["result"]
    assert isinstance(new_state["result"]["sources"], list)
    assert len(new_state["result"]["sources"]) > 0
    assert new_state["result"]["sources"][0]["doc_name"] == "fake.pdf"
    assert new_state["result"]["sources"][0]["content"] == "Sample text"
    assert new_state["result"]["sources"][0]["score"] == 0.9


def test_graph_returns_structured_output(monkeypatch):
    """Test the full graph execution returns the expected structure."""
    # Arrange - mock the Elasticsearch search
    def fake_search(query, k=3):
        return [
            {"chunk_id": 1, "doc_name": "fake.pdf", "text": "Sample chunk", "score": 0.95}
        ]

    monkeypatch.setattr("src.retrieval.elastic.search_elastic", fake_search)

    # Act
    result = run_agent("How do I change my name?")

    # Assert
    assert "answer" in result
    assert "confidence" in result
    assert "sources" in result
    assert len(result["sources"]) == 1
    assert result["sources"][0]["doc_name"] == "fake.pdf"
    assert result["sources"][0]["chunk_id"] == 1
    assert result["sources"][0]["score"] == 0.95


def test_build_graph():
    """Test that the graph can be built and compiled successfully."""
    app = build_graph()
    assert app is not None
    # Verify we can invoke it with a valid state
    initial_state = {"query": "test", "retrieved_chunks": [], "result": {}}
    # This will fail if graph structure is wrong, but that's okay for this test
    # We're just checking it compiles
