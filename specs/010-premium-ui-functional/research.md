# Research: Premium UI Functional Implementation

**Date**: 2026-03-30  
**Feature**: Premium UI Functional Implementation  
**Phase**: 0 - Research

## 1. PyMuPDF Capabilities

### Decision: Use PyMuPDF (fitz) as primary PDF library

**Rationale**: PyMuPDF provides comprehensive PDF manipulation capabilities including:
- PDF rendering with pixmap generation
- Text extraction and search
- Page manipulation (insert, delete, rotate, crop)
- Annotation support (text, highlight, drawing, stamp)
- Merging and splitting documents
- Encryption/decryption (AES-256)
- Digital signature verification
- Image extraction
- Form field manipulation

**Key APIs**:
- `fitz.open()` - Open PDF documents
- `doc.merge_pdf()` - Merge documents
- `page.get_text()` - Extract text
- `page.add_redact_annot()` - Redaction annotations
- `page.add_text_annot()` - Text annotations
- `page.insert_pdf()` - Insert pages from another PDF

**Limitations**:
- Digital signature creation requires additional library (cryptography)
- Complex DOCX/XLSX conversion needs external tools (docx2pdf, LibreOffice)

**Alternatives considered**:
- pypdf - Limited rendering, no text extraction from complex layouts
- pdfplumber - Good for tables, limited editing capabilities

---

## 2. PyQt6 Document Viewer

### Decision: Use QGraphicsView with custom PDF page items

**Rationale**: QGraphicsView provides:
- Efficient viewport management for multi-page documents
- Built-in zoom and pan support
- Scalable rendering with transform
- Easy page layout management

**Architecture**:
```
PDFViewer (QGraphicsView)
└── QGraphicsScene
    ├── PDFPageItem (QGraphicsPixmapItem) x N pages
    ├── AnnotationLayer (QGraphicsItem)
    └── SelectionOverlay (QGraphicsItem)
```

**Key considerations**:
- Render pages to QPixmap using `page.get_pixmap()`
- Cache rendered pages to avoid re-rendering on scroll
- Use `QGraphicsView.cacheMode` for smooth scrolling
- Implement lazy loading for large documents

**Alternatives considered**:
- QLabel with QPixmap - Simple but no multi-page support, poor performance
- Custom QWidget with QPainter - Maximum control but requires more code
- QWebView with PDF.js - Cross-platform rendering but heavy dependency

---

## 3. File System Watching

### Decision: Use QFileSystemWatcher with periodic refresh fallback

**Rationale**: 
- QFileSystemWatcher provides real-time file change notifications
- Fallback to periodic scan for network drives or unsupported filesystems

**Implementation**:
```python
watcher = QFileSystemWatcher()
watcher.addPath(library_directory)
watcher.directoryChanged.connect(refresh_library)
watcher.fileChanged.connect(update_document_metadata)
```

**Considerations**:
- Watcher has limit on number of watched files (platform-dependent)
- For large libraries, watch directory rather than individual files
- Debounce refresh signals to avoid excessive updates

---

## 4. Background Processing

### Decision: Use QThreadPool with QRunnable for PDF operations

**Rationale**:
- QThreadPool manages worker threads efficiently
- QRunnable provides lightweight task execution
- Signals/slots allow safe UI updates from worker threads

**Pattern**:
```python
class PDFOperation(QRunnable):
    def __init__(self, operation_type, params):
        super().__init__()
        self.operation_type = operation_type
        self.params = params
        self.signals = PDFOperationSignals()
    
    def run(self):
        # Perform PDF operation
        result = perform_operation(self.params)
        self.signals.finished.emit(result)

# Usage
operation = PDFOperation("merge", file_list)
operation.signals.finished.connect(on_merge_complete)
QThreadPool.globalInstance().start(operation)
```

**Error handling**:
- Catch exceptions in worker thread
- Emit error signal with exception details
- Display error dialog in UI thread

---

## 5. SQLite Metadata Caching

### Decision: Use SQLite for document metadata cache

**Rationale**:
- Fast queries for filtering and sorting
- Persistent across sessions
- Handles 10k+ documents efficiently
- Built-in Python support

**Schema**:
```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    path TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    size INTEGER,
    modified_date INTEGER,
    page_count INTEGER,
    is_scanned BOOLEAN,
    has_annotations BOOLEAN,
    starred BOOLEAN DEFAULT 0,
    archived BOOLEAN DEFAULT 0,
    last_accessed INTEGER,
    created_at INTEGER
);

CREATE TABLE collections (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    created_at INTEGER
);

CREATE TABLE document_collections (
    document_id INTEGER,
    collection_id INTEGER,
    PRIMARY KEY (document_id, collection_id)
);

CREATE INDEX idx_path ON documents(path);
CREATE INDEX idx_modified ON documents(modified_date);
CREATE INDEX idx_starred ON documents(starred);
```

**Update strategy**:
- On startup: Full scan if database is empty or library directory changed
- On file watcher event: Update single document entry
- Periodic: Full rescan every 24 hours or on demand

---

## 6. PDF Rendering Performance

### Decision: Implement progressive loading with page caching

**Rationale**: Large PDFs (100+ pages) should not block the UI during initial load.

**Strategy**:
1. Load document structure immediately (page count, metadata)
2. Render visible pages first (current viewport ± 2 pages)
3. Render adjacent pages in background
4. Cache rendered pixmaps with LRU eviction

**Cache implementation**:
```python
class PageCache:
    def __init__(self, max_size=50):
        self.cache = LRUCache(max_size)
    
    def get_page(self, doc_path, page_num, zoom_level):
        key = (doc_path, page_num, zoom_level)
        if key in self.cache:
            return self.cache[key]
        
        pixmap = render_page(doc_path, page_num, zoom_level)
        self.cache[key] = pixmap
        return pixmap
```

---

## 7. Multi-Format Conversion

### Decision: Use existing converters with subprocess for external tools

**Rationale**: 
- docx2pdf library for Word/Excel/PowerPoint to PDF
- WeasyPrint for HTML to PDF
- PyMuPDF for text extraction

**Conversion pipeline**:
```
Input File → Determine format → Select converter → Convert → Output PDF
                                    ↓
                            docx2pdf (DOCX, XLSX, PPTX)
                            WeasyPrint (HTML)
                            PyMuPDF (images)
```

**Fallback**: If external tools not available, show user-friendly error with installation instructions.

---

## Summary

| Question | Decision | Confidence |
|----------|----------|------------|
| Primary PDF library | PyMuPDF (fitz) | High |
| Document viewer | QGraphicsView | High |
| File watching | QFileSystemWatcher | High |
| Background processing | QThreadPool + QRunnable | High |
| Metadata storage | SQLite | High |
| Multi-format conversion | docx2pdf + WeasyPrint | Medium |

No [NEEDS CLARIFICATION] items remain.
