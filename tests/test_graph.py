from src.agent.graph import run_agent


def test_graph_returns_structured_output(monkeypatch):
    # Arrange
    def fake_retrieve(query, k=3):
        return [
            {"chunk_id": 1, "doc_name": "fake.pdf", "text": "Sample chunk", "score": 0.9}
        ]

    def fake_llm_call(query, docs):
        return {"answer": "Stub answer", "confidence": 0.99}

    monkeypatch.setattr("src.agent.graph.retrieve_chunks", fake_retrieve)
    monkeypatch.setattr("src.agent.graph.call_llm", fake_llm_call)

    # Act
    result = run_agent("How do I change my name?")

    # Assert
    assert "answer" in result
    assert "confidence" in result
    assert "sources" in result
    assert len(result["sources"]) == 1
    assert result["sources"][0]["doc_name"] == "fake.pdf"
    assert result["sources"][0]["chunk_id"] == 1
    assert result["sources"][0]["text"] == "Sample chunk"
    assert result["sources"][0]["score"] == 0.9
