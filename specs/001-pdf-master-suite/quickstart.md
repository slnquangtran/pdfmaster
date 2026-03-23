# Quick Start: PDF Master Suite

## Installation

```bash
pip install pdfmaster
```

Or install from source:

```bash
git clone <repo>
cd pdfmaster
pip install -e .
```

## CLI Commands

### Create a PDF

```bash
pdfmaster create --output document.pdf --title "My Document"
```

### Convert File to PDF

```bash
pdfmaster convert input.docx output.pdf
pdfmaster convert input.xlsx output.pdf
pdfmaster convert image.png output.pdf
```

### Extract Text from PDF

```bash
pdfmaster extract-text input.pdf output.txt
```

### Extract Tables and Generate SQL Schema

```bash
pdfmaster extract-schema input.pdf --output schema.sql
```

### Batch Conversion

```bash
pdfmaster batch-convert --input-dir ./docs --output-dir ./pdfs
```

## Python API

```python
from pdfmaster import PDFCreator, PDFConverter, TextExtractor, SchemaExtractor

# Create PDF
creator = PDFCreator()
creator.add_text("Hello, World!")
creator.save("output.pdf")

# Convert to PDF
converter = PDFConverter()
converter.convert("input.docx", "output.pdf")

# Extract text
extractor = TextExtractor()
text = extractor.extract("document.pdf")

# Generate SQL schema
schema_extractor = SchemaExtractor()
schema = schema_extractor.extract("data.pdf")
schema.to_sql("schema.sql")
```

## Supported Formats

| Input Format | Output |
|--------------|--------|
| DOCX, DOC | PDF |
| XLSX, XLS | PDF |
| TXT | PDF |
| PNG, JPG, JPEG | PDF |
| HTML | PDF |
| PDF | TXT |
| PDF | SQL Schema |

## Options

See `pdfmaster --help` for all available commands and options.