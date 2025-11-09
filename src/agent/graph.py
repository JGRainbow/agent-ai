from typing import Optional, List
from langgraph.graph import StateGraph, END
from src.models.types import GraphState, RetrievedChunk, AgentResult
from src.models.schemas import Source
from src.adapters.repository import AbstractDatabaseRepository
from src.adapters.elasticsearch_repository import ElasticsearchRepository
from src.config import settings


def retrieve_node(
    state: GraphState,
    repository: Optional[AbstractDatabaseRepository] = None
) -> GraphState:
    """
    Retrieves relevant chunks from the database based on the query.
    Args:
        state: The current graph state
        repository: Optional database repository. Defaults to ElasticsearchRepository.
    Returns:
        Updated state with retrieved_chunks populated
    """
    if repository is None:
        repository = ElasticsearchRepository()

    try:
        retrieved_chunks = repository.search(state["query"], k=settings.retrieval_k)
        state["retrieved_chunks"] = retrieved_chunks
    except Exception as e:
        # Log error and set empty chunks on failure
        print(f"Error retrieving chunks: {e}")
        state["retrieved_chunks"] = []

    return state


def reason_node(state: GraphState) -> GraphState:
    """
    Processes retrieved chunks and generates the answer.
    Args:
        state: The current graph state with retrieved_chunks
    Returns:
        Updated state with result populated
    """
    # TODO: Replace with actual LLM call
    retrieved_chunks: List[RetrievedChunk] = state.get("retrieved_chunks", [])

    # Convert retrieved chunks to Source objects
    sources = []
    for chunk in retrieved_chunks:
        sources.append(Source(
            doc_name=chunk["doc_name"],
            chunk_id=chunk["chunk_id"],
            content=chunk["text"],
            score=chunk["score"]
        ))

    result: AgentResult = {
        "answer": "Stub answer based on retrieval",
        "confidence": 0.95,
        "sources": sources
    }

    state["result"] = result
    return state


def build_graph(
    repository: Optional[AbstractDatabaseRepository] = None
) -> StateGraph:
    """
    Builds and compiles the LangGraph workflow.
    Args:
        repository: Optional database repository for dependency injection
    Returns:
        A compiled StateGraph application
    """
    graph = StateGraph(GraphState)

    # Create a partial function to inject repository into retrieve_node
    def retrieve_with_repo(state: GraphState) -> GraphState:
        return retrieve_node(state, repository)

    graph.add_node("retrieve", retrieve_with_repo)
    graph.add_node("reason", reason_node)

    # Set entry point
    graph.set_entry_point("retrieve")

    # Add edges
    graph.add_edge("retrieve", "reason")
    graph.add_edge("reason", END)

    return graph.compile()


def run_agent(
    user_query: str,
    repository: Optional[AbstractDatabaseRepository] = None
) -> AgentResult:
    """
    Orchestrates the RAG pipeline to answer the user's query.
    1. Retrieves relevant documents from the vector database
    2. Calls LLM to synthesize the answer
    3. Returns the answer and the sources

    Args:
        user_query: The user's query
        repository: Optional database repository for dependency injection

    Returns:
        A dictionary containing the answer, confidence, and sources

    Raises:
        ValueError: If user_query is empty
    """
    if not user_query or not user_query.strip():
        raise ValueError("Query cannot be empty")

    app = build_graph(repository=repository)
    initial_state: GraphState = {
        "query": user_query.strip(),
        "retrieved_chunks": [],
        "result": {
            "answer": "",
            "confidence": 0.0,
            "sources": []
        }
    }
    result = app.invoke(initial_state)
    return result["result"]
