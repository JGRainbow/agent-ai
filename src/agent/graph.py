from langgraph import Graph, Node

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
    state = {"query": user_query, "retrieved_chunks": [], "result": {}}

    graph = Graph()

    def input_node(state: dict) -> dict:
        return state

    def retrieve_node(state: dict) -> dict:
        from src.retrieval.elastic import search_elastic
        retrieved_chunks = search_elastic(state["query"], k=3)
        state["retrieved_chunks"] = retrieved_chunks
        return state

    def reason_node(state):
        # Replace with LLM call later
        state["result"] = {
            "answer": "Stub answer based on retrieval",
            "confidence": 0.95,
            "sources": [
                {"doc_name": "fake.pdf", "chunk_id": 1, "text_snippet": state["retrieved_chunks"][0], "score": 0.95}
            ]
        }
        return state

    # Node 4: Output node
    def output_node(state):
        return state["result"]

    # Add nodes in order
    graph.add_node("input_node", input_node)
    graph.add_node("retrieve_node", retrieve_node)
    graph.add_node("reason_node", reason_node)
    graph.add_node("output_node", output_node)

    # Add edges
    graph.add_edge("input_node", "retrieve_node")
    graph.add_edge("retrieve_node", "reason_node")
    graph.add_edge("reason_node", "output_node")

    # Run graph
    result = graph.run("input_node", state)
    return result
