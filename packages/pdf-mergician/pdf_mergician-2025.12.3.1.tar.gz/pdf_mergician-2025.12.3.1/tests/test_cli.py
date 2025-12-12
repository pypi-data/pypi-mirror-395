"""Tests for CLI commands."""

import re

import pytest
from click.testing import CliRunner
from pypdf import PdfReader, PdfWriter

from merge_pdf.cli import cli


@pytest.fixture
def runner():
    """Create a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def sample_pdfs(tmp_path):
    """Create sample PDFs for CLI testing."""
    pdfs = []
    for i in range(3):
        pdf_path = tmp_path / f"test{i+1}.pdf"
        writer = PdfWriter()
        for _ in range(5):
            writer.add_blank_page(width=612, height=792)
        with pdf_path.open("wb") as f:
            writer.write(f)
        pdfs.append(pdf_path)
    return pdfs


class TestMergeCommand:
    """Tests for the merge command."""

    def test_merge_basic(self, runner, sample_pdfs, tmp_path):
        """Test basic merge command."""
        output = tmp_path / "output.pdf"
        result = runner.invoke(
            cli, ["merge", str(output)] + [str(p) for p in sample_pdfs]
        )

        assert result.exit_code == 0
        assert "Created" in result.output
        assert output.exists()

        reader = PdfReader(output)
        assert len(reader.pages) == 15  # 3 PDFs × 5 pages

    def test_merge_no_files(self, runner, tmp_path):
        """Test merge with no input files."""
        output = tmp_path / "output.pdf"
        result = runner.invoke(cli, ["merge", str(output)])

        assert result.exit_code != 0
        # Click provides its own error message for missing required arguments
        assert "Missing argument" in result.output or "FILES" in result.output

    def test_merge_nonexistent_file(self, runner, sample_pdfs, tmp_path):
        """Test merge with nonexistent file."""
        output = tmp_path / "output.pdf"
        nonexistent = tmp_path / "nonexistent.pdf"

        result = runner.invoke(
            cli, ["merge", str(output), str(sample_pdfs[0]), str(nonexistent)]
        )

        assert result.exit_code != 0
        # Click validates file existence and provides its own error message
        assert "does not exist" in result.output.lower() or "not found" in result.output.lower()

    def test_merge_no_metadata(self, runner, sample_pdfs, tmp_path):
        """Test merge with --no-metadata flag."""
        output = tmp_path / "output.pdf"
        result = runner.invoke(
            cli, ["merge", str(output), "--no-metadata"] + [str(p) for p in sample_pdfs]
        )

        assert result.exit_code == 0
        assert output.exists()

    def test_merge_help(self, runner):
        """Test merge command help."""
        result = runner.invoke(cli, ["merge", "--help"])

        assert result.exit_code == 0
        assert "Merge multiple PDF files" in result.output


class TestPatternCommand:
    """Tests for the pattern command."""

    def test_pattern_basic(self, runner, sample_pdfs, tmp_path):
        """Test basic pattern command."""
        output = tmp_path / "output.pdf"
        result = runner.invoke(
            cli,
            [
                "pattern",
                str(output),
                "-s",
                f"{sample_pdfs[0]}:1-3",
                "-s",
                f"{sample_pdfs[1]}:1-2",
            ],
        )

        assert result.exit_code == 0
        assert "Created" in result.output
        assert output.exists()

        reader = PdfReader(output)
        assert len(reader.pages) == 5  # 3 + 2 pages

    def test_pattern_single_page(self, runner, sample_pdfs, tmp_path):
        """Test pattern with single page specification."""
        output = tmp_path / "output.pdf"
        result = runner.invoke(
            cli, ["pattern", str(output), "-s", f"{sample_pdfs[0]}:1-1"]
        )

        assert result.exit_code == 0
        reader = PdfReader(output)
        assert len(reader.pages) == 1

    def test_pattern_no_specs(self, runner, tmp_path):
        """Test pattern with no specifications."""
        output = tmp_path / "output.pdf"
        result = runner.invoke(cli, ["pattern", str(output)])

        assert result.exit_code != 0

    def test_pattern_invalid_format(self, runner, sample_pdfs, tmp_path):
        """Test pattern with invalid format."""
        output = tmp_path / "output.pdf"
        result = runner.invoke(
            cli, ["pattern", str(output), "-s", "invalid_format"]
        )

        assert result.exit_code != 0

    def test_pattern_help(self, runner):
        """Test pattern command help."""
        result = runner.invoke(cli, ["pattern", "--help"])

        assert result.exit_code == 0
        assert "advanced pattern" in result.output.lower()


class TestSplitCommand:
    """Tests for the split command."""

    def test_split_basic(self, runner, sample_pdfs, tmp_path):
        """Test basic split command."""
        output_dir = tmp_path / "split"
        result = runner.invoke(cli, ["split", str(sample_pdfs[0]), str(output_dir)])

        assert result.exit_code == 0
        assert "Created" in result.output
        assert output_dir.exists()

        # Should create 5 files (1 page each)
        split_files = list(output_dir.glob("*.pdf"))
        assert len(split_files) == 5

    def test_split_with_pages_per_file(self, runner, sample_pdfs, tmp_path):
        """Test split with custom pages per file."""
        output_dir = tmp_path / "split"
        result = runner.invoke(
            cli,
            ["split", str(sample_pdfs[0]), str(output_dir), "--pages-per-file", "2"],
        )

        assert result.exit_code == 0

        split_files = list(output_dir.glob("*.pdf"))
        assert len(split_files) == 3  # 5 pages / 2 per file = 3 files

    def test_split_nonexistent_file(self, runner, tmp_path):
        """Test split with nonexistent file."""
        nonexistent = tmp_path / "nonexistent.pdf"
        output_dir = tmp_path / "split"

        result = runner.invoke(cli, ["split", str(nonexistent), str(output_dir)])

        assert result.exit_code != 0

    def test_split_help(self, runner):
        """Test split command help."""
        result = runner.invoke(cli, ["split", "--help"])

        assert result.exit_code == 0
        assert "Split a PDF" in result.output


class TestRotateCommand:
    """Tests for the rotate command."""

    def test_rotate_all_pages(self, runner, sample_pdfs, tmp_path):
        """Test rotating all pages."""
        output = tmp_path / "rotated.pdf"
        result = runner.invoke(
            cli, ["rotate", str(sample_pdfs[0]), str(output), "--angle", "90"]
        )

        assert result.exit_code == 0
        assert "Created" in result.output
        assert output.exists()

    def test_rotate_specific_pages(self, runner, sample_pdfs, tmp_path):
        """Test rotating specific pages."""
        output = tmp_path / "rotated.pdf"
        result = runner.invoke(
            cli,
            [
                "rotate",
                str(sample_pdfs[0]),
                str(output),
                "--angle",
                "180",
                "--pages",
                "1,3,5",
            ],
        )

        assert result.exit_code == 0
        assert output.exists()

    def test_rotate_negative_angle(self, runner, sample_pdfs, tmp_path):
        """Test rotating with negative angle."""
        output = tmp_path / "rotated.pdf"
        result = runner.invoke(
            cli, ["rotate", str(sample_pdfs[0]), str(output), "--angle", "-90"]
        )

        assert result.exit_code == 0
        assert output.exists()

    def test_rotate_no_angle(self, runner, sample_pdfs, tmp_path):
        """Test rotate without angle (should fail)."""
        output = tmp_path / "rotated.pdf"
        result = runner.invoke(cli, ["rotate", str(sample_pdfs[0]), str(output)])

        assert result.exit_code != 0

    def test_rotate_invalid_pages(self, runner, sample_pdfs, tmp_path):
        """Test rotate with invalid page specification."""
        output = tmp_path / "rotated.pdf"
        result = runner.invoke(
            cli,
            [
                "rotate",
                str(sample_pdfs[0]),
                str(output),
                "--angle",
                "90",
                "--pages",
                "invalid",
            ],
        )

        assert result.exit_code != 0

    def test_rotate_help(self, runner):
        """Test rotate command help."""
        result = runner.invoke(cli, ["rotate", "--help"])

        assert result.exit_code == 0
        assert "Rotate pages" in result.output


class TestExtractCommand:
    """Tests for the extract command."""

    def test_extract_single_page(self, runner, sample_pdfs, tmp_path):
        """Test extracting a single page."""
        output = tmp_path / "extracted.pdf"
        result = runner.invoke(
            cli, ["extract", str(sample_pdfs[0]), str(output), "--pages", "3"]
        )

        assert result.exit_code == 0
        assert output.exists()

        reader = PdfReader(output)
        assert len(reader.pages) == 1

    def test_extract_multiple_pages(self, runner, sample_pdfs, tmp_path):
        """Test extracting multiple pages."""
        output = tmp_path / "extracted.pdf"
        result = runner.invoke(
            cli, ["extract", str(sample_pdfs[0]), str(output), "--pages", "1,3,5"]
        )

        assert result.exit_code == 0

        reader = PdfReader(output)
        assert len(reader.pages) == 3

    def test_extract_range(self, runner, sample_pdfs, tmp_path):
        """Test extracting a range of pages."""
        output = tmp_path / "extracted.pdf"
        result = runner.invoke(
            cli, ["extract", str(sample_pdfs[0]), str(output), "--pages", "2-4"]
        )

        assert result.exit_code == 0

        reader = PdfReader(output)
        assert len(reader.pages) == 3

    def test_extract_mixed_format(self, runner, sample_pdfs, tmp_path):
        """Test extracting with mixed page specification."""
        output = tmp_path / "extracted.pdf"
        result = runner.invoke(
            cli, ["extract", str(sample_pdfs[0]), str(output), "--pages", "1,3-5"]
        )

        assert result.exit_code == 0

        reader = PdfReader(output)
        assert len(reader.pages) == 4  # Pages 1, 3, 4, 5

    def test_extract_no_pages(self, runner, sample_pdfs, tmp_path):
        """Test extract without page specification."""
        output = tmp_path / "extracted.pdf"
        result = runner.invoke(cli, ["extract", str(sample_pdfs[0]), str(output)])

        assert result.exit_code != 0

    def test_extract_invalid_range(self, runner, sample_pdfs, tmp_path):
        """Test extract with invalid range."""
        output = tmp_path / "extracted.pdf"
        result = runner.invoke(
            cli, ["extract", str(sample_pdfs[0]), str(output), "--pages", "5-2"]
        )

        assert result.exit_code != 0

    def test_extract_help(self, runner):
        """Test extract command help."""
        result = runner.invoke(cli, ["extract", "--help"])

        assert result.exit_code == 0
        assert "Extract specific pages" in result.output


class TestCLIGeneral:
    """Tests for general CLI functionality."""

    def test_version(self, runner):
        """Test version flag."""
        result = runner.invoke(cli, ["--version"])

        assert result.exit_code == 0
        assert "pdf-mergician" in result.output
        # Version should be in YYYY.MM.DD.x format
        assert re.search(r"\d{4}\.\d{2}\.\d{2}\.\d+", result.output)

    def test_help(self, runner):
        """Test help flag."""
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "pdf-mergician" in result.output.lower()
        assert "pdf manipulation" in result.output.lower()

    def test_no_command(self, runner):
        """Test running without a command."""
        result = runner.invoke(cli, [])

        assert result.exit_code == 0
        # Should show help
        assert "pdf-mergician" in result.output

