from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from src.models.schemas import QueryRequest, QueryResponse
from src.agent.graph import run_agent
from src.adapters.elasticsearch_repository import ElasticsearchRepository
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Agent-AI: Name Change Assistant")

# Create a default repository instance
_default_repository = ElasticsearchRepository()


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest) -> QueryResponse:
    """
    Process a query and return an answer with sources.

    Args:
        request: The query request containing the user's question

    Returns:
        QueryResponse with answer, confidence, and sources

    Raises:
        HTTPException: If there's an error processing the query
    """
    try:
        result = run_agent(request.query, repository=_default_repository)

        # result["sources"] already contains Source Pydantic objects
        return QueryResponse(
            answer=result["answer"],
            confidence=result["confidence"],
            sources=result["sources"]  # Already List[Source]
        )
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your query. Please try again."
        )


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
