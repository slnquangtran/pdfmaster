# Contract: Library Service

**Date**: 2026-03-30  
**Service**: Document Library Management

## Overview

The Library Service manages the user's PDF document collection, including scanning, metadata caching, filtering, and sorting.

## Interface

### LibraryManager

```python
class LibraryManager:
    """Manages the document library"""
    
    def __init__(self, library_path: str):
        """Initialize library with the given directory path"""
        
    def scan(self) -> List[PDFDocument]:
        """
        Scan library directory for PDF files.
        Returns: List of discovered documents
        """
        
    def get_documents(
        self,
        filter_type: str = "all",  # "all", "pdfs", "scans", "markups"
        sort_by: str = "name",     # "name", "date", "size"
        sort_order: str = "asc",   # "asc", "desc"
        collection: str = None,    # Collection name or None
        starred: bool = None,      # Filter starred or None
        archived: bool = None,     # Filter archived or None
        search_query: str = None   # Search query or None
    ) -> List[PDFDocument]:
        """
        Get filtered and sorted document list.
        Returns: Filtered list of documents
        """
        
    def get_document(self, path: str) -> Optional[PDFDocument]:
        """
        Get a single document by path.
        Returns: Document or None if not found
        """
        
    def get_recent(self, limit: int = 10) -> List[PDFDocument]:
        """
        Get recently accessed documents.
        Returns: List of recent documents
        """
        
    def get_storage_usage(self) -> Dict[str, int]:
        """
        Get storage usage statistics.
        Returns: {"used": bytes, "total": bytes, "document_count": int}
        """
        
    def refresh(self):
        """Force a full library rescan"""
```

### Document Operations

```python
class DocumentOperations:
    """Operations on individual documents"""
    
    def open(self, path: str) -> PDFDocument:
        """
        Open a document and update last_accessed timestamp.
        Returns: The opened document
        Raises: FileNotFoundError if file doesn't exist
        """
        
    def rename(self, path: str, new_name: str) -> PDFDocument:
        """
        Rename a document.
        Returns: Updated document
        Raises: FileNotFoundError, FileExistsError
        """
        
    def delete(self, path: str, permanent: bool = False) -> bool:
        """
        Delete or archive a document.
        Returns: True if successful
        """
        
    def move(self, path: str, new_path: str) -> PDFDocument:
        """
        Move a document to a new location.
        Returns: Updated document
        """
        
    def toggle_starred(self, path: str) -> PDFDocument:
        """
        Toggle starred status.
        Returns: Updated document
        """
```

### Collection Operations

```python
class CollectionOperations:
    """Operations for document collections"""
    
    def create(self, name: str, color: str = "#004f8f") -> Collection:
        """
        Create a new collection.
        Returns: Created collection
        Raises: ValueError if name exists
        """
        
    def delete(self, collection_id: int) -> bool:
        """
        Delete a collection.
        Returns: True if successful
        """
        
    def rename(self, collection_id: int, new_name: str) -> Collection:
        """
        Rename a collection.
        Returns: Updated collection
        """
        
    def add_document(self, collection_id: int, document_path: str) -> bool:
        """
        Add a document to a collection.
        Returns: True if successful
        """
        
    def remove_document(self, collection_id: int, document_path: str) -> bool:
        """
        Remove a document from a collection.
        Returns: True if successful
        """
        
    def get_documents(self, collection_id: int) -> List[PDFDocument]:
        """
        Get all documents in a collection.
        Returns: List of documents
        """
        
    def list_all(self) -> List[Collection]:
        """
        List all collections.
        Returns: List of collections with document counts
        """
```

## Events

The service emits the following events:

| Event | Payload | Description |
|-------|---------|-------------|
| document_added | PDFDocument | New document discovered |
| document_removed | str (path) | Document deleted |
| document_updated | PDFDocument | Document metadata changed |
| collection_changed | Collection | Collection created/deleted/modified |
| scan_complete | int (count) | Full scan completed |
| storage_updated | Dict | Storage usage changed |

## Error Handling

| Error Type | Condition | Recovery |
|------------|-----------|----------|
| FileNotFoundError | Document path invalid | Remove from cache |
| PermissionError | Cannot access file | Show user warning |
| DiskFullError | Cannot write to disk | Show user warning |

## Performance Requirements

- `scan()`: Complete within 5s for 1000 documents
- `get_documents()`: Return within 100ms with cached data
- `get_storage_usage()`: Calculate within 1s
- Events: Emit within 50ms of state change
