"""
Core PDF manipulation functions.

This module provides the fundamental operations for working with PDFs,
including merging, splitting, rotating, and extracting pages.
"""

from pathlib import Path
from typing import List, Sequence, Tuple, Union

from pypdf import PdfReader, PdfWriter

PathLike = Union[str, Path]


def _ensure_path(file: PathLike) -> Path:
    """Convert a path-like object to a resolved Path object."""
    return Path(file).expanduser().resolve()


def _ensure_paths(files: Sequence[PathLike]) -> List[Path]:
    """Convert a sequence of path-like objects to resolved Path objects."""
    return [_ensure_path(f) for f in files]


def merge(files: Sequence[PathLike], output: PathLike, *, preserve_metadata: bool = True) -> None:
    """
    Merge multiple PDF files into a single PDF.

    This function takes a list of PDF files and merges them in the order provided,
    creating a single output PDF file. Optionally preserves metadata from the first PDF.

    Args:
        files: A sequence of file paths to merge (in order)
        output: The output file path for the merged PDF
        preserve_metadata: If True, preserve metadata from the first PDF (default: True)

    Raises:
        FileNotFoundError: If any input file doesn't exist
        ValueError: If the files list is empty
        pypdf.errors.PdfReadError: If any input file is not a valid PDF

    Example:
        >>> merge(["doc1.pdf", "doc2.pdf", "doc3.pdf"], "combined.pdf")
    """
    if not files:
        raise ValueError("No input files provided")

    paths = _ensure_paths(files)
    output_path = _ensure_path(output)

    # Verify all input files exist
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {path}")

    writer = PdfWriter()

    # Add all pages from all PDFs
    for i, pdf_path in enumerate(paths):
        reader = PdfReader(pdf_path)

        # Preserve metadata from the first PDF if requested
        if i == 0 and preserve_metadata and reader.metadata:
            writer.add_metadata(reader.metadata)

        # Append all pages
        for page in reader.pages:
            writer.add_page(page)

    # Write the merged PDF
    with output_path.open("wb") as output_file:
        writer.write(output_file)


def merge_pattern(
    pattern: Sequence[Tuple[PathLike, int, int]], output: PathLike
) -> None:
    """
    Merge PDFs using a pattern of (file, start_page, end_page) tuples.

    This function allows fine-grained control over which pages from which files
    are merged. Pages are specified using 1-based indexing (like Adobe Reader),
    and ranges are inclusive on both ends.

    Args:
        pattern: A sequence of (file_path, start_page, end_page) tuples
                 where pages are 1-based and inclusive
        output: The output file path for the merged PDF

    Raises:
        FileNotFoundError: If any input file doesn't exist
        ValueError: If pattern is empty or page ranges are invalid
        IndexError: If page numbers are out of range

    Example:
        >>> pattern = [
        ...     ("A.pdf", 1, 5),   # Pages 1-5 from A.pdf
        ...     ("B.pdf", 1, 5),   # Pages 1-5 from B.pdf
        ...     ("A.pdf", 6, 10),  # Pages 6-10 from A.pdf
        ...     ("B.pdf", 6, 10),  # Pages 6-10 from B.pdf
        ... ]
        >>> merge_pattern(pattern, "output.pdf")
    """
    if not pattern:
        raise ValueError("No pattern provided")

    output_path = _ensure_path(output)
    writer = PdfWriter()

    # Cache readers to avoid reopening the same file multiple times
    reader_cache: dict[str, PdfReader] = {}

    for file_path, start_page, end_page in pattern:
        path = _ensure_path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {path}")

        if start_page < 1 or end_page < 1:
            raise ValueError(f"Page numbers must be >= 1, got: {start_page}-{end_page}")

        if start_page > end_page:
            raise ValueError(
                f"Start page ({start_page}) must be <= end page ({end_page})"
            )

        # Get or create cached reader
        path_str = str(path)
        if path_str not in reader_cache:
            reader_cache[path_str] = PdfReader(path)

        reader = reader_cache[path_str]
        total_pages = len(reader.pages)

        # Validate page range
        if end_page > total_pages:
            raise IndexError(
                f"Page range {start_page}-{end_page} exceeds total pages "
                f"({total_pages}) in {path.name}"
            )

        # Add pages (convert from 1-based to 0-based indexing)
        for page_num in range(start_page - 1, end_page):
            writer.add_page(reader.pages[page_num])

    # Write the merged PDF
    with output_path.open("wb") as output_file:
        writer.write(output_file)


def split_pdf(
    input_file: PathLike, output_dir: PathLike, *, pages_per_file: int = 1
) -> List[Path]:
    """
    Split a PDF into multiple files.

    Args:
        input_file: The input PDF file to split
        output_dir: Directory where split files will be saved
        pages_per_file: Number of pages per output file (default: 1)

    Returns:
        A list of paths to the created files

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If pages_per_file < 1

    Example:
        >>> split_pdf("large.pdf", "output_dir", pages_per_file=5)
        [Path('output_dir/large_001.pdf'), Path('output_dir/large_002.pdf'), ...]
    """
    if pages_per_file < 1:
        raise ValueError("pages_per_file must be >= 1")

    input_path = _ensure_path(input_file)
    output_path = _ensure_path(output_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    base_name = input_path.stem

    created_files = []
    file_num = 1

    for start_page in range(0, total_pages, pages_per_file):
        writer = PdfWriter()
        end_page = min(start_page + pages_per_file, total_pages)

        # Add pages to this split
        for page_num in range(start_page, end_page):
            writer.add_page(reader.pages[page_num])

        # Create output filename with zero-padded number
        output_file = output_path / f"{base_name}_{file_num:03d}.pdf"
        with output_file.open("wb") as f:
            writer.write(f)

        created_files.append(output_file)
        file_num += 1

    return created_files


def rotate_pages(
    input_file: PathLike,
    output_file: PathLike,
    rotation: int,
    *,
    pages: Union[Sequence[int], None] = None,
) -> None:
    """
    Rotate specific pages in a PDF.

    Args:
        input_file: The input PDF file
        output_file: The output PDF file
        rotation: Rotation angle in degrees (must be multiple of 90)
        pages: List of page numbers to rotate (1-based). If None, rotate all pages.

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If rotation is not a multiple of 90
        IndexError: If any page number is out of range

    Example:
        >>> rotate_pages("input.pdf", "output.pdf", 90, pages=[1, 3, 5])
    """
    if rotation % 90 != 0:
        raise ValueError("Rotation must be a multiple of 90 degrees")

    input_path = _ensure_path(input_file)
    output_path = _ensure_path(output_file)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    reader = PdfReader(input_path)
    writer = PdfWriter()
    total_pages = len(reader.pages)

    # If no pages specified, rotate all pages
    pages_to_rotate = set(pages) if pages else set(range(1, total_pages + 1))

    # Validate page numbers
    for page_num in pages_to_rotate:
        if page_num < 1 or page_num > total_pages:
            raise IndexError(f"Page number {page_num} is out of range (1-{total_pages})")

    # Process all pages
    for page_num in range(1, total_pages + 1):
        page = reader.pages[page_num - 1]

        if page_num in pages_to_rotate:
            page.rotate(rotation)

        writer.add_page(page)

    # Write the output PDF
    with output_path.open("wb") as f:
        writer.write(f)


def extract_pages(
    input_file: PathLike, output_file: PathLike, pages: Sequence[int]
) -> None:
    """
    Extract specific pages from a PDF into a new file.

    Args:
        input_file: The input PDF file
        output_file: The output PDF file
        pages: List of page numbers to extract (1-based)

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If pages list is empty
        IndexError: If any page number is out of range

    Example:
        >>> extract_pages("input.pdf", "output.pdf", [1, 3, 5, 7])
    """
    if not pages:
        raise ValueError("No pages specified for extraction")

    input_path = _ensure_path(input_file)
    output_path = _ensure_path(output_file)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    reader = PdfReader(input_path)
    writer = PdfWriter()
    total_pages = len(reader.pages)

    # Validate and extract pages
    for page_num in pages:
        if page_num < 1 or page_num > total_pages:
            raise IndexError(f"Page number {page_num} is out of range (1-{total_pages})")

        writer.add_page(reader.pages[page_num - 1])

    # Write the output PDF
    with output_path.open("wb") as f:
        writer.write(f)

