"""
Command-line interface for pdf-mergician.

This module provides a user-friendly CLI for all PDF manipulation operations,
built with Click for a professional and intuitive experience.
"""

import sys
from pathlib import Path
from typing import List, Optional, Tuple

import click

from merge_pdf import __version__
from merge_pdf.core import extract_pages, merge, merge_pattern, rotate_pages, split_pdf


# Custom Click types for better validation
class PageRangeParamType(click.ParamType):
    """Custom parameter type for page ranges (e.g., '1-5', '10-20')."""

    name = "page_range"

    def convert(self, value, param, ctx):
        """Convert string like '1-5' to tuple (1, 5)."""
        try:
            if "-" not in value:
                page = int(value)
                return (page, page)

            start, end = value.split("-", 1)
            start_page = int(start)
            end_page = int(end)

            if start_page < 1 or end_page < 1:
                self.fail("Page numbers must be >= 1", param, ctx)

            if start_page > end_page:
                self.fail(f"Invalid range: {value} (start > end)", param, ctx)

            return (start_page, end_page)
        except ValueError:
            self.fail(f"Invalid page range: {value}", param, ctx)


PAGE_RANGE = PageRangeParamType()


class PatternParamType(click.ParamType):
    """Custom parameter type for merge patterns (e.g., 'file.pdf:1-5')."""

    name = "pattern"

    def convert(self, value, param, ctx):
        """Convert string like 'file.pdf:1-5' to tuple ('file.pdf', 1, 5)."""
        try:
            if ":" not in value:
                self.fail(f"Pattern must be in format FILE:START-END, got: {value}", param, ctx)

            file_part, pages = value.split(":", 1)

            if "-" not in pages:
                page = int(pages)
                return (file_part, page, page)

            start, end = pages.split("-", 1)
            start_page = int(start)
            end_page = int(end)

            if start_page < 1 or end_page < 1:
                self.fail("Page numbers must be >= 1", param, ctx)

            if start_page > end_page:
                self.fail(f"Invalid page range in pattern: {value}", param, ctx)

            return (file_part, start_page, end_page)
        except ValueError as e:
            self.fail(f"Invalid pattern: {value} ({e})", param, ctx)


PATTERN = PatternParamType()


def _echo_success(message: str) -> None:
    """Print a success message in green with a checkmark."""
    click.secho(f"✓ {message}", fg="green", bold=True)


def _echo_error(message: str) -> None:
    """Print an error message in red with an X."""
    click.secho(f"✗ {message}", fg="red", bold=True, err=True)


def _echo_info(message: str) -> None:
    """Print an info message in blue."""
    click.secho(f"ℹ {message}", fg="blue")


def _echo_warning(message: str) -> None:
    """Print a warning message in yellow."""
    click.secho(f"⚠ {message}", fg="yellow")


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__, prog_name="pdf-mergician")
def cli():
    """
    pdf-mergician: A powerful PDF manipulation tool. 🎩✨

    Merge, split, rotate, and extract pages from PDF files with ease.
    Built with pypdf and designed for both simplicity and power.

    Examples:

      # Merge multiple PDFs
      pdf-mergician merge output.pdf file1.pdf file2.pdf file3.pdf

      # Advanced pattern merge
      pdf-mergician pattern output.pdf -s A.pdf:1-5 -s B.pdf:1-5

      # Split a PDF
      pdf-mergician split large.pdf output_dir/ --pages-per-file 10

      # Rotate pages
      pdf-mergician rotate input.pdf output.pdf --angle 90 --pages 1,3,5

    For more information, visit: https://github.com/jmcswain/pdf-mergician
    """


@cli.command("merge")
@click.argument("output", type=click.Path(dir_okay=False, writable=True))
@click.argument("files", nargs=-1, type=click.Path(exists=True, dir_okay=False), required=True)
@click.option(
    "--no-metadata",
    is_flag=True,
    help="Don't preserve metadata from the first PDF",
)
def merge_cmd(output: str, files: Tuple[str, ...], no_metadata: bool) -> None:
    """
    Merge multiple PDF files into one.

    Combines PDF files in the order specified, creating a single output file.
    By default, metadata from the first PDF is preserved.

    OUTPUT: Path to the output PDF file

    FILES: One or more PDF files to merge (in order)

    Examples:

      pdf-mergician merge combined.pdf doc1.pdf doc2.pdf doc3.pdf

      pdf-mergician merge output.pdf *.pdf --no-metadata
    """
    try:
        if not files:
            _echo_error("No input files provided")
            sys.exit(1)

        _echo_info(f"Merging {len(files)} PDF file(s)...")

        merge(files, output, preserve_metadata=not no_metadata)

        output_path = Path(output)
        file_size = output_path.stat().st_size / 1024  # KB

        _echo_success(f"Created {output} ({file_size:.1f} KB)")

    except FileNotFoundError as e:
        _echo_error(str(e))
        sys.exit(1)
    except Exception as e:
        _echo_error(f"Failed to merge PDFs: {e}")
        sys.exit(1)


@cli.command()
@click.argument("output", type=click.Path(dir_okay=False, writable=True))
@click.option(
    "-s",
    "--spec",
    "specs",
    type=PATTERN,
    multiple=True,
    required=True,
    help="Pattern spec: FILE:START-END (pages are 1-based, inclusive)",
)
def pattern(output: str, specs: List[Tuple[str, int, int]]) -> None:
    """
    Merge PDFs using an advanced pattern specification.

    This command allows you to specify exactly which pages from which files
    should be merged, and in what order. Pages are 1-based (like Adobe Reader)
    and ranges are inclusive on both ends.

    OUTPUT: Path to the output PDF file

    Examples:

      # Interleave pages from two PDFs
      pdf-mergician pattern output.pdf -s A.pdf:1-5 -s B.pdf:1-5 -s A.pdf:6-10 -s B.pdf:6-10

      # Extract and combine specific pages
      pdf-mergician pattern output.pdf -s doc1.pdf:1 -s doc2.pdf:5-10 -s doc1.pdf:20

      # Single page from multiple documents
      pdf-mergician pattern covers.pdf -s A.pdf:1 -s B.pdf:1 -s C.pdf:1
    """
    try:
        if not specs:
            _echo_error("No pattern specifications provided")
            sys.exit(1)

        _echo_info(f"Merging with {len(specs)} pattern specification(s)...")

        merge_pattern(specs, output)

        output_path = Path(output)
        file_size = output_path.stat().st_size / 1024  # KB

        _echo_success(f"Created {output} ({file_size:.1f} KB)")

    except (FileNotFoundError, ValueError, IndexError) as e:
        _echo_error(str(e))
        sys.exit(1)
    except Exception as e:
        _echo_error(f"Failed to merge PDFs: {e}")
        sys.exit(1)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("output_dir", type=click.Path(file_okay=False))
@click.option(
    "-p",
    "--pages-per-file",
    type=click.IntRange(min=1),
    default=1,
    help="Number of pages per output file (default: 1)",
)
def split(input_file: str, output_dir: str, pages_per_file: int) -> None:
    """
    Split a PDF into multiple files.

    Divides a PDF into smaller files, each containing the specified number
    of pages. Output files are numbered sequentially.

    INPUT_FILE: The PDF file to split

    OUTPUT_DIR: Directory where split files will be saved

    Examples:

      # Split into individual pages
      pdf-mergician split large.pdf output_dir/

      # Split into 10-page chunks
      pdf-mergician split large.pdf output_dir/ --pages-per-file 10
    """
    try:
        _echo_info(f"Splitting PDF with {pages_per_file} page(s) per file...")

        created_files = split_pdf(input_file, output_dir, pages_per_file=pages_per_file)

        _echo_success(f"Created {len(created_files)} file(s) in {output_dir}")

        # Show first few filenames
        if created_files:
            _echo_info("Files created:")
            max_display = 5
            for file_path in created_files[:max_display]:
                click.echo(f"  • {file_path.name}")
            if len(created_files) > max_display:
                click.echo(f"  ... and {len(created_files) - max_display} more")

    except (FileNotFoundError, ValueError) as e:
        _echo_error(str(e))
        sys.exit(1)
    except Exception as e:
        _echo_error(f"Failed to split PDF: {e}")
        sys.exit(1)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("output_file", type=click.Path(dir_okay=False, writable=True))
@click.option(
    "-a",
    "--angle",
    type=click.Choice(["90", "180", "270", "-90"]),
    required=True,
    help="Rotation angle in degrees",
)
@click.option(
    "-p",
    "--pages",
    help="Comma-separated page numbers to rotate (1-based). If not specified, rotates all pages.",
)
def rotate(input_file: str, output_file: str, angle: str, pages: Optional[str]) -> None:
    """
    Rotate pages in a PDF.

    Rotates specified pages (or all pages) by the given angle. Angles must
    be multiples of 90 degrees.

    INPUT_FILE: The input PDF file

    OUTPUT_FILE: The output PDF file

    Examples:

      # Rotate all pages 90 degrees clockwise
      pdf-mergician rotate input.pdf output.pdf --angle 90

      # Rotate specific pages
      pdf-mergician rotate input.pdf output.pdf --angle 180 --pages 1,3,5

      # Rotate counter-clockwise
      pdf-mergician rotate input.pdf output.pdf --angle -90
    """
    try:
        rotation = int(angle)

        # Parse page numbers if provided
        page_list = None
        if pages:
            try:
                page_list = [int(p.strip()) for p in pages.split(",")]
            except ValueError:
                _echo_error(f"Invalid page numbers: {pages}")
                sys.exit(1)

        if page_list:
            _echo_info(f"Rotating {len(page_list)} page(s) by {rotation}°...")
        else:
            _echo_info(f"Rotating all pages by {rotation}°...")

        rotate_pages(input_file, output_file, rotation, pages=page_list)

        _echo_success(f"Created {output_file}")

    except (FileNotFoundError, ValueError, IndexError) as e:
        _echo_error(str(e))
        sys.exit(1)
    except Exception as e:
        _echo_error(f"Failed to rotate pages: {e}")
        sys.exit(1)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("output_file", type=click.Path(dir_okay=False, writable=True))
@click.option(
    "-p",
    "--pages",
    required=True,
    help="Comma-separated page numbers or ranges to extract (1-based)",
)
def extract(input_file: str, output_file: str, pages: str) -> None:
    """
    Extract specific pages from a PDF.

    Creates a new PDF containing only the specified pages from the input file.
    Pages can be specified as individual numbers or ranges.

    INPUT_FILE: The input PDF file

    OUTPUT_FILE: The output PDF file

    Examples:

      # Extract specific pages
      pdf-mergician extract input.pdf output.pdf --pages 1,3,5,7

      # Extract a range
      pdf-mergician extract input.pdf output.pdf --pages 1-10

      # Mix ranges and individual pages
      pdf-mergician extract input.pdf output.pdf --pages 1,3-7,10,15-20
    """
    try:
        # Parse page specification
        page_list = []
        for part_raw in pages.split(","):
            part = part_raw.strip()
            if "-" in part:
                # Range
                start, end = part.split("-", 1)
                start_page = int(start)
                end_page = int(end)
                if start_page > end_page:
                    _echo_error(f"Invalid range: {part} (start > end)")
                    sys.exit(1)
                page_list.extend(range(start_page, end_page + 1))
            else:
                # Individual page
                page_list.append(int(part))

        if not page_list:
            _echo_error("No pages specified")
            sys.exit(1)

        _echo_info(f"Extracting {len(page_list)} page(s)...")

        extract_pages(input_file, output_file, page_list)

        _echo_success(f"Created {output_file}")

    except ValueError:
        _echo_error(f"Invalid page specification: {pages}")
        sys.exit(1)
    except (FileNotFoundError, IndexError) as e:
        _echo_error(str(e))
        sys.exit(1)
    except Exception as e:
        _echo_error(f"Failed to extract pages: {e}")
        sys.exit(1)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()

