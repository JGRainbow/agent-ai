#!/usr/bin/env python3
"""
Quick script to index a single PDF file.
Usage: python scripts/index_single_pdf.py path/to/document.pdf
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.adapters.elasticsearch_repository import ElasticsearchRepository
from src.retrieval.chunker import chunk_texts
from src.config import settings

try:
    from pypdf import PdfReader
except ImportError:
    print("Error: pypdf not installed. Run: pip install pypdf")
    sys.exit(1)


def extract_pdf_text(pdf_path: str) -> str:
    """Extract text from PDF."""
    reader = PdfReader(pdf_path)
    text_parts = []

    for page in reader.pages:
        text = page.extract_text()
        if text.strip():
            text_parts.append(text)

    return "\n\n".join(text_parts)


def main():
    """Index a single PDF file."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/index_single_pdf.py <path_to_pdf>")
        print("Example: python scripts/index_single_pdf.py data/raw/name_change_guide.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]
    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)

    print(f"Processing PDF: {pdf_path}")

    # Extract text
    print("Extracting text from PDF...")
    text = extract_pdf_text(pdf_path)

    if not text.strip():
        print("Error: No text extracted from PDF")
        sys.exit(1)

    print(f"✓ Extracted {len(text)} characters")

    # Create repository
    repo = ElasticsearchRepository()

    # Create index if needed
    if not repo.index_exists():
        print("Creating index...")
        repo.create_index_if_not_exists()
    else:
        print("Index already exists")

    # Get document name from filename
    doc_name = pdf_file.stem

    # Chunk the document
    print("Chunking document...")
    chunks = chunk_texts(
        [text],
        chunk_size=settings.default_chunk_size,
        overlap=settings.default_chunk_overlap
    )

    print(f"✓ Created {len(chunks)} chunks")

    # Prepare for indexing
    indexed_chunks = []
    for chunk in chunks:
        indexed_chunks.append({
            "id": f"{doc_name}_{chunk['chunk_id']}",
            "doc_name": doc_name,
            "text": chunk["content"]
        })

    # Index in batches
    print("Indexing chunks...")
    batch_size = 50
    for i in range(0, len(indexed_chunks), batch_size):
        batch = indexed_chunks[i:i + batch_size]
        print(f"  Indexing batch {i//batch_size + 1}/{(len(indexed_chunks) + batch_size - 1)//batch_size}...")
        repo.index_documents(batch)

    print(f"\n✓ Successfully indexed {len(indexed_chunks)} chunks from '{doc_name}'")
    print(f"  Index: {settings.es_index}")
    print(f"\nYou can now query the API with questions about this document!")


if __name__ == "__main__":
    main()
