from typing import List, Dict, Any, Optional
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from src.adapters.repository import AbstractDatabaseRepository
from src.config import settings
from src.retrieval.embeddings import embed_texts


class ElasticsearchRepository(AbstractDatabaseRepository):
    """Elasticsearch implementation of the database repository."""

    def __init__(self, client: Optional[Elasticsearch] = None):
        """
        Initialize the Elasticsearch repository.
        Args:
            client: Optional Elasticsearch client. If not provided, creates a new one.
        """
        self._client = client or self._create_client()
        self.index_name = settings.es_index

    @property
    def client(self) -> Elasticsearch:
        """Get the Elasticsearch client (for scripts that need direct access)."""
        return self._client

    def _create_client(self) -> Elasticsearch:
        """Create and return an Elasticsearch client."""
        return Elasticsearch(
            hosts=[settings.es_url],
            verify_certs=False,
            ssl_show_warn=False,
            request_timeout=30,
        )

    def create_index_if_not_exists(self, dims: int = None) -> None:
        """
        Creates the Elasticsearch index with proper mapping for vector search.
        Args:
            dims: Dimension of the embedding vectors. Defaults to settings.embedding_dims
        """
        if dims is None:
            dims = settings.embedding_dims

        # Check if index exists by trying to get it
        try:
            self._client.indices.get(index=self.index_name)
            return  # Index already exists
        except NotFoundError:
            pass  # Index doesn't exist, continue to create it

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
        self._client.indices.create(index=self.index_name, mappings=mapping["mappings"])

    def index_documents(self, chunks: List[Dict[str, Any]]) -> None:
        """
        Indexes documents into Elasticsearch.
        Each chunk must have: {id, doc_name, text}
        """
        if not chunks:
            return

        vectors = embed_texts([c["text"] for c in chunks])
        for chunk, vector in zip(chunks, vectors):
            self._client.index(
                index=self.index_name,
                id=chunk["id"],
                document={
                    "doc_name": chunk["doc_name"],
                    "text": chunk["text"],
                    "embedding": vector
                }
            )

    def search(self, query: str, k: int = None) -> List[Dict[str, Any]]:
        """
        Performs a vector search in Elasticsearch.
        Args:
            query: The search query
            k: Number of results to return. Defaults to settings.retrieval_k
        Returns:
            List of dictionaries with: {chunk_id, doc_name, text, score}
        """
        if k is None:
            k = settings.retrieval_k

        query_vector = embed_texts([query])[0]

        response = self._client.search(
            index=self.index_name,
            knn={
                "field": "embedding",
                "query_vector": query_vector,
                "k": k,
                "num_candidates": settings.knn_num_candidates
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

    def delete_index(self) -> None:
        """Delete the Elasticsearch index."""
        if self.index_exists():
            self._client.indices.delete(index=self.index_name)

    def index_exists(self) -> bool:
        """Check if the index exists."""
        try:
            self._client.indices.get(index=self.index_name)
            return True
        except NotFoundError:
            return False
