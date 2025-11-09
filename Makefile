.PHONY: install test test-unit test-integration elasticsearch elasticsearch-stop elasticsearch-logs elasticsearch-clean
.PHONY: create-index delete-index check-elasticsearch list-indices
.PHONY: ui ui-stop api

install:
	pip install -r requirements.txt

test:
	pytest

test-unit:
	pytest tests/unit

test-integration:
	pytest tests/integration -m integration

# Elasticsearch Docker commands
elasticsearch:
	docker-compose up -d elasticsearch
	@echo "Waiting for Elasticsearch to be ready..."
	@timeout 60 bash -c 'until curl -s http://localhost:9200 > /dev/null; do sleep 2; done' || true
	@echo "Elasticsearch is ready at http://localhost:9200"

elasticsearch-stop:
	docker-compose stop elasticsearch

elasticsearch-logs:
	docker-compose logs -f elasticsearch

elasticsearch-clean:
	docker-compose down -v
	@echo "Elasticsearch container and volumes removed"

# Elasticsearch UI
ui:
	docker-compose up -d deploy
	@echo "Elasticsearch UI is available at http://localhost:1358"
	@echo "Connect to: http://elasticsearch:9200"

ui-stop:
	docker-compose stop deploy

# Elasticsearch index management scripts
create-index:
	@python scripts/create_index.py

delete-index:
	@python scripts/delete_index.py

check-elasticsearch:
	@python scripts/check_elasticsearch.py

list-indices:
	@python scripts/list_indices.py

# Document indexing
index-documents:
	@python scripts/index_documents.py

index-documents-create:
	@python scripts/index_documents.py --create-index

# Quick: Index a single PDF (usage: make index-pdf PDF=path/to/file.pdf)
index-pdf:
	@python scripts/index_single_pdf.py $(PDF)

# Start the API server
api:
	@echo "Starting API server at http://localhost:8000"
	@echo "Swagger UI: http://localhost:8000/docs"
	@python -m uvicorn src.api.main:app --reload
