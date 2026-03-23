# Quick Start: PDF Master Desktop Application

## Running the Application

### Development Mode

```bash
# Install dependencies
pip install PyQt6 pyinstaller

# Run the application
python pdfmaster/ui/main.py
```

### From Executable (After Build)

```bash
# Installer version
./dist/PDFMasterSetup.exe

# Portable version
./dist/PDFMaster/PDFMaster.exe
```

## Application Features

### Main Window

The main window provides access to all PDF operations through a sidebar navigation:

1. **Create PDF** - Create new PDF documents with text and images
2. **Convert** - Convert files (DOCX, TXT, images) to PDF
3. **Extract Text** - Extract text content from PDFs
4. **Extract Schema** - Extract tables and generate SQL schema

### Creating a PDF

1. Click "Create PDF" in sidebar
2. Enter document title and author (optional)
3. Type your content in the text area
4. Click "Preview" to see the PDF
5. Click "Save" to save the PDF

### Converting Files

1. Click "Convert" in sidebar
2. Drag files into the drop zone OR click to browse
3. Select output directory
4. Click "Convert"
5. View results in the output list

### Extracting Text

1. Click "Extract" in sidebar
2. Select "Text" as operation type
3. Drop or browse for a PDF file
4. Click "Extract"
5. Click "Save" to save the extracted text

### Extracting SQL Schema

1. Click "Extract" in sidebar
2. Select "SQL Schema" as operation type
3. Drop or browse for a PDF file
4. Optionally enter a table name
5. Click "Extract"
6. Preview the generated SQL
7. Click "Save" to export the schema

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New document |
| Ctrl+O | Open file |
| Ctrl+S | Save |
| Ctrl+Q | Quit |
| F11 | Toggle fullscreen |

## Troubleshooting

### Application won't start

- Ensure Python 3.10+ is installed
- Run with `-v` flag for verbose output

### PDF preview not working

- Check that PDF.js is properly embedded
- Try Chrome-based PDF viewer option

### Conversion fails

- Verify source file is not corrupted
- Check write permissions on output directory