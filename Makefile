.PHONY: install test elasticsearch elasticsearch-stop elasticsearch-logs elasticsearch-clean
.PHONY: create-index delete-index check-elasticsearch list-indices

install:
	pip install -r requirements.txt

test:
	pytest

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

# Elasticsearch index management scripts
create-index:
	@python scripts/create_index.py

delete-index:
	@python scripts/delete_index.py

check-elasticsearch:
	@python scripts/check_elasticsearch.py

list-indices:
	@python scripts/list_indices.py
