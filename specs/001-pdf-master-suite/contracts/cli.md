# PDF Master Suite - CLI Interface Contract

## Command: create

Create a new PDF document.

### Input
- `--output, -o`: Output PDF file path (required)
- `--title`: Document title (optional)
- `--author`: Document author (optional)
- `--page-size`: Page size (default: A4)
- `--template`: Template file path (optional)

### Output
- Created PDF file at specified path
- Exit code 0 on success

### Errors
- Exit code 1: Invalid output path or insufficient permissions
- Exit code 2: Invalid template file

---

## Command: convert

Convert a file to PDF format.

### Input
- `input`: Input file path (required)
- `output`: Output PDF path (required)
- `--format`: Input format hint (optional, auto-detected)

### Output
- Created PDF file at specified path
- Exit code 0 on success

### Errors
- Exit code 1: Unsupported input format
- Exit code 2: Conversion failed

---

## Command: extract-text

Extract text content from PDF.

### Input
- `input`: Input PDF path (required)
- `output`: Output text file path (required)
- `--encoding`: Text encoding (default: utf-8)

### Output
- Created text file at specified path
- Exit code 0 on success

### Errors
- Exit code 1: Invalid PDF or no text content

---

## Command: extract-schema

Extract table data and generate SQL schema from PDF.

### Input
- `input`: Input PDF path (required)
- `--output, -o`: Output SQL file path (required)
- `--table-name`: Name for generated table (optional)

### Output
- Created SQL file with CREATE TABLE statements
- Exit code 0 on success

### Errors
- Exit code 1: No tables found in PDF
- Exit code 2: Extraction failed

---

## Command: batch-convert

Convert multiple files to PDF.

### Input
- `--input-dir, -i`: Input directory (required)
- `--output-dir, -o`: Output directory (required)
- `--pattern`: File pattern (default: *.*)

### Output
- PDF files in output directory
- Exit code 0 on success

### Errors
- Exit code 1: Invalid directories
- Exit code 2: Some conversions failed (check logs)