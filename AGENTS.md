# pdf_master Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-03-30

## Active Technologies
- Python 3.10+ + PyQt6 (GUI framework), PyInstaller (packaging) (002-pdfmaster-ui-release)
- File-based (local storage) (002-pdfmaster-ui-release)
- Python 3.10+ (project uses 3.14) + PyMuPDF (fitz) - already in project (006-pdf-merge-split)
- Local file system (006-pdf-merge-split)
- Python 3.10+ (project uses 3.14) + PyQt6 (GUI), PyYAML (templates), jsonschema (validation) (009-ai-agent-builder)
- SQLite for metadata + YAML files for templates, JSON for sessions (009-ai-agent-builder)

- Python 3.10+ + ReportLab, PyMuPDF, pypdf, pdfplumber, docx2pdf, WeasyPrint (001-pdf-master-suite)

## Project Structure

```text
backend/
frontend/
tests/
```

## Commands

cd src; pytest; ruff check .

## Code Style

Python 3.10+: Follow standard conventions

## Recent Changes
- 009-ai-agent-builder: Added Python 3.10+ (project uses 3.14) + PyQt6 (GUI), PyYAML (templates), jsonschema (validation)
- 006-pdf-merge-split: Added Python 3.10+ (project uses 3.14) + PyMuPDF (fitz) - already in project
- 002-pdfmaster-ui-release: Added Python 3.10+ + PyQt6 (GUI framework), PyInstaller (packaging)


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
