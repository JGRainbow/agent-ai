from fastapi import FastAPI
from src.models.schemas import QueryRequest, QueryResponse, Source
from src.agent.graph import run_agent

app = FastAPI(title="Agent-AI: Name Change Assistant")

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest) -> QueryResponse:
    result = run_agent(request.query)

    return QueryResponse(
        answer=result["answer"],
        confidence=result["confidence"],
        sources=[
            Source(
                doc_name=source["doc_name"],
                chunk_id=source["chunk_id"],
                content=source["content"],
                score=source["score"]
            ) for source in result["sources"]
        ]
    )
