#!/usr/bin/env python3
"""
Script to create the Elasticsearch index for vector search.
"""
import sys
import os

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.adapters.elasticsearch_repository import ElasticsearchRepository
from src.retrieval.embeddings import get_model
from src.config import settings

def main():
    """Create the Elasticsearch index with proper vector search mapping."""
    # Get embedding dimension from the model by encoding a test string
    model = get_model()
    test_embedding = model.encode(["test"], normalize_embeddings=True)
    dims = len(test_embedding[0])

    repo = ElasticsearchRepository()
    print(f"Creating index '{settings.es_index}' with {dims} dimensions...")
    repo.create_index_if_not_exists(dims=dims)
    print(f"✓ Index '{settings.es_index}' created successfully!")

if __name__ == "__main__":
    main()
