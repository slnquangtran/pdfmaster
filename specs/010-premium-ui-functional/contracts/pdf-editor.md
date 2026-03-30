# Contract: PDF Editor

**Date**: 2026-03-30  
**Service**: PDF Document Viewing and Editing

## Overview

The PDF Editor provides document viewing, navigation, zooming, and annotation capabilities.

## Interface

### PDFViewer

```python
class PDFViewer:
    """PDF document viewer widget"""
    
    def open(self, path: str, password: str = None) -> None:
        """
        Open a PDF document for viewing.
        Raises: 
            FileNotFoundError - file not found
            PasswordError - incorrect password
        """
        
    def close(self) -> None:
        """Close the current document"""
        
    @property
    def is_open(self) -> bool:
        """Check if a document is open"""
        
    @property
    def page_count(self) -> int:
        """Get total page count"""
        
    @property
    def current_page(self) -> int:
        """Get current page number (1-indexed)"""
        
    @current_page.setter
    def current_page(self, page: int) -> None:
        """Navigate to a specific page"""
        
    def next_page(self) -> None:
        """Go to next page"""
        
    def previous_page(self) -> None:
        """Go to previous page"""
        
    def first_page(self) -> None:
        """Go to first page"""
        
    def last_page(self) -> None:
        """Go to last page"""
```

### Zoom Controls

```python
class ZoomControls:
    """Zoom and view controls"""
    
    @property
    def zoom_level(self) -> float:
        """Get current zoom level (1.0 = 100%)"""
        
    @zoom_level.setter
    def zoom_level(self, level: float) -> None:
        """
        Set zoom level.
        Valid range: 0.5 - 4.0 (50% - 400%)
        """
        
    def zoom_in(self, step: float = 0.25) -> None:
        """Zoom in by step"""
        
    def zoom_out(self, step: float = 0.25) -> None:
        """Zoom out by step"""
        
    def fit_width(self) -> None:
        """Zoom to fit page width"""
        
    def fit_page(self) -> None:
        """Zoom to fit entire page"""
        
    ZOOM_MIN = 0.5
    ZOOM_MAX = 4.0
    ZOOM_STEP = 0.25
```

### Annotation Tools

```python
class AnnotationTools:
    """Annotation and markup tools"""
    
    def add_text(
        self,
        page: int,
        x: float,
        y: float,
        text: str,
        font_size: int = 12,
        color: str = "#000000"
    ) -> Annotation:
        """
        Add text annotation at position.
        Returns: Created annotation
        """
        
    def add_highlight(
        self,
        page: int,
        rect: Tuple[float, float, float, float],
        color: str = "#FFFF00"
    ) -> Annotation:
        """
        Add highlight annotation.
        rect: (x0, y0, x1, y1) in page coordinates
        Returns: Created annotation
        """
        
    def add_note(
        self,
        page: int,
        x: float,
        y: float,
        content: str,
        author: str = "User"
    ) -> Annotation:
        """
        Add note annotation.
        Returns: Created annotation
        """
        
    def add_drawing(
        self,
        page: int,
        points: List[Tuple[float, float]],
        color: str = "#000000",
        width: float = 1.0
    ) -> Annotation:
        """
        Add freehand drawing.
        Returns: Created annotation
        """
        
    def get_annotations(self, page: int) -> List[Annotation]:
        """
        Get all annotations on a page.
        Returns: List of annotations
        """
        
    def delete_annotation(self, annotation_id: int) -> bool:
        """
        Delete an annotation.
        Returns: True if successful
        """
```

### Document Editing

```python
class DocumentEditing:
    """Document modification operations"""
    
    def insert_text(
        self,
        page: int,
        x: float,
        y: float,
        text: str,
        font_name: str = "helv",
        font_size: int = 12
    ) -> bool:
        """
        Insert text into document.
        Returns: True if successful
        """
        
    def delete_text(self, page: int, rect: Tuple[float, float, float, float]) -> bool:
        """
        Delete text from document (redact).
        Returns: True if successful
        """
        
    def insert_image(
        self,
        page: int,
        x: float,
        y: float,
        image_path: str,
        width: float = None,
        height: float = None
    ) -> bool:
        """
        Insert image into document.
        Returns: True if successful
        """
        
    def insert_page(self, position: int, page_data: bytes) -> bool:
        """
        Insert a page from another document.
        Returns: True if successful
        """
        
    def delete_page(self, page: int) -> bool:
        """
        Delete a page from the document.
        Returns: True if successful
        """
        
    def rotate_page(self, page: int, degrees: int = 90) -> bool:
        """
        Rotate a page.
        degrees: 90, 180, or 270
        Returns: True if successful
        """
```

### Save Operations

```python
class SaveOperations:
    """Document save and export"""
    
    def save(self) -> bool:
        """
        Save changes to original file.
        Returns: True if successful
        """
        
    def save_as(self, path: str) -> bool:
        """
        Save to a new file.
        Returns: True if successful
        """
        
    def export(
        self,
        path: str,
        format: str  # "pdf", "png", "jpeg", "text"
    ) -> bool:
        """
        Export document or current page.
        Returns: True if successful
        """
        
    @property
    def has_unsaved_changes(self) -> bool:
        """Check if there are unsaved changes"""
```

## Events

| Event | Payload | Description |
|-------|---------|-------------|
| document_opened | str (path) | Document opened |
| document_closed | None | Document closed |
| page_changed | int (page) | Current page changed |
| zoom_changed | float (level) | Zoom level changed |
| annotation_added | Annotation | New annotation created |
| annotation_deleted | int (id) | Annotation removed |
| content_modified | None | Document content changed |
| save_completed | bool (success) | Save operation completed |

## Rendering Requirements

- Pages render within 100ms for standard documents
- Zoom changes apply within 50ms
- Smooth scrolling at 60fps
- Progressive loading for large documents (100+ pages)

## Error Handling

| Error Type | Condition | Recovery |
|------------|-----------|----------|
| PasswordError | PDF is password protected | Prompt for password |
| CorruptedPDFError | PDF structure invalid | Show error, allow cancel |
| MemoryError | Document too large | Show warning, reduce cache |
| PermissionError | Cannot write to file | Prompt for save-as |
