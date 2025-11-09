from src.api.main import app

def test_query_endpoint_returns_structured_response(client):
    payload = {"query": "How do I change my name after marriage?"}
    response = client.post("/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["sources"], list)
