## Summary
- Extend CI to multi-version Python matrix (3.10, 3.11, 3.12) with Windows CI, add caching, and publish coverage.
- Expand the CLI with new features: merge, split, extract-table, export-page-image, watermark, preview-text.
- Strengthen packaging: explicit package namespaces, fixed __main__ launcher, and PyMuPDF dependency naming.
- Add extensive test suite: unit tests, integration tests for CLI flows, and end-to-end text/watermark tests.
- Improve repository hygiene: ignore heavy frontend assets (web/) and add a changelog and contributing docs.

## Changes
- CI: multi-version matrix; Windows CI; dependency caching; coverage upload.
- CLI: new commands (merge, split, extract-table, export-page-image, watermark, preview-text).
- Watermark: stable watermark feature with PyMuPDF.
- Tests: version, smoke tests, edge cases, integration tests for merge/split, text extraction, watermark.
- Packaging: add pdfmaster/src/__init__.py, pdfmaster/ui/__init__.py, pdfmaster/ui/windows/__init__.py; fix __main__ launcher.
- Docs: CHANGELOG.md and CONTRIBUTING.md added; README updated.

## How to test locally
- Install: pip install -e .[dev]
- Run tests: pytest -q
- CLI help: python -m pdfmaster --help
- Example commands: merge, split, extract-table, export-page-image, watermark, preview-text

## Notes
- Frontend assets in web/ are ignored for now; consider isolating to a separate repo in the future if needed.
