.PHONY: install test elasticsearch elasticsearch-stop elasticsearch-logs elasticsearch-clean

install:
	pip install -r requirements.txt

test:
	pytest

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
