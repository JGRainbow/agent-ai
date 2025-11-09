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
# Run all tests
make test
# or
pytest

# Run only unit tests (fast, no external services)
make test-unit
# or
pytest tests/unit

# Run only integration tests (requires Elasticsearch)
make test-integration
# or
pytest tests/integration -m integration
```

**Test Structure:**
- `tests/unit/` - Fast, isolated unit tests with mocks
- `tests/integration/` - Integration tests that require external services (marked with `@pytest.mark.integration`)

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
from src.adapters.elasticsearch_repository import ElasticsearchRepository
from src.config import settings

# Create repository and index
repo = ElasticsearchRepository()
repo.create_index_if_not_exists()

# Chunk your documents
texts = ["Your document text here..."]
chunks = chunk_texts(texts, chunk_size=settings.default_chunk_size, overlap=settings.default_chunk_overlap)

# Index chunks
repo.index_documents([
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

### Elasticsearch UI
- `make ui` - Start Dejavu (Elasticsearch web UI) at http://localhost:1358
- `make ui-stop` - Stop the UI container

**Using the UI:**
1. Run `make ui` to start the UI
2. Open http://localhost:1358 in your browser
3. When prompted, enter the Elasticsearch URL: `http://elasticsearch:9200`
4. You can now browse indices, view documents, and run queries

### Index Management
- `make create-index` - Create the Elasticsearch index
- `make delete-index` - Delete the Elasticsearch index
- `make check-elasticsearch` - Check Elasticsearch status and index info
- `make list-indices` - List all Elasticsearch indices

### Testing Commands
- `make test` - Run all tests
- `make test-unit` - Run only unit tests (fast)
- `make test-integration` - Run integration tests (requires services)

### Other Commands
- `make install` - Install Python dependencies

## License

[Add your license here]
