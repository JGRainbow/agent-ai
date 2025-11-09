#!/usr/bin/env python3
"""
Simple script to extract text from a PDF file.
"""
import sys
import os
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    print("Error: pypdf not installed. Run: pip install pypdf")
    sys.exit(1)


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract all text from a PDF file.

    Args:
        pdf_path: Path to PDF file

    Returns:
        Extracted text as string
    """
    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    print(f"Extracting text from: {pdf_path}")

    reader = PdfReader(pdf_path)
    text_parts = []

    for page_num, page in enumerate(reader.pages, 1):
        text = page.extract_text()
        if text.strip():
            text_parts.append(text)
            print(f"  Extracted page {page_num} ({len(text)} characters)")

    full_text = "\n\n".join(text_parts)
    print(f"✓ Extracted {len(full_text)} total characters from {len(reader.pages)} pages")

    return full_text


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description="Extract text from PDF")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument(
        "-o", "--output",
        help="Output text file path (default: same as PDF with .txt extension)"
    )

    args = parser.parse_args()

    # Extract text
    text = extract_text_from_pdf(args.pdf_path)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(args.pdf_path).with_suffix('.txt')

    # Save to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"✓ Saved to: {output_path}")


if __name__ == "__main__":
    main()
