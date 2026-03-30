# Quickstart: PDF Merge and Split

**Feature**: 006-pdf-merge-split

## CLI Usage

```bash
# Merge PDFs
python -m pdfmaster merge file1.pdf file2.pdf file3.pdf -o merged.pdf

# Split by page range
python -m pdfmaster split input.pdf -o output.pdf -r 1-3

# Split into individual pages
python -m pdfmaster split input.pdf -o output.pdf --individual
```

## GUI Usage

1. Launch the application: `python -m pdfmaster`
2. Navigate to new "Merge/Split" tab in sidebar
3. Select operation: Merge or Split
4. For Merge: Add PDF files, reorder as needed
5. For Split: Enter page range or select "individual pages"
6. Click "Execute" to run operation
7. Progress shown in status bar

## Page Range Formats

| Format | Example | Meaning |
|--------|---------|---------|
| Range | `1-3` | Pages 1, 2, 3 |
| To end | `5-` | Page 5 to last page |
| From start | `-3` | First 3 pages |
| Specific | `1,3,5` | Pages 1, 3, 5 |

## Output Files

- Merged: `[name]_merged.pdf`
- Individual: `[name]_page_1.pdf`, `[name]_page_2.pdf`, etc.
- Page range: User-specified filename