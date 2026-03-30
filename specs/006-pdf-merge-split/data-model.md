# Data Model: PDF Merge and Split

**Feature**: 006-pdf-merge-split  
**Date**: 2026-03-23

## Entities

### PageRange
Represents a specification for which pages to extract from a PDF.

| Field | Type | Description |
|-------|------|-------------|
| start | int | Start page (1-indexed), 0 if omitted (-3 case) |
| end | int | End page (1-indexed), None if omitted (5- case) |
| specific_pages | list[int] | Explicit pages when using comma format |

**Validation**:
- start >= 1
- end >= start (when both specified)
- specific_pages sorted and unique

### MergeRequest
Request to merge multiple PDFs.

| Field | Type | Description |
|-------|------|-------------|
| source_files | list[str] | Ordered list of PDF file paths |
| output_path | str | Destination file path |
| progress_callback | callable | Optional callback for progress |

### SplitRequest
Request to split a PDF by page specification.

| Field | Type | Description |
|-------|------|-------------|
| source_file | str | Input PDF path |
| output_path | str | Destination file path (or base for individual pages) |
| split_mode | str | "range", "individual", "every_n" |
| page_spec | str\|int | Page range string or N for "every_n" |

### PDFOperationResult
Result of a merge/split operation.

| Field | Type | Description |
|-------|------|-------------|
| success | bool | Whether operation succeeded |
| output_files | list[str] | Created file paths |
| error_message | str | Error description if failed |
| pages_processed | int | Number of pages processed |

## State Transitions

```
User selects files → User specifies split/merge → Validate → Execute → Result
                                                                       
Valid page range: Parse string → [start, end] or [specific_pages]
Invalid page range: Return error before execution
```

## Validation Rules

1. All source PDF files must exist and be readable
2. Page range must be within document page bounds
3. Output path must be writable (parent directory exists)
4. No password-protected PDFs (skip with clear error)