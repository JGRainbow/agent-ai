from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class AbstractDatabaseRepository(ABC):
    """Abstract base class for database repositories."""

    @abstractmethod
    def create_index_if_not_exists(self, dims: int) -> None:
        """Create the index if it doesn't exist."""
        pass

    @abstractmethod
    def index_documents(self, chunks: List[Dict[str, Any]]) -> None:
        """
        Index documents into the database.
        Each chunk must have: {id, doc_name, text}
        """
        pass

    @abstractmethod
    def search(self, query: str, k: int) -> List[Dict[str, Any]]:
        """
        Perform a vector search.
        Returns a list of dictionaries with: {chunk_id, doc_name, text, score}
        """
        pass

    @abstractmethod
    def delete_index(self) -> None:
        """Delete the index."""
        pass

    @abstractmethod
    def index_exists(self) -> bool:
        """Check if the index exists."""
        pass
