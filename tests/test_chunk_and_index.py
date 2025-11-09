import pytest
from src.chunk_and_index import chunk_text

def test_chunk_and_index_produces_overlap():
    # Arrange
    text = "A" * 1200
    chunk_size = 500
    overlap = 50

    # Act
    chunks = chunk_text(text, chunk_size, overlap)

    # Assert
    assert len(chunks) == 3
    assert chunks[0] == "A" * 500
    assert chunks[1] == "A" * 500
    assert chunks[2] == "A" * 200