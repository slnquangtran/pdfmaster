# Quickstart: Premium UI Functional Implementation

**Date**: 2026-03-30  
**Feature**: Premium UI Functional Implementation

## Prerequisites

- Python 3.10 or higher
- PyQt6
- PyMuPDF (fitz)
- PDF files for testing

## Setup

### 1. Install Dependencies

```bash
pip install PyQt6 PyMuPDF pypdf pdfplumber docx2pdf
```

### 2. Create Library Directory

```bash
mkdir ~/PDFLibrary
# Copy some PDF files to test
cp *.pdf ~/PDFLibrary/
```

### 3. Run Application

```bash
cd pdfmaster
python -m pdfmaster
```

## Verification Steps

### P1: Workspace Overview

1. Launch the application
2. Verify "Workspace Overview" page displays
3. Check that "Storage Status" shows actual file sizes
4. Check that "Recent Documents" shows real PDF files from library
5. Click on a document - should open in PDF Editor
6. Click "View All Library" - should navigate to Document Library

### P1: Document Library

1. Navigate to "Library" in sidebar
2. Verify all PDF files are listed with correct names and sizes
3. Click "PDFs" filter - should show only PDFs
4. Click column headers to sort by name, date, size
5. Double-click a document - should open in PDF Editor
6. Click document actions menu - should show Open, Rename, Delete options
7. Click "+ New Collection" - should create new collection
8. Star a document - should toggle starred status

### P1: Navigation and Search

1. Click each sidebar item (Library, Recent, Starred, Annotated, Archive)
2. Verify each shows appropriate document list
3. Type in search box - results should appear in real-time
4. Click search result - should open document
5. Click "Upload PDF" - file dialog should open
6. Select a PDF - it should be added to library

### P2: PDF Editor

1. Open a document in PDF Editor
2. Verify document renders correctly
3. Use zoom in/out buttons - view should scale
4. Scroll through multi-page document - pages should load
5. Click "Add Text" - should allow adding text annotation
6. Click "Sign PDF" - should allow adding signature
7. Click "Save Changes" - modifications should persist
8. Click "Export" - should offer format options

### P2: PDF Tools

1. Navigate to Utility Library
2. Click "Smart Merger" - select multiple PDFs, verify merge works
3. Click "Document Split" - verify split by page ranges works
4. Click "Compress" - verify file size reduction
5. Click "Multi-Format to PDF" - verify DOCX/XLSX conversion
6. Click "Extract Images" - verify images are extracted
7. Click "AES-256 Encryption" - verify password protection
8. Click "Redaction Tool" - verify text can be redacted

### P3: Theme Toggle

1. Press Ctrl+D - theme should change to dark
2. Press Ctrl+D again - theme should change to light
3. Restart application - theme preference should persist
4. Navigate all pages in dark mode - should render correctly

## Troubleshooting

### Library Not Found

If library directory doesn't exist:
1. Click settings gear icon
2. Select new library directory
3. Application will rescan

### PDF Not Opening

If PDF fails to open:
1. Check if file is password-protected
2. Check if file is corrupted
3. Check file permissions

### Slow Performance

If application is slow:
1. Reduce number of cached pages in settings
2. Close other PDF viewers
3. Ensure sufficient disk space

## Testing Commands

```bash
# Run tests
cd pdfmaster
pytest tests/

# Check code quality
ruff check .

# Type checking
mypy .
```
