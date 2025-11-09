from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from src.models.schemas import Source


class AbstractLLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate_answer(
        self,
        query: str,
        retrieved_chunks: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate an answer based on the query and retrieved chunks.

        Args:
            query: The user's question
            retrieved_chunks: List of retrieved document chunks with keys:
                - chunk_id: str
                - doc_name: str
                - text: str
                - score: float
            context: Optional additional context

        Returns:
            Dictionary with:
                - answer: str - The generated answer
                - confidence: float - Confidence score (0.0 to 1.0)
                - reasoning: Optional[str] - Reasoning behind the answer
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the LLM provider is available and configured."""
        pass
