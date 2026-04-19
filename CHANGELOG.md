# Change Log

All notable changes to this project will be documented here.

## [Unreleased]
- Expanded CLI with merge, split, extract-table, export-page-image, watermark, preview-text features.
- Added watermark capability via PyMuPDF integration; improved compatibility.
- Added end-to-end tests for CLI commands and text extraction.
- CI now runs on Python 3.10, 3.11, and 3.12 with a multi-version matrix and dependency caching.
- Improved packaging: added explicit package namespaces and cleaned up README/docs.
- Ignores for heavy frontend assets (web/) to keep repo lean.

## Next
- Add more edge-case coverage for CLI commands (invalid inputs, large PDFs).
- Add coverage reporting to CI and a release process.
- Consider isolating frontend assets into a separate repo.
