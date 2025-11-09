"""
Legacy Elasticsearch module.
This module is kept for backward compatibility but new code should use
src.adapters.elasticsearch_repository.ElasticsearchRepository instead.
"""
from typing import List, Dict, Any
from src.adapters.elasticsearch_repository import ElasticsearchRepository
from src.config import settings

# Create a default repository instance for backward compatibility
_default_repo = ElasticsearchRepository()


def create_index_if_not_exists(dims: int = None) -> None:
    """Create the index if it doesn't exist. Uses default repository."""
    _default_repo.create_index_if_not_exists(dims=dims)


def index_documents(chunks: List[Dict[str, Any]]) -> None:
    """Index documents. Uses default repository."""
    _default_repo.index_documents(chunks)


def search_elastic(query: str, k: int = None) -> List[Dict[str, Any]]:
    """Search Elasticsearch. Uses default repository."""
    return _default_repo.search(query, k=k)
