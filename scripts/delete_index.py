#!/usr/bin/env python3
"""
Script to delete the Elasticsearch index.
"""
import sys
import os

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.adapters.elasticsearch_repository import ElasticsearchRepository
from src.config import settings

def main():
    """Delete the Elasticsearch index."""
    repo = ElasticsearchRepository()
    if repo.index_exists():
        print(f"Deleting index '{settings.es_index}'...")
        repo.delete_index()
        print(f"✓ Index '{settings.es_index}' deleted successfully!")
    else:
        print(f"Index '{settings.es_index}' does not exist.")

if __name__ == "__main__":
    main()
