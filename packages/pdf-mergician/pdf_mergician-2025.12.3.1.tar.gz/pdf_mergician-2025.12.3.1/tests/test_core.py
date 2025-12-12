"""Tests for core PDF manipulation functions."""

import pytest
from pypdf import PdfReader, PdfWriter

from merge_pdf.core import (
    extract_pages,
    merge,
    merge_pattern,
    rotate_pages,
    split_pdf,
)


class TestMerge:
    """Tests for the merge function."""

    def test_merge_multiple_pdfs(self, multiple_pdfs, tmp_path):
        """Test merging multiple PDFs."""
        output = tmp_path / "merged.pdf"
        merge(multiple_pdfs, output)

        assert output.exists()
        reader = PdfReader(output)
        # Should have 3 + 5 + 2 = 10 pages
        assert len(reader.pages) == 10

    def test_merge_single_pdf(self, sample_pdf, tmp_path):
        """Test merging a single PDF."""
        output = tmp_path / "merged.pdf"
        merge([sample_pdf], output)

        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 1

    def test_merge_empty_list(self, tmp_path):
        """Test that merging empty list raises ValueError."""
        output = tmp_path / "merged.pdf"
        with pytest.raises(ValueError, match="No input files provided"):
            merge([], output)

    def test_merge_nonexistent_file(self, sample_pdf, tmp_path):
        """Test that merging with nonexistent file raises FileNotFoundError."""
        output = tmp_path / "merged.pdf"
        nonexistent = tmp_path / "nonexistent.pdf"

        with pytest.raises(FileNotFoundError):
            merge([sample_pdf, nonexistent], output)

    def test_merge_preserves_metadata(self, sample_pdf, tmp_path):
        """Test that metadata preservation works."""
        # Create a PDF with metadata
        pdf_with_metadata = tmp_path / "with_metadata.pdf"
        writer = PdfWriter()
        writer.add_blank_page(width=612, height=792)
        writer.add_metadata({"/Title": "Test Document", "/Author": "Test Author"})
        with pdf_with_metadata.open("wb") as f:
            writer.write(f)

        output = tmp_path / "merged.pdf"
        merge([pdf_with_metadata, sample_pdf], output, preserve_metadata=True)

        reader = PdfReader(output)
        assert reader.metadata is not None
        assert reader.metadata.get("/Title") == "Test Document"

    def test_merge_without_metadata(self, sample_pdf, tmp_path):
        """Test merging without preserving metadata."""
        output = tmp_path / "merged.pdf"
        merge([sample_pdf], output, preserve_metadata=False)

        assert output.exists()


class TestMergePattern:
    """Tests for the merge_pattern function."""

    def test_merge_pattern_basic(self, multi_page_pdf, tmp_path):
        """Test basic pattern merging."""
        output = tmp_path / "pattern.pdf"
        pattern = [(multi_page_pdf, 1, 3), (multi_page_pdf, 8, 10)]

        merge_pattern(pattern, output)

        assert output.exists()
        reader = PdfReader(output)
        # Should have 3 + 3 = 6 pages
        assert len(reader.pages) == 6

    def test_merge_pattern_interleave(self, multiple_pdfs, tmp_path):
        """Test interleaving pages from multiple PDFs."""
        output = tmp_path / "interleaved.pdf"
        doc1, doc2, _ = multiple_pdfs

        pattern = [
            (doc1, 1, 2),
            (doc2, 1, 2),
            (doc1, 3, 3),
            (doc2, 3, 3),
        ]

        merge_pattern(pattern, output)

        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 6

    def test_merge_pattern_single_page(self, multi_page_pdf, tmp_path):
        """Test extracting single pages with pattern."""
        output = tmp_path / "single.pdf"
        pattern = [(multi_page_pdf, 5, 5)]

        merge_pattern(pattern, output)

        reader = PdfReader(output)
        assert len(reader.pages) == 1

    def test_merge_pattern_empty(self, tmp_path):
        """Test that empty pattern raises ValueError."""
        output = tmp_path / "pattern.pdf"
        with pytest.raises(ValueError, match="No pattern provided"):
            merge_pattern([], output)

    def test_merge_pattern_invalid_page_range(self, multi_page_pdf, tmp_path):
        """Test that invalid page range raises ValueError."""
        output = tmp_path / "pattern.pdf"

        # Start page > end page
        with pytest.raises(ValueError, match="Start page.*must be <= end page"):
            merge_pattern([(multi_page_pdf, 5, 3)], output)

        # Page number < 1
        with pytest.raises(ValueError, match="Page numbers must be >= 1"):
            merge_pattern([(multi_page_pdf, 0, 5)], output)

    def test_merge_pattern_out_of_range(self, multi_page_pdf, tmp_path):
        """Test that out-of-range pages raise IndexError."""
        output = tmp_path / "pattern.pdf"

        with pytest.raises(IndexError, match="exceeds total pages"):
            merge_pattern([(multi_page_pdf, 1, 100)], output)

    def test_merge_pattern_nonexistent_file(self, tmp_path):
        """Test that nonexistent file raises FileNotFoundError."""
        output = tmp_path / "pattern.pdf"
        nonexistent = tmp_path / "nonexistent.pdf"

        with pytest.raises(FileNotFoundError):
            merge_pattern([(nonexistent, 1, 5)], output)


class TestSplitPdf:
    """Tests for the split_pdf function."""

    def test_split_single_page_per_file(self, multi_page_pdf, tmp_path):
        """Test splitting into individual pages."""
        output_dir = tmp_path / "split"
        files = split_pdf(multi_page_pdf, output_dir, pages_per_file=1)

        assert len(files) == 10
        for i, file_path in enumerate(files, start=1):
            assert file_path.exists()
            assert file_path.name == f"multi_page_{i:03d}.pdf"
            reader = PdfReader(file_path)
            assert len(reader.pages) == 1

    def test_split_multiple_pages_per_file(self, multi_page_pdf, tmp_path):
        """Test splitting into multi-page files."""
        output_dir = tmp_path / "split"
        files = split_pdf(multi_page_pdf, output_dir, pages_per_file=3)

        assert len(files) == 4  # 10 pages / 3 per file = 4 files
        # First three files should have 3 pages
        for file_path in files[:3]:
            reader = PdfReader(file_path)
            assert len(reader.pages) == 3
        # Last file should have 1 page (remainder)
        reader = PdfReader(files[-1])
        assert len(reader.pages) == 1

    def test_split_creates_output_dir(self, multi_page_pdf, tmp_path):
        """Test that output directory is created if it doesn't exist."""
        output_dir = tmp_path / "new_dir" / "split"
        files = split_pdf(multi_page_pdf, output_dir)

        assert output_dir.exists()
        assert len(files) == 10

    def test_split_invalid_pages_per_file(self, multi_page_pdf, tmp_path):
        """Test that invalid pages_per_file raises ValueError."""
        output_dir = tmp_path / "split"

        with pytest.raises(ValueError, match="pages_per_file must be >= 1"):
            split_pdf(multi_page_pdf, output_dir, pages_per_file=0)

    def test_split_nonexistent_file(self, tmp_path):
        """Test that nonexistent file raises FileNotFoundError."""
        nonexistent = tmp_path / "nonexistent.pdf"
        output_dir = tmp_path / "split"

        with pytest.raises(FileNotFoundError):
            split_pdf(nonexistent, output_dir)


class TestRotatePages:
    """Tests for the rotate_pages function."""

    def test_rotate_all_pages(self, multi_page_pdf, tmp_path):
        """Test rotating all pages."""
        output = tmp_path / "rotated.pdf"
        rotate_pages(multi_page_pdf, output, 90)

        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 10

    def test_rotate_specific_pages(self, multi_page_pdf, tmp_path):
        """Test rotating specific pages."""
        output = tmp_path / "rotated.pdf"
        rotate_pages(multi_page_pdf, output, 180, pages=[1, 3, 5])

        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 10

    def test_rotate_invalid_angle(self, multi_page_pdf, tmp_path):
        """Test that invalid rotation angle raises ValueError."""
        output = tmp_path / "rotated.pdf"

        with pytest.raises(ValueError, match="Rotation must be a multiple of 90"):
            rotate_pages(multi_page_pdf, output, 45)

    def test_rotate_out_of_range_page(self, multi_page_pdf, tmp_path):
        """Test that out-of-range page number raises IndexError."""
        output = tmp_path / "rotated.pdf"

        with pytest.raises(IndexError, match="out of range"):
            rotate_pages(multi_page_pdf, output, 90, pages=[100])

    def test_rotate_negative_angle(self, multi_page_pdf, tmp_path):
        """Test rotating with negative angle."""
        output = tmp_path / "rotated.pdf"
        rotate_pages(multi_page_pdf, output, -90)

        assert output.exists()

    def test_rotate_nonexistent_file(self, tmp_path):
        """Test that nonexistent file raises FileNotFoundError."""
        nonexistent = tmp_path / "nonexistent.pdf"
        output = tmp_path / "rotated.pdf"

        with pytest.raises(FileNotFoundError):
            rotate_pages(nonexistent, output, 90)


class TestExtractPages:
    """Tests for the extract_pages function."""

    def test_extract_single_page(self, multi_page_pdf, tmp_path):
        """Test extracting a single page."""
        output = tmp_path / "extracted.pdf"
        extract_pages(multi_page_pdf, output, [5])

        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 1

    def test_extract_multiple_pages(self, multi_page_pdf, tmp_path):
        """Test extracting multiple pages."""
        output = tmp_path / "extracted.pdf"
        extract_pages(multi_page_pdf, output, [1, 3, 5, 7, 9])

        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 5

    def test_extract_pages_in_order(self, multi_page_pdf, tmp_path):
        """Test that pages are extracted in the specified order."""
        output = tmp_path / "extracted.pdf"
        extract_pages(multi_page_pdf, output, [10, 5, 1])

        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 3

    def test_extract_empty_list(self, multi_page_pdf, tmp_path):
        """Test that empty page list raises ValueError."""
        output = tmp_path / "extracted.pdf"

        with pytest.raises(ValueError, match="No pages specified"):
            extract_pages(multi_page_pdf, output, [])

    def test_extract_out_of_range(self, multi_page_pdf, tmp_path):
        """Test that out-of-range page raises IndexError."""
        output = tmp_path / "extracted.pdf"

        with pytest.raises(IndexError, match="out of range"):
            extract_pages(multi_page_pdf, output, [1, 100])

    def test_extract_nonexistent_file(self, tmp_path):
        """Test that nonexistent file raises FileNotFoundError."""
        nonexistent = tmp_path / "nonexistent.pdf"
        output = tmp_path / "extracted.pdf"

        with pytest.raises(FileNotFoundError):
            extract_pages(nonexistent, output, [1])

