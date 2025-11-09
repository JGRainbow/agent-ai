from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    query: str


class Source(BaseModel):
    doc_name: str
    chunk_id: int
    content: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[Source]
