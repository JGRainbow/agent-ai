from src.agent_graph import build_graph, run_graph


def test_graph_returns_structured_output(monkeypatch):
    # Arrange
    monkeypatch.setattr("src.agent_graph.search_elastic", lambda q, k=3: ["Sample text about name change."])
    monkeypatch.setattr("src.agent_graph.call_llm", lambda q, docs: {"answer": "Send certificate", "confidence": 0.9})

    # Act
    graph = build_graph()
    result = run_graph(graph, "How do I change my name?")

    # Assert
    assert result == {"answer": "Send certificate", "confidence": 0.9}
