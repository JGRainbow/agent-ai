#!/usr/bin/env python3
"""
Script to list all Elasticsearch indices.
"""
import sys
import os

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.adapters.elasticsearch_repository import ElasticsearchRepository
from src.config import settings

def main():
    """List all indices in Elasticsearch."""
    try:
        repo = ElasticsearchRepository()
        indices = repo.client.indices.get_alias(index="*")
        print(f"Elasticsearch indices at {settings.es_url}:\n")

        if not indices:
            print("  No indices found")
        else:
            for index_name in sorted(indices.keys()):
                # Skip system indices
                if index_name.startswith('.'):
                    continue

                try:
                    stats = repo.client.indices.stats(index=index_name)
                    doc_count = stats['indices'][index_name]['total']['docs']['count']
                    size = stats['indices'][index_name]['total']['store']['size_in_bytes']
                    size_mb = size / (1024 * 1024)
                    print(f"  {index_name}")
                    print(f"    Documents: {doc_count:,}")
                    print(f"    Size: {size_mb:.2f} MB")
                except Exception as e:
                    print(f"  {index_name} (error getting stats: {e})")
                print()

    except Exception as e:
        print(f"✗ Error connecting to Elasticsearch at {settings.es_url}")
        print(f"  Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
