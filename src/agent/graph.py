
def build_graph():
    pass


def run_graph():
    pass


def run_agent(user_query: str) -> dict:
    # TODO : Build RAG pipeline
    return {
        "answer": "Send certificate",
        "confidence": 0.9,
        "sources": [
            {
                "doc_name": "dvla_guide.pdf",
                "chunk_id": 0,
                "content": "You must send your old driving licence to the DVLA. If your name has changed after marriage, you must include your marriage certificate. It usually takes 3 weeks to get your new licence. Do not drive until you receive it.",
                "score": 0.9
            }
        ]
    }
