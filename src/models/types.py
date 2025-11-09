from typing import TypedDict, List, Any
from src.models.schemas import Source


class RetrievedChunk(TypedDict):
    """Type definition for a retrieved chunk from the database."""
    chunk_id: str
    doc_name: str
    text: str
    score: float


class AgentResult(TypedDict):
    """Type definition for the agent's result."""
    answer: str
    confidence: float
    sources: List[Any]  # List[Source] - using Any because TypedDict doesn't support Pydantic models directly


class GraphState(TypedDict):
    """Type definition for the LangGraph state."""
    query: str
    retrieved_chunks: List[RetrievedChunk]
    result: AgentResult
