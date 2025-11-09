#!/usr/bin/env python3
"""
Script to delete and recreate the Elasticsearch index with proper mapping.
Use this if you get errors about the embedding field not existing.
"""
import sys
import os

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.adapters.elasticsearch_repository import ElasticsearchRepository
from src.retrieval.embeddings import get_model
from src.config import settings

def main():
    """Delete and recreate the index with proper mapping."""
    repo = ElasticsearchRepository()

    # Check if index exists
    if repo.index_exists():
        print(f"⚠️  Index '{settings.es_index}' exists but has wrong mapping.")
        response = input(f"Delete and recreate it? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return

        print(f"Deleting index '{settings.es_index}'...")
        repo.delete_index()
        print("✓ Index deleted")
    else:
        print(f"Index '{settings.es_index}' does not exist.")

    # Get embedding dimension from the model
    model = get_model()
    test_embedding = model.encode(["test"], normalize_embeddings=True)
    dims = len(test_embedding[0])

    # Create index with proper mapping
    print(f"Creating index '{settings.es_index}' with {dims} dimensions...")
    repo.create_index_if_not_exists(dims=dims)
    print(f"✓ Index '{settings.es_index}' created successfully!")
    print("\n⚠️  Note: You'll need to re-index your documents:")
    print("   python scripts/index_single_pdf.py <your_pdf_file>")

if __name__ == "__main__":
    main()
