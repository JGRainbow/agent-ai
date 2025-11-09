import pytest
from src.retrieval import elastic

def test_search_elastic_produces_results(monkeypatch):
    # Arrange
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
    monkeypatch.setattr(elastic, "embed_texts", lambda texts: [[1.0, 0.0], [0.0, 1.0]])
    monkeypatch.setattr(elastic.es, "search", lambda **kwargs: fake_hits)

    # Act
    results = elastic.search_elastic("cat", k=1)

    # Assert
    assert results is not None
    assert len(results) == 1
    assert results[0]["doc_name"] == "Cat.pdf"
    assert results[0]["text"] == "Cat is a cat."
    assert results[0]["score"] == 0.95
