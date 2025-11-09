import re
from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_texts(texts: List[str], chunk_size: int, overlap: int) -> List[Dict[str, Any]]:
    """
    Split texts into chunks with sentence boundary awareness.

    Args:
        texts: List of text strings to chunk
        chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks

    Returns:
        List of dictionaries with: {chunk_id: str, content: str}
    """
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", "? ", "! ", "; "],
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len,
        is_separator_regex=False
    )

    chunks = []
    chunk_id = 0

    for text in texts:
        pieces = splitter.split_text(text)

        # Post-process: ensure punctuation ends sentences
        fixed_pieces = []
        for p in pieces:
            p = p.strip()
            if not re.search(r'[.!?]"?$', p):
                p += "."
            fixed_pieces.append(p)

        for piece in fixed_pieces:
            chunks.append({"chunk_id": str(chunk_id), "content": piece})
            chunk_id += 1

    return chunks
