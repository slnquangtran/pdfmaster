# Research: PDF Merge and Split

**Feature**: 006-pdf-merge-split  
**Date**: 2026-03-23

## Technology Decision

### Selected Tool: PyMuPDF (fitz)

**Decision**: Use PyMuPDF (imported as `fitz`) - already a project dependency

**Rationale**:
- Already installed in project
- High performance (C-based MuPDF engine)
- Supports all required operations: merge, split, page extraction
- Clean API: `doc.insert_pdf()`, `doc.delete_page()`, etc.

**Alternatives considered**:
- pypdf (PyPDF2): Also available, but PyMuPDF is faster and more feature-rich
- pdfplumber: Good for extraction, not for merge/split

## Implementation Patterns

### Merge Multiple PDFs
```python
import fitz
doc = fitz.open()
for pdf_path in pdf_list:
    doc2 = fitz.open(pdf_path)
    doc.insert_pdf(doc2)
    doc2.close()
doc.save(output_path)
```

### Split by Page Range
```python
import fitz
doc = fitz.open(input_path)
output = fitz.open()
# Parse "1-3" or "5-" or "-3" or "1,3,5"
output.insert_pdf(doc, from_page=start, to_page=end)
output.save(output_path)
```

### Split into Individual Pages
```python
import fitz
doc = fitz.open(input_path)
for page_num in range(len(doc)):
    new_doc = fitz.open()
    new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
    new_doc.save(f"{base}_page_{page_num+1}.pdf")
```

### Page Range Parser
- "1-3" → pages 1, 2, 3 (1-indexed)
- "5-" → pages 5 to end
- "-3" → pages 1 to 3
- "1,3,5" → pages 1, 3, 5

Convert to 0-indexed for PyMuPDF: subtract 1 from page numbers.

## Error Handling

- `fitz.FileNotFoundError`: Invalid file path
- `fitz.PasswordError`: PDF is locked
- `ValueError`: Invalid page range format
- `IndexError`: Page range exceeds document length

## File Naming

- Merged output: `[original_name]_merged.pdf`
- Individual pages: `[original_name]_page_[n].pdf`
- Default output directory: QStandardPaths.DocumentsLocation

## Testing Strategy

- Unit tests for page range parsing
- Unit tests for merge/split logic
- Integration tests with sample PDFs