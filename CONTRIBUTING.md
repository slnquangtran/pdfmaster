Contributing to pdfmaster
=========================

This project is a Python-based desktop/CLI suite for PDF manipulation.

Prerequisites
- Python 3.10+ (tested with 3.11 in CI)
- Access to a Python environment with build tools (pip, setuptools, wheel)
- Optional: Node-based tooling is not required for core Python tests

Getting started
- Install dependencies in dev mode: `pip install -e .[dev]`
- Run tests: `pytest`
- Lint: `ruff check .`

CI
- This repository uses GitHub Actions for CI. See .github/workflows/ci.yml

Reporting issues
- Open an issue with a clear description, reproduction steps, and expected vs actual outcomes.
