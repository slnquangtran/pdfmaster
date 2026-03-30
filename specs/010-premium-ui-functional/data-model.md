# Data Model: Premium UI Functional Implementation

**Date**: 2026-03-30  
**Feature**: Premium UI Functional Implementation

## Entities

### PDFDocument

Represents a PDF file with metadata.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | Integer | Unique identifier | Primary key, auto-increment |
| path | String | Absolute file path | Unique, not null |
| name | String | File name | Not null |
| size | Integer | File size in bytes | |
| modified_date | Integer | Last modified timestamp | Unix epoch |
| page_count | Integer | Number of pages | |
| is_scanned | Boolean | Whether document is a scan | Default false |
| has_annotations | Boolean | Whether document has annotations | Default false |
| starred | Boolean | User-starred flag | Default false |
| archived | Boolean | Archived flag | Default false |
| last_accessed | Integer | Last access timestamp | Unix epoch |
| created_at | Integer | Cache entry creation time | Unix epoch |

**Relationships**:
- Many-to-many with Collection through document_collections

**State Transitions**:
```
New → Cached → Active → Modified → Saved
              ↓        ↓
           Archived  Starred
```

**Validation Rules**:
- path must be a valid file path
- size must be positive
- page_count must be positive

---

### Collection

A user-defined group of documents.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | Integer | Unique identifier | Primary key, auto-increment |
| name | String | Collection name | Unique, not null |
| color | String | Display color (hex) | Default "#004f8f" |
| created_at | Integer | Creation timestamp | Unix epoch |

**Relationships**:
- Many-to-many with PDFDocument through document_collections

**Validation Rules**:
- name must not be empty
- name must be unique
- color must be valid hex color

---

### DocumentCollection (Junction Table)

Links documents to collections.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| document_id | Integer | Document reference | Foreign key to documents |
| collection_id | Integer | Collection reference | Foreign key to collections |

**Primary Key**: (document_id, collection_id)

---

### Workspace

Configuration for the user's workspace.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | Integer | Unique identifier | Primary key (always 1) |
| library_path | String | Path to PDF library directory | Not null |
| theme | String | UI theme preference | "light" or "dark" |
| last_scan | Integer | Last full library scan timestamp | Unix epoch |

**Singleton**: Only one workspace configuration exists.

---

### Annotation

A user annotation on a PDF document.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | Integer | Unique identifier | Primary key, auto-increment |
| document_id | Integer | Document reference | Foreign key to documents |
| page_num | Integer | Page number (0-indexed) | Not null |
| type | String | Annotation type | "text", "highlight", "note", "drawing" |
| content | Text | Annotation content/JSON | |
| x | Float | X position on page | 0.0-1.0 normalized |
| y | Float | Y position on page | 0.0-1.0 normalized |
| width | Float | Width (for rectangles) | |
| height | Float | Height (for rectangles) | |
| color | String | Annotation color | Hex color |
| author | String | Author name | |
| created_at | Integer | Creation timestamp | Unix epoch |
| modified_at | Integer | Last modification timestamp | Unix epoch |

**Relationships**:
- Belongs to PDFDocument

**State Transitions**:
```
Created → Saved → Synced
    ↓
  Deleted
```

---

## Database Schema

```sql
-- Documents table
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    size INTEGER,
    modified_date INTEGER,
    page_count INTEGER,
    is_scanned BOOLEAN DEFAULT 0,
    has_annotations BOOLEAN DEFAULT 0,
    starred BOOLEAN DEFAULT 0,
    archived BOOLEAN DEFAULT 0,
    last_accessed INTEGER,
    created_at INTEGER
);

-- Collections table
CREATE TABLE IF NOT EXISTS collections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    color TEXT DEFAULT '#004f8f',
    created_at INTEGER
);

-- Document-Collection junction table
CREATE TABLE IF NOT EXISTS document_collections (
    document_id INTEGER,
    collection_id INTEGER,
    PRIMARY KEY (document_id, collection_id),
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    FOREIGN KEY (collection_id) REFERENCES collections(id) ON DELETE CASCADE
);

-- Workspace configuration
CREATE TABLE IF NOT EXISTS workspace (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    library_path TEXT NOT NULL,
    theme TEXT DEFAULT 'light',
    last_scan INTEGER
);

-- Annotations table
CREATE TABLE IF NOT EXISTS annotations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    page_num INTEGER NOT NULL,
    type TEXT NOT NULL,
    content TEXT,
    x REAL,
    y REAL,
    width REAL,
    height REAL,
    color TEXT,
    author TEXT,
    created_at INTEGER,
    modified_at INTEGER,
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_documents_path ON documents(path);
CREATE INDEX IF NOT EXISTS idx_documents_modified ON documents(modified_date);
CREATE INDEX IF NOT EXISTS idx_documents_starred ON documents(starred);
CREATE INDEX IF NOT EXISTS idx_annotations_document ON annotations(document_id);
```

---

## In-Memory Models (Python Classes)

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class PDFDocument:
    id: Optional[int]
    path: str
    name: str
    size: int
    modified_date: datetime
    page_count: int
    is_scanned: bool = False
    has_annotations: bool = False
    starred: bool = False
    archived: bool = False
    last_accessed: Optional[datetime] = None
    collections: List[str] = None
    
    @property
    def size_mb(self) -> float:
        return self.size / (1024 * 1024)

@dataclass
class Collection:
    id: Optional[int]
    name: str
    color: str = "#004f8f"
    document_count: int = 0

@dataclass
class Annotation:
    id: Optional[int]
    document_id: int
    page_num: int
    type: str  # "text", "highlight", "note", "drawing"
    content: str
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    color: str = "#FFFF00"
    author: str = "User"
    created_at: datetime = None
```
