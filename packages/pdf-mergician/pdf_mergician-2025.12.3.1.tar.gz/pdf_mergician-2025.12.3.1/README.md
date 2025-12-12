# pdf-mergician 🎩✨

[![PyPI version](https://badge.fury.io/py/pdf-mergician.svg)](https://badge.fury.io/py/pdf-mergician)
[![Python Support](https://img.shields.io/pypi/pyversions/pdf-mergician.svg)](https://pypi.org/project/pdf-mergician/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A powerful, user-friendly CLI tool for PDF manipulation. Merge, split, rotate, and extract pages with ease - like magic! 🪄

Built with [pypdf](https://github.com/py-pdf/pypdf) and [Click](https://click.palletsprojects.com/), `pdf-mergician` provides both a professional command-line interface and a clean Python API for all your PDF manipulation needs.

---

## ✨ Features

- **🔗 Merge PDFs** - Combine multiple PDFs into one with a single command
- **📐 Advanced Pattern Merging** - Interleave pages from multiple PDFs with precise control
- **✂️ Split PDFs** - Divide large PDFs into smaller files
- **🔄 Rotate Pages** - Rotate specific pages or entire documents
- **📤 Extract Pages** - Pull out specific pages into new PDFs
- **🎯 Intuitive CLI** - Clean, professional command-line interface with helpful error messages
- **🐍 Python API** - Use all features programmatically in your Python projects
- **⚡ Fast & Reliable** - Built on the robust pypdf library
- **📝 Well Documented** - Comprehensive documentation and examples

---

## 🚀 Quick Start

### Installation

```bash
pip install pdf-mergician
```

### Basic Usage

```bash
# Merge multiple PDFs
pdf-mergician merge output.pdf file1.pdf file2.pdf file3.pdf

# Split a PDF into individual pages
pdf-mergician split large.pdf output_dir/

# Rotate pages
pdf-mergician rotate input.pdf output.pdf --angle 90

# Extract specific pages
pdf-mergician extract input.pdf output.pdf --pages 1,3,5-10
```

### Common Use Cases

```bash
# Combine all PDFs in a directory
pdf-mergician merge combined.pdf *.pdf

# Interleave pages from two documents
pdf-mergician pattern comparison.pdf -s doc1.pdf:1-5 -s doc2.pdf:1-5

# Split into 10-page chunks
pdf-mergician split large.pdf chunks/ --pages-per-file 10

# Rotate specific pages 180 degrees
pdf-mergician rotate input.pdf output.pdf --angle 180 --pages 1,3,5

# Extract a range of pages
pdf-mergician extract input.pdf chapter1.pdf --pages 10-25

# Combine cover pages from multiple documents
pdf-mergician pattern covers.pdf -s doc1.pdf:1 -s doc2.pdf:1 -s doc3.pdf:1

# Create a booklet by extracting odd pages
pdf-mergician extract document.pdf odd_pages.pdf --pages 1,3,5,7,9,11

# Merge with custom page selection
pdf-mergician pattern custom.pdf -s report.pdf:1 -s data.pdf:5-10 -s report.pdf:20
```

---

## 📚 Documentation

### Command Overview

```bash
pdf-mergician --help
```

Available commands:
- `merge` - Merge multiple PDF files into one
- `pattern` - Advanced pattern-based merging
- `split` - Split a PDF into multiple files
- `rotate` - Rotate pages in a PDF
- `extract` - Extract specific pages from a PDF

### Merge Command

Combine multiple PDF files in order:

```bash
pdf-mergician merge output.pdf file1.pdf file2.pdf file3.pdf
```

**Options:**
- `--no-metadata` - Don't preserve metadata from the first PDF

**Examples:**

```bash
# Merge all PDFs in current directory
pdf-mergician merge combined.pdf *.pdf

# Merge without preserving metadata
pdf-mergician merge output.pdf doc1.pdf doc2.pdf --no-metadata
```

### Pattern Command

Advanced merging with precise page control. Perfect for interleaving pages or creating custom combinations:

```bash
pdf-mergician pattern output.pdf -s A.pdf:1-5 -s B.pdf:1-5 -s A.pdf:6-10
```

**Pattern Format:** `FILE:START-END` (pages are 1-based, inclusive)

**Examples:**

```bash
# Interleave pages from two documents
pdf-mergician pattern output.pdf \
    -s doc1.pdf:1-5 \
    -s doc2.pdf:1-5 \
    -s doc1.pdf:6-10 \
    -s doc2.pdf:6-10

# Extract and combine specific pages
pdf-mergician pattern output.pdf \
    -s report.pdf:1 \
    -s data.pdf:5-10 \
    -s report.pdf:20

# Combine cover pages from multiple documents
pdf-mergician pattern covers.pdf \
    -s doc1.pdf:1 \
    -s doc2.pdf:1 \
    -s doc3.pdf:1
```

### Split Command

Divide a PDF into smaller files:

```bash
pdf-mergician split input.pdf output_dir/
```

**Options:**
- `-p, --pages-per-file INTEGER` - Number of pages per output file (default: 1)

**Examples:**

```bash
# Split into individual pages
pdf-mergician split large.pdf pages/

# Split into 10-page chunks
pdf-mergician split large.pdf chunks/ --pages-per-file 10

# Split into 5-page sections
pdf-mergician split document.pdf sections/ -p 5
```

### Rotate Command

Rotate pages in a PDF:

```bash
pdf-mergician rotate input.pdf output.pdf --angle 90
```

**Options:**
- `-a, --angle` - Rotation angle: 90, 180, 270, or -90 (required)
- `-p, --pages` - Comma-separated page numbers to rotate (default: all pages)

**Examples:**

```bash
# Rotate all pages 90° clockwise
pdf-mergician rotate input.pdf output.pdf --angle 90

# Rotate specific pages 180°
pdf-mergician rotate input.pdf output.pdf --angle 180 --pages 1,3,5

# Rotate counter-clockwise
pdf-mergician rotate input.pdf output.pdf --angle -90

# Rotate a range of pages
pdf-mergician rotate input.pdf output.pdf --angle 90 --pages 1,2,3,4,5
```

### Extract Command

Extract specific pages into a new PDF:

```bash
pdf-mergician extract input.pdf output.pdf --pages 1,3,5-10
```

**Options:**
- `-p, --pages` - Comma-separated page numbers or ranges (required)

**Examples:**

```bash
# Extract specific pages
pdf-mergician extract input.pdf output.pdf --pages 1,3,5,7

# Extract a range
pdf-mergician extract input.pdf output.pdf --pages 1-10

# Mix ranges and individual pages
pdf-mergician extract input.pdf output.pdf --pages 1,3-7,10,15-20

# Extract just the first page
pdf-mergician extract input.pdf cover.pdf --pages 1
```

---

## 🐍 Python API

You can also use `pdf-mergician` as a Python library:

### Basic Operations

```python
from merge_pdf import merge, merge_pattern, split_pdf, rotate_pages, extract_pages

# Merge PDFs
merge(["file1.pdf", "file2.pdf", "file3.pdf"], "output.pdf")

# Merge without preserving metadata
merge(["doc1.pdf", "doc2.pdf"], "output.pdf", preserve_metadata=False)

# Split a PDF
split_pdf("large.pdf", "output_dir/", pages_per_file=10)

# Rotate pages
rotate_pages("input.pdf", "output.pdf", rotation=90, pages=[1, 3, 5])

# Rotate all pages
rotate_pages("input.pdf", "output.pdf", rotation=180)

# Extract pages
extract_pages("input.pdf", "output.pdf", pages=[1, 3, 5, 7, 9])
```

### Advanced Pattern Merging

```python
from merge_pdf import merge_pattern

# Interleave pages from two documents
pattern = [
    ("A.pdf", 1, 5),   # Pages 1-5 from A.pdf
    ("B.pdf", 1, 5),   # Pages 1-5 from B.pdf
    ("A.pdf", 6, 10),  # Pages 6-10 from A.pdf
    ("B.pdf", 6, 10),  # Pages 6-10 from B.pdf
]
merge_pattern(pattern, "interleaved.pdf")

# Build custom document
pattern = [
    ("cover.pdf", 1, 1),
    ("intro.pdf", 1, 3),
    ("main.pdf", 5, 25),
    ("conclusion.pdf", 1, 5),
]
merge_pattern(pattern, "custom_document.pdf")
```

### Practical Examples

```python
from pathlib import Path
from merge_pdf import merge, split_pdf, extract_pages

# Merge all PDFs in a directory
pdf_dir = Path("documents/")
pdf_files = sorted(pdf_dir.glob("*.pdf"))
merge(pdf_files, "combined.pdf")

# Split and process
split_files = split_pdf("large.pdf", "chunks/", pages_per_file=5)
print(f"Created {len(split_files)} files")

# Extract specific pages
extract_pages("report.pdf", "summary.pdf", [1, 5, 10, 15, 20])

# Batch processing
for pdf in Path("input/").glob("*.pdf"):
    output = Path("output") / f"rotated_{pdf.name}"
    rotate_pages(pdf, output, 90)
```

### Error Handling

```python
from merge_pdf import merge

try:
    merge(["file1.pdf", "file2.pdf"], "output.pdf")
    print("✓ Merge successful")
except FileNotFoundError as e:
    print(f"✗ File not found: {e}")
except ValueError as e:
    print(f"✗ Invalid input: {e}")
except Exception as e:
    print(f"✗ Error: {e}")
```

See the [API documentation](docs/api.md) for complete details.

---

## 🎨 Advanced Use Cases & Real-World Examples

### 📄 Document Assembly

#### Combine Report Sections
```bash
# Assemble a complete report from multiple sources
pdf-mergician merge final_report.pdf \
    cover_page.pdf \
    executive_summary.pdf \
    introduction.pdf \
    chapter1.pdf \
    chapter2.pdf \
    chapter3.pdf \
    conclusion.pdf \
    references.pdf \
    appendix.pdf
```

#### Create Custom Document from Multiple Sources
```bash
# Build a custom document with specific pages
pdf-mergician pattern custom_document.pdf \
    -s template_cover.pdf:1 \
    -s toc.pdf:1-2 \
    -s main_content.pdf:5-25 \
    -s data_analysis.pdf:10-30 \
    -s conclusions.pdf:1-5
```

### 🔄 Interleaving & Comparison

#### Side-by-Side Document Comparison
```bash
# Compare two versions page by page
pdf-mergician pattern comparison.pdf \
    -s original.pdf:1 -s revised.pdf:1 \
    -s original.pdf:2 -s revised.pdf:2 \
    -s original.pdf:3 -s revised.pdf:3 \
    -s original.pdf:4 -s revised.pdf:4 \
    -s original.pdf:5 -s revised.pdf:5
```

#### Interleave Slides with Notes
```bash
# Create presentation with notes after each slide
pdf-mergician pattern presentation_with_notes.pdf \
    -s slides.pdf:1 -s notes.pdf:1 \
    -s slides.pdf:2 -s notes.pdf:2 \
    -s slides.pdf:3 -s notes.pdf:3
```

### 📚 Academic & Research

#### Combine Research Papers
```bash
# Merge multiple papers with cover page
pdf-mergician merge literature_review.pdf \
    cover.pdf \
    paper1.pdf \
    paper2.pdf \
    paper3.pdf \
    bibliography.pdf
```

#### Extract Key Pages from Multiple Papers
```bash
# Extract methodology sections from different papers
pdf-mergician pattern methodology_comparison.pdf \
    -s paper1.pdf:5-8 \
    -s paper2.pdf:3-6 \
    -s paper3.pdf:4-7
```

### 💼 Business & Legal

#### Assemble Contract with Exhibits
```bash
# Complete contract package
pdf-mergician merge complete_contract.pdf \
    main_agreement.pdf \
    terms_and_conditions.pdf \
    exhibit_a.pdf \
    exhibit_b.pdf \
    signature_pages.pdf
```

#### Create Invoice Package
```bash
# Combine invoice with supporting documents
pdf-mergician merge invoice_package.pdf \
    invoice.pdf \
    purchase_order.pdf \
    delivery_receipt.pdf \
    payment_terms.pdf
```

### 📖 Publishing & Printing

#### Create Booklet Layout
```bash
# Extract odd and even pages for booklet printing
pdf-mergician extract document.pdf odd_pages.pdf --pages 1,3,5,7,9,11,13,15
pdf-mergician extract document.pdf even_pages.pdf --pages 2,4,6,8,10,12,14,16

# Rotate even pages for back-to-back printing
pdf-mergician rotate even_pages.pdf even_rotated.pdf --angle 180
```

#### Prepare Print-Ready Document
```bash
# Add cover and back cover to content
pdf-mergician merge print_ready.pdf \
    front_cover.pdf \
    content.pdf \
    back_cover.pdf
```

### 🎓 Education

#### Combine Lecture Materials
```bash
# Merge all lecture slides for a course
pdf-mergician merge complete_course.pdf \
    lecture01_intro.pdf \
    lecture02_basics.pdf \
    lecture03_advanced.pdf \
    lecture04_practice.pdf \
    lecture05_review.pdf
```

#### Create Study Guide
```bash
# Extract key pages from textbook chapters
pdf-mergician pattern study_guide.pdf \
    -s chapter1.pdf:1-2 \
    -s chapter2.pdf:5-7 \
    -s chapter3.pdf:10-12 \
    -s practice_problems.pdf:1-10
```

### 🔧 Batch Processing

#### Rotate All Scanned Documents
```bash
# Fix orientation for all scanned PDFs
for pdf in scanned_*.pdf; do
    echo "Rotating $pdf..."
    pdf-mergician rotate "$pdf" "fixed_$pdf" --angle 90
done
```

#### Split Large Documents
```bash
# Split all large PDFs into 10-page sections
for pdf in large_*.pdf; do
    dirname="sections_${pdf%.pdf}"
    echo "Splitting $pdf into $dirname..."
    pdf-mergician split "$pdf" "$dirname/" --pages-per-file 10
done
```

#### Extract First Pages as Thumbnails
```bash
# Create cover page collection
for pdf in *.pdf; do
    output="cover_${pdf}"
    echo "Extracting cover from $pdf..."
    pdf-mergician extract "$pdf" "$output" --pages 1
done
```

#### Process Monthly Reports
```bash
# Combine all monthly reports into yearly report
pdf-mergician merge annual_report_2024.pdf \
    january_2024.pdf \
    february_2024.pdf \
    march_2024.pdf \
    april_2024.pdf \
    may_2024.pdf \
    june_2024.pdf \
    july_2024.pdf \
    august_2024.pdf \
    september_2024.pdf \
    october_2024.pdf \
    november_2024.pdf \
    december_2024.pdf
```

### 🎨 Creative Workflows

#### Create Photo Album
```bash
# Combine photo pages in order
pdf-mergician merge photo_album.pdf \
    album_cover.pdf \
    page_01.pdf \
    page_02.pdf \
    page_03.pdf \
    page_04.pdf \
    page_05.pdf \
    back_cover.pdf
```

#### Portfolio Assembly
```bash
# Build portfolio with selected works
pdf-mergician pattern portfolio.pdf \
    -s cover.pdf:1 \
    -s project1.pdf:1-3 \
    -s project2.pdf:1-5 \
    -s project3.pdf:1-2 \
    -s bio.pdf:1
```

### 🔄 Quality Control & Review

#### Extract Sample Pages for Review
```bash
# Extract every 10th page for quick review
pdf-mergician extract large_document.pdf sample.pdf \
    --pages 10,20,30,40,50,60,70,80,90,100
```

#### Create Redacted Version
```bash
# Combine non-sensitive pages only
pdf-mergician pattern public_version.pdf \
    -s full_document.pdf:1-5 \
    -s full_document.pdf:15-20 \
    -s full_document.pdf:30-35
```

### 📊 Data & Analytics

#### Combine Data Reports
```bash
# Merge quarterly data reports
pdf-mergician merge q4_2024_data.pdf \
    executive_summary.pdf \
    sales_data.pdf \
    marketing_metrics.pdf \
    financial_analysis.pdf \
    forecasts.pdf
```

#### Create Dashboard Compilation
```bash
# Combine dashboard screenshots
pdf-mergician merge dashboard_report.pdf \
    overview_dashboard.pdf \
    sales_dashboard.pdf \
    operations_dashboard.pdf \
    hr_dashboard.pdf
```

### 🌐 Multi-Language Documents

#### Combine Translations
```bash
# Create bilingual document
pdf-mergician pattern bilingual_manual.pdf \
    -s english_version.pdf:1 -s spanish_version.pdf:1 \
    -s english_version.pdf:2 -s spanish_version.pdf:2 \
    -s english_version.pdf:3 -s spanish_version.pdf:3
```

### 🔐 Compliance & Archival

#### Create Audit Package
```bash
# Assemble complete audit documentation
pdf-mergician merge audit_package_2024.pdf \
    audit_report.pdf \
    financial_statements.pdf \
    supporting_documents.pdf \
    management_response.pdf \
    corrective_actions.pdf
```

#### Archive Project Documents
```bash
# Create dated archive
DATE=$(date +%Y%m%d)
pdf-mergician merge "project_archive_${DATE}.pdf" \
    project_plan.pdf \
    requirements.pdf \
    design_docs.pdf \
    test_results.pdf \
    final_deliverable.pdf
```

### 💡 Automation Scripts

#### Automated Report Generation
```bash
#!/bin/bash
# Generate monthly report automatically

MONTH=$(date +%B_%Y)
OUTPUT="monthly_report_${MONTH}.pdf"

echo "Generating report for $MONTH..."

pdf-mergician merge "$OUTPUT" \
    templates/cover.pdf \
    "data/summary_${MONTH}.pdf" \
    "data/details_${MONTH}.pdf" \
    templates/footer.pdf

echo "Report generated: $OUTPUT"
```

#### Smart Document Organizer
```bash
#!/bin/bash
# Organize PDFs by page count

mkdir -p short medium long

for pdf in *.pdf; do
    # Get page count (requires pdfinfo)
    pages=$(pdfinfo "$pdf" 2>/dev/null | grep Pages | awk '{print $2}')

    if [ "$pages" -lt 10 ]; then
        mv "$pdf" short/
    elif [ "$pages" -lt 50 ]; then
        mv "$pdf" medium/
    else
        mv "$pdf" long/
        # Split long documents
        pdf-mergician split "long/$pdf" "long/split_${pdf%.pdf}/" -p 25
    fi
done
```

---

## 🛠️ Development

### Setup

```bash
# Clone the repository
git clone https://github.com/jmcswain/pdf-mergician.git
cd pdf-mergician

# Create virtual environment and install dependencies
make venv           # Creates ./venv/ virtual environment
make dev-install    # Installs package with dev dependencies
```

**Note:** All Makefile commands automatically use the virtual environment at `./venv/`. This keeps your system Python clean and ensures consistent dependencies.

### Publishing Setup

Before you can publish to PyPI, you need to configure authentication. We support two methods:

#### Method 1: Trusted Publishers (Recommended) ⭐

**The modern, secure way** using GitHub Actions with OpenID Connect (OIDC). **No API tokens or passwords needed!**

**Benefits:**
- ✅ No manual token management
- ✅ Short-lived credentials (15 min)
- ✅ Enhanced security
- ✅ PyPI recommended approach

**Quick Setup:**
1. Configure trusted publisher on [PyPI](https://pypi.org/manage/account/publishing/)
2. Create GitHub environments (`pypi`, `testpypi`)
3. Push a release tag or create a GitHub Release
4. Automatic publishing! 🎉

📖 **Complete Guide**: [GitHub Trusted Publisher Setup](docs/github-trusted-publisher.md)
🚀 **Quick Start**: [Publishing Quick Start](docs/publishing-quickstart.md)

#### Method 2: API Tokens (Traditional)

For manual publishing or non-GitHub CI systems.

📖 **Complete Guide**: [PyPI Credentials Setup](docs/pypi-setup.md)

### Available Make Targets

```bash
make help          # Show all available targets
make venv          # Create virtual environment at ./venv/
make clean         # Remove build artifacts (keeps venv)
make clean-all     # Remove all artifacts including venv
make dev-install   # Install with dev dependencies
make lint          # Run linting checks
make test          # Run tests
make coverage      # Run tests with coverage report
make version       # Show current version
make version-bump  # Bump version (YYYY.MM.DD.x format)
make build         # Build distribution packages
make package       # Full package preparation (bump + lint + test + build)
make publish       # Publish to PyPI
```

**All commands automatically use the `./venv/` virtual environment.**

### Version Management

pdf-mergician uses date-based versioning with the format **YYYY.MM.DD.x** where:
- `YYYY.MM.DD` is the current date
- `x` is an incremental build number (starting at 1 for each day)

```bash
# Show current version
make version

# Bump to next version
make version-bump

# Package automatically bumps version
make package
```

See [docs/versioning.md](docs/versioning.md) for detailed information.

### Running Tests

```bash
# Run all tests
make test

# Run tests with coverage
make coverage

# Run quick tests (no coverage)
make test-quick
```

### Code Quality

This project uses:
- **[ruff](https://github.com/astral-sh/ruff)** for linting and formatting
- **[pytest](https://pytest.org/)** for testing
- **Type hints** throughout the codebase

```bash
# Format code
make format

# Run linter
make lint

# Auto-fix linting issues
make lint-fix
```

---

## 📋 Requirements

- **Python**: 3.8 or higher (matches pypdf support)
- **Dependencies**:
  - [pypdf](https://github.com/py-pdf/pypdf) >= 4.0.0
  - [click](https://click.palletsprojects.com/) >= 8.1.0

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Run tests (`make test`)
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [pypdf](https://github.com/py-pdf/pypdf) - A powerful PDF library for Python
- CLI powered by [Click](https://click.palletsprojects.com/) - A beautiful command line interface framework
- Inspired by the need for a simple, powerful PDF manipulation tool

---

## 🔗 Links

- **Documentation**: [docs/](docs/)
- **PyPI**: https://pypi.org/project/pdf-mergician/
- **Source Code**: https://github.com/jmcswain/pdf-mergician
- **Issue Tracker**: https://github.com/jmcswain/pdf-mergician/issues
- **pypdf Documentation**: https://pypdf.readthedocs.io/
- **Click Documentation**: https://click.palletsprojects.com/

---

## 💡 Future Features

Ideas for future enhancements:

- 🔐 **Encryption/Decryption** - Add password protection to PDFs
- 🖼️ **Image to PDF** - Convert images to PDF format
- 📑 **Bookmark Management** - Add, edit, and remove bookmarks
- 🏷️ **Metadata Editing** - Update PDF metadata (title, author, etc.)
- 🎨 **Watermarking** - Add watermarks or stamps to pages
- 📊 **PDF Info** - Display detailed information about PDFs
- 🔍 **Text Extraction** - Extract text content from PDFs
- 📐 **Page Resizing** - Resize or scale pages
- 🎭 **Page Overlays** - Overlay pages from different PDFs
- 📱 **Progress Bars** - Visual progress for long operations

Have a feature request? [Open an issue](https://github.com/jmcswain/pdf-mergician/issues)!

---

<div align="center">
Made with ❤️ by J McSwain
</div>
merge pdf files via click cli
