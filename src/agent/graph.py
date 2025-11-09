from typing import TypedDict
from langgraph.graph import StateGraph, END

class GraphState(TypedDict):
    query: str
    retrieved_chunks: list
    result: dict


def retrieve_node(state: GraphState) -> GraphState:
    """Retrieves relevant chunks from Elasticsearch based on the query."""
    from src.retrieval.elastic import search_elastic
    retrieved_chunks = search_elastic(state["query"], k=3)
    state["retrieved_chunks"] = retrieved_chunks
    return state


def reason_node(state: GraphState) -> GraphState:
    """Processes retrieved chunks and generates the answer."""
    # Replace with LLM call later
    state["result"] = {
        "answer": "Stub answer based on retrieval",
        "confidence": 0.95,
        "sources": [
            {"doc_name": "fake.pdf", "chunk_id": 1, "text_snippet": state["retrieved_chunks"][0], "score": 0.95}
        ]
    }
    return state


def build_graph() -> StateGraph:
    """
    Builds and compiles the LangGraph workflow.
    Returns:
        A compiled StateGraph application
    """
    graph = StateGraph(GraphState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("reason", reason_node)

    # Set entry point
    graph.set_entry_point("retrieve")

    # Add edges
    graph.add_edge("retrieve", "reason")
    graph.add_edge("reason", END)

    return graph.compile()


def run_agent(user_query: str) -> dict:
    """
    Orchestrates the RAG pipeline to answer the user's query.
    1. Retrieves relevant documents from the vector database
    2. Call LLM to synthesize the answer
    3. Return the answer and the sources
    Args:
        user_query: The user's query
    Returns:
        A dictionary containing the answer, confidence, and sources
    """
    app = build_graph()
    initial_state = {"query": user_query, "retrieved_chunks": [], "result": {}}
    result = app.invoke(initial_state)
    return result["result"]
