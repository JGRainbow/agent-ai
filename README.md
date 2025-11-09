# Agent-AI: Name Change Assistant

A RAG (Retrieval-Augmented Generation) system built with LangGraph, FastAPI, and Elasticsearch to answer questions about name change procedures.

## Project Structure

```
agent-ai/
├── src/
│   ├── api/                  # FastAPI service
│   ├── agent/                 # LangGraph orchestration
│   ├── retrieval/             # Chunking, embeddings, Elasticsearch ops
│   ├── models/                # Pydantic data schemas
│   ├── config.py
│   └── utils.py
├── scripts/                   # Utility scripts
├── tests/
├── data/
├── notebooks/
├── docker-compose.yml
└── Makefile
```

## Prerequisites

- Python 3.12+
- Docker and Docker Compose
- Make (optional, for convenience commands)

## Setup

### 1. Install Dependencies

```bash
make install
# or
pip install -r requirements.txt
```

### 2. Start Elasticsearch

```bash
make elasticsearch
# or
docker-compose up -d elasticsearch
```

Wait for Elasticsearch to be ready (usually 30-60 seconds). You can check the status:

```bash
curl http://localhost:9200
```

### 3. Create the Elasticsearch Index

Create the index with the proper vector search mapping:

```bash
make create-index
# or
python scripts/create_index.py
```

The index will also be created automatically when you first index documents.

### 4. Environment Variables (Optional)

Copy `.env.example` to `.env` and configure if needed:

```bash
cp .env.example .env
```

Default values:
- `ES_URL=http://localhost:9200`
- `ES_INDEX=rag_docs`

## Usage

### Running Tests

```bash
make test
# or
pytest
```

### Running the API

```bash
uvicorn src.api.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Indexing Documents

```python
from src.retrieval.chunker import chunk_texts
from src.retrieval.elastic import index_documents, create_index_if_not_exists

# Create index
create_index_if_not_exists()

# Chunk your documents
texts = ["Your document text here..."]
chunks = chunk_texts(texts, chunk_size=500, overlap=50)

# Index chunks
index_documents([
    {"id": chunk["chunk_id"], "doc_name": "document.pdf", "text": chunk["content"]}
    for chunk in chunks
])
```

## Makefile Commands

### Elasticsearch Management
- `make elasticsearch` - Start Elasticsearch container
- `make elasticsearch-stop` - Stop Elasticsearch container
- `make elasticsearch-logs` - View Elasticsearch logs
- `make elasticsearch-clean` - Remove container and volumes

### Index Management
- `make create-index` - Create the Elasticsearch index
- `make delete-index` - Delete the Elasticsearch index
- `make check-elasticsearch` - Check Elasticsearch status and index info
- `make list-indices` - List all Elasticsearch indices

### Other Commands
- `make install` - Install Python dependencies
- `make test` - Run tests

## License

[Add your license here]
