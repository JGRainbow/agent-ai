#!/usr/bin/env python3
"""
Script to index documents from the processed data directory into Elasticsearch.
"""
import sys
import os
import json
from pathlib import Path

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.adapters.elasticsearch_repository import ElasticsearchRepository
from src.retrieval.chunker import chunk_texts
from src.config import settings


def load_documents_from_directory(data_dir: str) -> list[dict]:
    """
    Load processed documents from directory.
    Expected format: Each file should contain text, with filename as doc_name.

    Args:
        data_dir: Path to directory containing processed text files

    Returns:
        List of document dictionaries with: {doc_name, text, source_url, date}
    """
    documents = []
    data_path = Path(data_dir)

    if not data_path.exists():
        print(f"Warning: Directory {data_dir} does not exist")
        return documents

    # Support .txt and .md files
    for file_path in data_path.rglob("*.txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
            if text:  # Only add non-empty documents
                # Extract metadata from filename or directory structure
                relative_path = file_path.relative_to(data_path)
                doc_name = str(relative_path).replace('/', '_')

                documents.append({
                    "doc_name": doc_name,
                    "text": text,
                    "source_url": "",  # TODO: Load from metadata file
                    "date": file_path.stat().st_mtime
                })

    for file_path in data_path.rglob("*.md"):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
            if text:
                relative_path = file_path.relative_to(data_path)
                doc_name = str(relative_path).replace('/', '_')

                documents.append({
                    "doc_name": doc_name,
                    "text": text,
                    "source_url": "",
                    "date": file_path.stat().st_mtime
                })

    return documents


def index_documents(documents: list[dict], repo: ElasticsearchRepository):
    """
    Chunk and index documents into Elasticsearch.

    Args:
        documents: List of documents to index
        repo: ElasticsearchRepository instance
    """
    print(f"Processing {len(documents)} documents...")

    all_chunks = []
    chunk_id_counter = 0

    for doc in documents:
        # Chunk the document
        chunks = chunk_texts(
            [doc["text"]],
            chunk_size=settings.default_chunk_size,
            overlap=settings.default_chunk_overlap
        )

        # Prepare chunks for indexing
        for chunk in chunks:
            all_chunks.append({
                "id": f"{doc['doc_name']}_{chunk['chunk_id']}",
                "doc_name": doc["doc_name"],
                "text": chunk["content"]
            })
            chunk_id_counter += 1

    print(f"Created {len(all_chunks)} chunks from {len(documents)} documents")

    # Index in batches (to avoid memory issues with large embeddings)
    batch_size = 50
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i + batch_size]
        print(f"Indexing batch {i//batch_size + 1}/{(len(all_chunks) + batch_size - 1)//batch_size}...")
        repo.index_documents(batch)

    print(f"✓ Successfully indexed {len(all_chunks)} chunks")


def main():
    """Main function to index documents."""
    import argparse

    parser = argparse.ArgumentParser(description="Index documents into Elasticsearch")
    parser.add_argument(
        "--data-dir",
        type=str,
        default="data/processed",
        help="Directory containing processed documents (default: data/processed)"
    )
    parser.add_argument(
        "--create-index",
        action="store_true",
        help="Create the index if it doesn't exist"
    )

    args = parser.parse_args()

    # Create repository
    repo = ElasticsearchRepository()

    # Create index if requested
    if args.create_index:
        print("Creating index...")
        repo.create_index_if_not_exists()

    # Check if index exists
    if not repo.index_exists():
        print("Error: Index does not exist. Run with --create-index to create it.")
        print("Or run: make create-index")
        sys.exit(1)

    # Load documents
    documents = load_documents_from_directory(args.data_dir)

    if not documents:
        print(f"No documents found in {args.data_dir}")
        print("Place .txt or .md files in the directory to index them.")
        sys.exit(1)

    # Index documents
    index_documents(documents, repo)

    print("\n✓ Indexing complete!")
    print(f"Index: {settings.es_index}")
    print(f"Documents indexed: {len(documents)}")


if __name__ == "__main__":
    main()
