import pytest
from src.retrieval.chunker import chunk_texts

def test_chunk_texts_respects_sentence_boundaries():
    text = (
        "You must send your old driving licence to the DVLA. "
        "If your name has changed after marriage, you must include your marriage certificate. "
        "It usually takes 3 weeks to get your new licence. "
        "Do not drive until you receive it."
    )

    chunks = chunk_texts([text], chunk_size=150, overlap=20)

    # Check general properties
    assert all(len(c["content"]) <= 200 for c in chunks)
    assert len(chunks) >= 2

    # Each chunk should end at a sentence boundary (roughly)
    for c in chunks[:-1]:
        assert c["content"].strip().endswith((".", "!", "?")), f"Chunk not sentence-aligned: {c['content']}"
