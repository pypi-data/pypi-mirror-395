"""
pdf-mergician: A powerful CLI-first PDF merging and manipulation tool.

This package provides both a command-line interface and a Python API
for merging, splitting, and manipulating PDF files with ease.

Public API:
    - merge: Merge multiple PDFs into a single file
    - merge_pattern: Merge specific page ranges from multiple PDFs
    - split_pdf: Split a PDF into multiple files
    - rotate_pages: Rotate specific pages in a PDF
    - extract_pages: Extract specific pages from a PDF
"""

from merge_pdf.core import (
    extract_pages,
    merge,
    merge_pattern,
    rotate_pages,
    split_pdf,
)

__version__ = "2025.12.03.1"
__all__ = [
    "merge",
    "merge_pattern",
    "split_pdf",
    "rotate_pages",
    "extract_pages",
]

