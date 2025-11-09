#!/usr/bin/env python3
"""
Script to check if Elasticsearch is running and accessible.
"""
import sys
import os

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.adapters.elasticsearch_repository import ElasticsearchRepository
from src.config import settings

def main():
    """Check Elasticsearch connection and index status."""
    try:
        repo = ElasticsearchRepository()

        # Check cluster health (need direct client access for this)
        health = repo.client.cluster.health()
        print(f"✓ Elasticsearch is running at {settings.es_url}")
        print(f"  Cluster status: {health['status']}")
        print(f"  Number of nodes: {health['number_of_nodes']}")

        # Check if index exists
        if repo.index_exists():
            index_info = repo.client.indices.get(index=settings.es_index)
            doc_count = repo.client.count(index=settings.es_index)['count']
            print(f"\n✓ Index '{settings.es_index}' exists")
            print(f"  Document count: {doc_count}")

            # Get mapping info
            mapping = index_info[settings.es_index]['mappings']['properties']
            if 'embedding' in mapping:
                dims = mapping['embedding']['dims']
                print(f"  Embedding dimensions: {dims}")
        else:
            print(f"\n✗ Index '{settings.es_index}' does not exist")
            print(f"  Run 'make create-index' to create it")

    except Exception as e:
        print(f"✗ Error connecting to Elasticsearch at {settings.es_url}")
        print(f"  Error: {e}")
        print(f"\n  Make sure Elasticsearch is running:")
        print(f"    make elasticsearch")
        sys.exit(1)

if __name__ == "__main__":
    main()
