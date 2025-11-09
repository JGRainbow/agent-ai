from pydantic import BaseModel, Field, field_validator
from typing import List


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The user's query")

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()


class Source(BaseModel):
    doc_name: str = Field(..., description="Name of the source document")
    chunk_id: str = Field(..., description="ID of the chunk")
    content: str = Field(..., description="Content of the chunk")
    score: float = Field(..., ge=0.0, le=1.0, description="Relevance score")


class QueryResponse(BaseModel):
    answer: str = Field(..., description="The answer to the query")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    sources: List[Source] = Field(default_factory=list, description="Source documents")
