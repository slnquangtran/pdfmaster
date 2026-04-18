# PDF Master Suite

Comprehensive PDF application for creation, editing, design, and conversion.

## Features

- **Create PDFs**: Generate new PDF documents from scratch or templates
- **Edit PDFs**: Modify existing PDF documents (text, images, pages)
- **Convert to PDF**: Convert DOCX, XLSX, TXT, images, HTML to PDF
- **Extract Text**: Extract text content from PDF files
- **Design Layouts**: Create professionally designed PDFs with templates
- **SQL Schema**: Extract table data from PDFs and generate SQL schemas

## Desktop Application (GUI)

### Quick Start

Run the GUI application directly:

```bash
python -c "import sys; sys.path.insert(0, '.'); from pdfmaster.ui.main import main; main()"
```

Or use the launcher script (Windows):

```bash
python pdfmaster\run_gui.bat
```

The desktop application provides:
- Modern sidebar navigation
- Create PDF with text and formatting
- Drag-and-drop file conversion
- Extract text from PDFs
- Extract SQL schema from PDF tables
- Progress indicators for all operations
- Error handling with friendly messages

## Installation

```bash
pip install pdfmaster
```

Or install from source:

```bash
git clone <repository>
cd pdfmaster
pip install -e .
```

## CLI Usage

### Create a PDF

```bash
pdfmaster create --output document.pdf --title "My Document" --author "John Doe"
```

### Convert File to PDF

```bash
pdfmaster convert input.docx output.pdf
pdfmaster convert image.png output.pdf
pdfmaster convert document.txt output.pdf
```

### Extract Text from PDF

```bash
pdfmaster extract-text input.pdf output.txt
```

### Extract SQL Schema from PDF

```bash
pdfmaster extract-schema input.pdf --output schema.sql
```

### Batch Conversion

```bash
pdfmaster batch-convert --input-dir ./docs --output-dir ./pdfs
```

## Python API

```python
from pdfmaster.src.core.creator import PDFCreator

# Create PDF
creator = PDFCreator(title="My Document", author="John Doe")
creator.add_text("Hello, World!", font_size=24)
creator.add_text("This is a new paragraph.", y=700)
creator.save("output.pdf")

from pdfmaster.src.converters import convert_file

# Convert to PDF
convert_file("input.docx", "output.pdf")

from pdfmaster.src.extractors.text_extractor import TextExtractor

# Extract text
extractor = TextExtractor()
text = extractor.extract("document.pdf")

from pdfmaster.src.extractors.schema_generator import SchemaGenerator

# Generate SQL schema
generator = SchemaGenerator()
schema = generator.extract("data.pdf")
```

## Supported Formats

| Input Format | Output |
|--------------|--------|
| DOCX, DOC | PDF |
| XLSX, XLS | PDF |
| TXT | PDF |
| PNG, JPG, JPEG, GIF, BMP | PDF |
| HTML, HTM | PDF |
| PDF | TXT |
| PDF | SQL Schema |

## Requirements

- Python 3.10+
- ReportLab
- PyMuPDF
- pypdf
- pdfplumber
- Click
- Pillow

## License

MIT

## CI

- This project uses GitHub Actions to run tests and lint checks on pull requests.
- You can see the pipeline at .github/workflows/ci.yml.
