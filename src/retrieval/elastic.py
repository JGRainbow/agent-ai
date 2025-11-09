from elasticsearch import Elasticsearch
from src.retrieval.embeddings import embed_texts
import os


ES_INDEX = os.getenv("ES_INDEX", "rag_docs")
ES_URL = os.getenv("ES_URL", "http://localhost:9200")

es = Elasticsearch(
    hosts=[ES_URL],
    verify_certs=False,
    ssl_show_warn=False,
)


def create_index_if_not_exists(dims: int = 384):
    """
    Creates the Elasticsearch index with proper mapping for vector search.
    Args:
        dims: Dimension of the embedding vectors (default: 384 for all-MiniLM-L6-v2)
    """
    if not es.indices.exists(index=ES_INDEX):
        mapping = {
            "mappings": {
                "properties": {
                    "doc_name": {"type": "keyword"},
                    "text": {"type": "text"},
                    "embedding": {
                        "type": "dense_vector",
                        "dims": dims,
                        "index": True,
                        "similarity": "cosine"
                    }
                }
            }
        }
        # Elasticsearch 8.x+ uses 'mappings' parameter directly
        es.indices.create(index=ES_INDEX, mappings=mapping["mappings"])

def index_documents(chunks: list[dict]):
    """
    Indexes documents into Elasticsearch.
    Each chunk must have: {id, doc_name, text}
    """
    vectors = embed_texts([c["text"] for c in chunks])
    for chunk, vector in zip(chunks, vectors):
        es.index(index=ES_INDEX, id=chunk["id"], document={
            "doc_name": chunk["doc_name"],
            "text": chunk["text"],
            "embedding": vector
        })

def search_elastic(query: str, k: int) -> list[dict]:
    """Performs a vector search in Elasticsearch."""
    query_vector = embed_texts([query])[0]

    response = es.search(
        index=ES_INDEX,
        knn={
            "field": "embedding",
            "query_vector": query_vector,
            "k": k,
            "num_candidates": 50
        },
        _source=["doc_name", "text"]
    )

    hits = response["hits"]["hits"]

    return [
        {
            "chunk_id": hit["_id"],
            "doc_name": hit["_source"]["doc_name"],
            "text": hit["_source"]["text"],
            "score": hit["_score"]
        } for hit in hits
    ]
