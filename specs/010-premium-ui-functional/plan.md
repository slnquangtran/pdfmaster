# Implementation Plan: Premium UI Functional Implementation

**Branch**: `010-premium-ui-functional` | **Date**: 2026-03-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/010-premium-ui-functional/spec.md`

## Summary

Implement fully functional PDF Master application with working features based on the premium Editorial Workspace UI design. All UI elements shown in the design mockups must perform real operations including document management, PDF manipulation tools, document viewing/editing, and navigation.

## Technical Context

**Language/Version**: Python 3.10+ (project uses 3.14)  
**Primary Dependencies**: PyQt6 (GUI), PyMuPDF/fitz (PDF operations), ReportLab (PDF creation), pdfplumber (text/table extraction), pypdf (merge/split)  
**Storage**: File-based - PDF files stored in user's library directory, metadata cached in SQLite  
**Testing**: pytest  
**Target Platform**: Desktop (Windows/macOS/Linux)  
**Project Type**: desktop-app  
**Performance Goals**: PDF open < 3s for 50MB files, Search results < 1s for 1000 docs, UI responsive at 60fps  
**Constraints**: Must work offline, support files up to 200MB, handle 100+ page documents smoothly  
**Scale/Scope**: Single-user desktop app, ~50 screens/components, 10k+ documents support

## Constitution Check

**Result**: SKIP - Constitution file is template-only with no defined principles or gates.

## Project Structure

### Documentation (this feature)

```text
specs/010-premium-ui-functional/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── contracts/           # Phase 1 output
    ├── library-service.md
    ├── pdf-editor.md
    └── pdf-tools.md
```

### Source Code (repository root)

```text
pdfmaster/
├── __main__.py          # Entry point
├── ui/
│   ├── premium_main.py  # Premium main window
│   ├── styles/
│   │   └── premium_theme.py
│   ├── widgets/
│   │   ├── premium_sidebar.py
│   │   └── floating_toolbar.py
│   ├── pages/
│   │   ├── workspace_overview.py
│   │   ├── document_library.py
│   │   ├── utility_library.py
│   │   └── pdf_editor.py
│   └── dialogs/
│       ├── upload_dialog.py
│       ├── collection_dialog.py
│       └── tool_dialogs/
├── core/
│   ├── library.py       # Document library management
│   ├── document.py      # PDF document handling
│   ├── collection.py    # Collection management
│   └── workspace.py     # Workspace configuration
├── pdf/
│   ├── reader.py        # PDF reading/rendering
│   ├── writer.py        # PDF creation/modification
│   ├── merger.py        # PDF merge functionality
│   ├── splitter.py      # PDF split functionality
│   ├── compressor.py    # PDF compression
│   ├── encryptor.py     # PDF encryption
│   ├── signer.py        # Digital signatures
│   └── redactor.py      # PDF redaction
├── converters/
│   ├── to_pdf.py        # DOCX/XLSX/PPTX to PDF
│   ├── to_html.py       # PDF to HTML
│   └── to_text.py       # PDF to text
└── extractors/
    ├── images.py        # Image extraction
    └── text.py          # Text extraction
```

**Structure Decision**: Single desktop application with modular architecture separating UI (PyQt6), core business logic (library/document management), PDF operations (PyMuPDF-based), and conversion utilities.

## Phase 0: Research

### Research Tasks

1. **PyMuPDF capabilities** - Verify PyMuPDF supports all required PDF operations (merge, split, encrypt, redact, annotations, signatures)
2. **PyQt6 document viewer** - Research best practices for PDF rendering in PyQt6 (QGraphicsView vs custom widget)
3. **File watching** - Research PyQt6 file system watcher for real-time library updates
4. **Background processing** - Research QThread/QRunnable patterns for non-blocking PDF operations
5. **SQLite metadata caching** - Research efficient metadata caching strategies for large document libraries

### Research Findings

See [research.md](./research.md) for detailed findings.

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](./data-model.md) for entity definitions.

### Interface Contracts

See [contracts/](./contracts/) for service interfaces.

### Quickstart

See [quickstart.md](./quickstart.md) for setup and verification guide.

## Implementation Phases

### Phase 1: Core Library Management (P1)

Implement the document library service that scans directories, caches metadata, and provides filtering/sorting.

**Deliverables**:
- `core/library.py` - Library scanning and file tracking
- `core/document.py` - Document metadata extraction
- `core/workspace.py` - Workspace configuration
- `core/collection.py` - Collection management
- SQLite schema for metadata cache

### Phase 2: Premium UI Integration (P1)

Connect the premium UI pages to real data sources.

**Deliverables**:
- Update `workspace_overview.py` with real storage and document data
- Update `document_library.py` with real file listing, filtering, sorting
- Update `premium_sidebar.py` with working navigation
- Add file upload functionality

### Phase 3: PDF Editor (P2)

Implement the PDF viewer/editor with PyMuPDF rendering.

**Deliverables**:
- `pdf/reader.py` - PDF rendering with PyMuPDF
- `ui/widgets/pdf_viewer.py` - PyQt6 PDF viewer widget
- Zoom, pan, page navigation
- Basic text annotation support

### Phase 4: PDF Tools (P2)

Implement the PDF manipulation tools.

**Deliverables**:
- `pdf/merger.py` - PDF merge with TOC
- `pdf/splitter.py` - PDF split by ranges/bookmarks
- `pdf/compressor.py` - PDF compression
- `pdf/encryptor.py` - AES-256 encryption
- `pdf/signer.py` - Digital signatures
- `pdf/redactor.py` - Text redaction
- `converters/to_pdf.py` - Multi-format to PDF
- `converters/to_html.py` - PDF to HTML
- `extractors/images.py` - Image extraction
- `extractors/text.py` - Text extraction

### Phase 5: Search & Polish (P1)

Implement search functionality and polish the UI.

**Deliverables**:
- Full-text search across documents
- Search results display
- Error handling for all operations
- Progress indicators for long operations
- Empty states for no results/errors

## Complexity Tracking

No violations requiring justification.
