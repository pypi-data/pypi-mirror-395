"""Integration tests for CLI with real PDF fixtures."""

from pathlib import Path

import pytest
from click.testing import CliRunner
from pypdf import PdfReader, PdfWriter

from merge_pdf.cli import cli


@pytest.fixture(scope="module")
def fixtures_dir():
    """Get the fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture(scope="module")
def test_pdfs(fixtures_dir):
    """Create test PDF fixtures if they don't exist."""
    fixtures_dir.mkdir(exist_ok=True)

    # Create test PDFs
    pdfs = {
        "doc_a.pdf": 10,
        "doc_b.pdf": 10,
        "doc_c.pdf": 5,
        "small.pdf": 3,
        "single.pdf": 1,
    }

    created_pdfs = {}
    for filename, num_pages in pdfs.items():
        pdf_path = fixtures_dir / filename
        if not pdf_path.exists():
            writer = PdfWriter()
            for _ in range(num_pages):
                writer.add_blank_page(width=612, height=792)
            with pdf_path.open("wb") as f:
                writer.write(f)
        created_pdfs[filename] = pdf_path

    return created_pdfs


@pytest.fixture
def runner():
    """Create a Click CLI test runner."""
    return CliRunner()


class TestMergeIntegration:
    """Integration tests for merge command with real PDFs."""

    def test_merge_multiple_documents(self, runner, test_pdfs, tmp_path):
        """Test merging multiple documents."""
        output = tmp_path / "merged.pdf"
        result = runner.invoke(
            cli,
            [
                "merge",
                str(output),
                str(test_pdfs["doc_a.pdf"]),
                str(test_pdfs["doc_b.pdf"]),
                str(test_pdfs["small.pdf"]),
            ],
        )

        assert result.exit_code == 0
        assert "Created" in result.output
        assert output.exists()

        # Verify merged PDF has correct number of pages
        reader = PdfReader(output)
        assert len(reader.pages) == 23  # 10 + 10 + 3

    def test_merge_with_multiple_files(self, runner, test_pdfs, tmp_path):
        """Test merging with multiple files from same directory."""
        output = tmp_path / "merged.pdf"
        fixtures_dir = test_pdfs["doc_a.pdf"].parent

        # Manually expand the glob (shell would do this normally)
        doc_files = sorted(fixtures_dir.glob("doc_*.pdf"))
        result = runner.invoke(
            cli, ["merge", str(output)] + [str(f) for f in doc_files]
        )

        assert result.exit_code == 0
        assert output.exists()

        # Should have merged doc_a, doc_b, doc_c
        reader = PdfReader(output)
        assert len(reader.pages) == 25  # 10 + 10 + 5

    def test_merge_preserves_page_content(self, runner, test_pdfs, tmp_path):
        """Test that merge preserves page content."""
        output = tmp_path / "merged.pdf"
        result = runner.invoke(
            cli,
            [
                "merge",
                str(output),
                str(test_pdfs["single.pdf"]),
                str(test_pdfs["small.pdf"]),
            ],
        )

        assert result.exit_code == 0
        reader = PdfReader(output)
        assert len(reader.pages) == 4  # 1 + 3


class TestPatternIntegration:
    """Integration tests for pattern command with real PDFs."""

    def test_pattern_interleave_pages(self, runner, test_pdfs, tmp_path):
        """Test interleaving pages from two documents."""
        output = tmp_path / "interleaved.pdf"
        doc_a = str(test_pdfs["doc_a.pdf"])
        doc_b = str(test_pdfs["doc_b.pdf"])

        result = runner.invoke(
            cli,
            [
                "pattern",
                str(output),
                "-s",
                f"{doc_a}:1-5",
                "-s",
                f"{doc_b}:1-5",
                "-s",
                f"{doc_a}:6-10",
                "-s",
                f"{doc_b}:6-10",
            ],
        )

        assert result.exit_code == 0
        assert "Created" in result.output
        reader = PdfReader(output)
        assert len(reader.pages) == 20  # 5 + 5 + 5 + 5

    def test_pattern_extract_specific_pages(self, runner, test_pdfs, tmp_path):
        """Test extracting specific pages with pattern."""
        output = tmp_path / "extracted.pdf"
        doc_a = str(test_pdfs["doc_a.pdf"])

        result = runner.invoke(
            cli, ["pattern", str(output), "-s", f"{doc_a}:1-3", "-s", f"{doc_a}:8-10"]
        )

        assert result.exit_code == 0
        reader = PdfReader(output)
        assert len(reader.pages) == 6  # 3 + 3

    def test_pattern_single_pages(self, runner, test_pdfs, tmp_path):
        """Test extracting single pages from multiple documents."""
        output = tmp_path / "covers.pdf"

        result = runner.invoke(
            cli,
            [
                "pattern",
                str(output),
                "-s",
                f"{test_pdfs['doc_a.pdf']}:1-1",
                "-s",
                f"{test_pdfs['doc_b.pdf']}:1-1",
                "-s",
                f"{test_pdfs['doc_c.pdf']}:1-1",
            ],
        )

        assert result.exit_code == 0
        reader = PdfReader(output)
        assert len(reader.pages) == 3

    def test_pattern_complex_combination(self, runner, test_pdfs, tmp_path):
        """Test complex pattern with multiple files and ranges."""
        output = tmp_path / "complex.pdf"

        result = runner.invoke(
            cli,
            [
                "pattern",
                str(output),
                "-s",
                f"{test_pdfs['single.pdf']}:1-1",  # 1 page
                "-s",
                f"{test_pdfs['small.pdf']}:1-3",  # 3 pages
                "-s",
                f"{test_pdfs['doc_c.pdf']}:2-4",  # 3 pages
            ],
        )

        assert result.exit_code == 0
        reader = PdfReader(output)
        assert len(reader.pages) == 7


class TestSplitIntegration:
    """Integration tests for split command with real PDFs."""

    def test_split_into_individual_pages(self, runner, test_pdfs, tmp_path):
        """Test splitting into individual pages."""
        output_dir = tmp_path / "split"
        result = runner.invoke(
            cli, ["split", str(test_pdfs["small.pdf"]), str(output_dir)]
        )

        assert result.exit_code == 0
        assert "Created 3 file(s)" in result.output

        # Verify all files were created
        split_files = list(output_dir.glob("*.pdf"))
        assert len(split_files) == 3

        # Verify each file has 1 page
        for pdf_file in split_files:
            reader = PdfReader(pdf_file)
            assert len(reader.pages) == 1

    def test_split_into_chunks(self, runner, test_pdfs, tmp_path):
        """Test splitting into multi-page chunks."""
        output_dir = tmp_path / "chunks"
        result = runner.invoke(
            cli,
            [
                "split",
                str(test_pdfs["doc_a.pdf"]),
                str(output_dir),
                "--pages-per-file",
                "3",
            ],
        )

        assert result.exit_code == 0
        split_files = list(output_dir.glob("*.pdf"))
        assert len(split_files) == 4  # 10 pages / 3 per file = 4 files

        # Verify page counts
        for i, pdf_file in enumerate(sorted(split_files)):
            reader = PdfReader(pdf_file)
            if i < 3:
                assert len(reader.pages) == 3
            else:
                assert len(reader.pages) == 1  # Last file has remainder

    def test_split_large_document(self, runner, test_pdfs, tmp_path):
        """Test splitting a larger document."""
        output_dir = tmp_path / "split_large"
        result = runner.invoke(
            cli,
            [
                "split",
                str(test_pdfs["doc_b.pdf"]),
                str(output_dir),
                "-p",
                "5",
            ],
        )

        assert result.exit_code == 0
        split_files = list(output_dir.glob("*.pdf"))
        assert len(split_files) == 2  # 10 pages / 5 per file = 2 files


class TestRotateIntegration:
    """Integration tests for rotate command with real PDFs."""

    def test_rotate_all_pages_90(self, runner, test_pdfs, tmp_path):
        """Test rotating all pages 90 degrees."""
        output = tmp_path / "rotated.pdf"
        result = runner.invoke(
            cli,
            [
                "rotate",
                str(test_pdfs["small.pdf"]),
                str(output),
                "--angle",
                "90",
            ],
        )

        assert result.exit_code == 0
        assert "Created" in result.output
        assert output.exists()

        reader = PdfReader(output)
        assert len(reader.pages) == 3

    def test_rotate_specific_pages(self, runner, test_pdfs, tmp_path):
        """Test rotating specific pages."""
        output = tmp_path / "rotated.pdf"
        result = runner.invoke(
            cli,
            [
                "rotate",
                str(test_pdfs["doc_c.pdf"]),
                str(output),
                "--angle",
                "180",
                "--pages",
                "1,3,5",
            ],
        )

        assert result.exit_code == 0
        reader = PdfReader(output)
        assert len(reader.pages) == 5

    def test_rotate_counter_clockwise(self, runner, test_pdfs, tmp_path):
        """Test counter-clockwise rotation."""
        output = tmp_path / "rotated.pdf"
        result = runner.invoke(
            cli,
            [
                "rotate",
                str(test_pdfs["single.pdf"]),
                str(output),
                "--angle",
                "-90",
            ],
        )

        assert result.exit_code == 0
        assert output.exists()


class TestExtractIntegration:
    """Integration tests for extract command with real PDFs."""

    def test_extract_single_page(self, runner, test_pdfs, tmp_path):
        """Test extracting a single page."""
        output = tmp_path / "extracted.pdf"
        result = runner.invoke(
            cli,
            [
                "extract",
                str(test_pdfs["doc_a.pdf"]),
                str(output),
                "--pages",
                "5",
            ],
        )

        assert result.exit_code == 0
        reader = PdfReader(output)
        assert len(reader.pages) == 1

    def test_extract_multiple_pages(self, runner, test_pdfs, tmp_path):
        """Test extracting multiple specific pages."""
        output = tmp_path / "extracted.pdf"
        result = runner.invoke(
            cli,
            [
                "extract",
                str(test_pdfs["doc_a.pdf"]),
                str(output),
                "--pages",
                "1,3,5,7,9",
            ],
        )

        assert result.exit_code == 0
        reader = PdfReader(output)
        assert len(reader.pages) == 5

    def test_extract_range(self, runner, test_pdfs, tmp_path):
        """Test extracting a range of pages."""
        output = tmp_path / "extracted.pdf"
        result = runner.invoke(
            cli,
            [
                "extract",
                str(test_pdfs["doc_b.pdf"]),
                str(output),
                "--pages",
                "3-7",
            ],
        )

        assert result.exit_code == 0
        reader = PdfReader(output)
        assert len(reader.pages) == 5

    def test_extract_mixed_format(self, runner, test_pdfs, tmp_path):
        """Test extracting with mixed page specification."""
        output = tmp_path / "extracted.pdf"
        result = runner.invoke(
            cli,
            [
                "extract",
                str(test_pdfs["doc_a.pdf"]),
                str(output),
                "--pages",
                "1,3-5,8-10",
            ],
        )

        assert result.exit_code == 0
        reader = PdfReader(output)
        assert len(reader.pages) == 7  # 1 + (3,4,5) + (8,9,10)

    def test_extract_all_pages_in_range(self, runner, test_pdfs, tmp_path):
        """Test extracting all pages using range."""
        output = tmp_path / "extracted.pdf"
        result = runner.invoke(
            cli,
            [
                "extract",
                str(test_pdfs["small.pdf"]),
                str(output),
                "--pages",
                "1-3",
            ],
        )

        assert result.exit_code == 0
        reader = PdfReader(output)
        assert len(reader.pages) == 3


class TestCLIErrorHandling:
    """Test CLI error handling with real PDFs."""

    def test_merge_with_invalid_pdf(self, runner, tmp_path):
        """Test merge with invalid PDF file."""
        # Create a fake PDF file
        fake_pdf = tmp_path / "fake.pdf"
        fake_pdf.write_text("This is not a PDF")

        output = tmp_path / "output.pdf"
        result = runner.invoke(cli, ["merge", str(output), str(fake_pdf)])

        assert result.exit_code != 0

    def test_pattern_out_of_range_pages(self, runner, test_pdfs, tmp_path):
        """Test pattern with out-of-range pages."""
        output = tmp_path / "output.pdf"
        result = runner.invoke(
            cli,
            [
                "pattern",
                str(output),
                "-s",
                f"{test_pdfs['small.pdf']}:1-100",  # Only 3 pages
            ],
        )

        assert result.exit_code != 0
        assert "exceeds total pages" in result.output.lower()

    def test_extract_invalid_page_numbers(self, runner, test_pdfs, tmp_path):
        """Test extract with invalid page numbers."""
        output = tmp_path / "output.pdf"
        result = runner.invoke(
            cli,
            [
                "extract",
                str(test_pdfs["small.pdf"]),
                str(output),
                "--pages",
                "1,50",  # Page 50 doesn't exist
            ],
        )

        assert result.exit_code != 0

    def test_rotate_invalid_angle(self, runner, test_pdfs, tmp_path):
        """Test rotate with invalid angle."""
        output = tmp_path / "output.pdf"
        result = runner.invoke(
            cli,
            [
                "rotate",
                str(test_pdfs["single.pdf"]),
                str(output),
                "--angle",
                "45",  # Not a valid angle
            ],
        )

        assert result.exit_code != 0


class TestCLIWorkflows:
    """Test complete workflows with real PDFs."""

    def test_workflow_merge_split_extract(self, runner, test_pdfs, tmp_path):
        """Test a complete workflow: merge, split, then extract."""
        # Step 1: Merge
        merged = tmp_path / "merged.pdf"
        result = runner.invoke(
            cli,
            [
                "merge",
                str(merged),
                str(test_pdfs["doc_a.pdf"]),
                str(test_pdfs["doc_b.pdf"]),
            ],
        )
        assert result.exit_code == 0

        # Step 2: Split
        split_dir = tmp_path / "split"
        result = runner.invoke(
            cli, ["split", str(merged), str(split_dir), "-p", "5"]
        )
        assert result.exit_code == 0

        # Step 3: Extract from one of the split files
        split_files = sorted(split_dir.glob("*.pdf"))
        extracted = tmp_path / "extracted.pdf"
        result = runner.invoke(
            cli, ["extract", str(split_files[0]), str(extracted), "--pages", "1-3"]
        )
        assert result.exit_code == 0

        reader = PdfReader(extracted)
        assert len(reader.pages) == 3

    def test_workflow_pattern_rotate(self, runner, test_pdfs, tmp_path):
        """Test pattern merge followed by rotation."""
        # Step 1: Pattern merge
        pattern_output = tmp_path / "pattern.pdf"
        result = runner.invoke(
            cli,
            [
                "pattern",
                str(pattern_output),
                "-s",
                f"{test_pdfs['doc_a.pdf']}:1-5",
                "-s",
                f"{test_pdfs['doc_b.pdf']}:1-5",
            ],
        )
        assert result.exit_code == 0

        # Step 2: Rotate specific pages
        rotated = tmp_path / "rotated.pdf"
        result = runner.invoke(
            cli,
            [
                "rotate",
                str(pattern_output),
                str(rotated),
                "--angle",
                "90",
                "--pages",
                "1,5,10",
            ],
        )
        assert result.exit_code == 0

        reader = PdfReader(rotated)
        assert len(reader.pages) == 10

