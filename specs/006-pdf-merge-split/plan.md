# Implementation Plan: PDF Merge and Split

**Branch**: `006-pdf-merge-split` | **Date**: 2026-03-23 | **Spec**: specs/006-pdf-merge-split/spec.md
**Input**: Feature specification from `/specs/006-pdf-merge-split/spec.md`

## Summary

Add PDF merge and split functionality to the application. Users can combine multiple PDFs into one, split by page ranges, or extract individual pages. Uses PyMuPDF (fitz) already in the project for high-performance PDF manipulation.

## Technical Context

**Language/Version**: Python 3.10+ (project uses 3.14)  
**Primary Dependencies**: PyMuPDF (fitz) - already in project  
**Storage**: Local file system  
**Testing**: pytest (per AGENTS.md)  
**Target Platform**: Windows desktop  
**Project Type**: Desktop application with PyQt6 GUI  
**Performance Goals**: Merge 5 PDFs (10 pages each) under 30 seconds  
**Constraints**: Handle password-protected PDFs gracefully (skip with error)  
**Scale/Scope**: Single user desktop use

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

No constitution defined in project - skipping gate checks.

## Project Structure

### Source Code (repository root)

```text
pdfmaster/
├── src/
│   ├── core/
│   │   ├── merger.py          # NEW: PDF merge/split logic
│   │   └── __init__.py
│   └── ...
├── ui/
│   ├── windows/
│   │   ├── merge_window.py     # NEW: Merge/split UI
│   │   └── ...
│   └── ...
└── tests/
    └── (add merge/split tests)
```

### Documentation (this feature)

```text
specs/006-pdf-merge-split/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A - internal feature)
└── tasks.md             # Phase 2 output
```

**Structure Decision**: Add new `src/core/merger.py` for PDF operations and `ui/windows/merge_window.py` for the GUI - following the existing pattern for converters and extractors.

## Phase 0: Research Complete

**Findings** (research.md generated with these decisions):

- **Tool**: PyMuPDF (fitz) - already in project, fast and capable
- **Merge**: Use `doc.insert_pdf(doc2)` to append PDFs in sequence
- **Split**: Use `doc.insert_pdf(doc, from_page=x, to_page=y)` for page ranges
- **Individual pages**: Loop and save each page as new document
- **Page range parsing**: Support "1-3", "5-", "-3", "1,3,5" formats
- **Error handling**: Catch fitz.FileNotFoundError, fitzPasswordError, etc.

## Complexity Tracking

> None needed - straightforward feature with existing tech stack.

## Next Steps

Ready for `/speckit.tasks` to generate implementation tasks.