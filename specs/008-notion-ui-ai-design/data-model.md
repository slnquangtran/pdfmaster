# Data Model: Notion-Style UI with AI Design Features

**Feature**: 008-notion-ui-ai-design  
**Date**: 2026-03-23

## Entities

### Document
Represents a PDF document in the workspace.

| Field | Type | Description |
|-------|------|-------------|
| id | str | Unique document identifier |
| title | str | Document title |
| icon | str | Emoji or icon identifier |
| cover | Optional[str] | Cover image path |
| author | str | Document author |
| created_at | datetime | Creation timestamp |
| modified_at | datetime | Last modification timestamp |
| parent_id | Optional[str] | Parent document ID for hierarchy |
| tags | List[str] | Associated tags |
| status | str | Document status (draft, published, archived) |
| metadata | dict | Additional metadata |

### Page
A single page within a document.

| Field | Type | Description |
|-------|------|-------------|
| id | str | Unique page identifier |
| document_id | str | Parent document ID |
| page_number | int | Page position (1-indexed) |
| blocks | List[str] | Ordered list of block IDs |
| width | float | Page width in points |
| height | float | Page height in points |
| rotation | int | Page rotation (0, 90, 180, 270) |

### Block
Base class for all content blocks.

| Field | Type | Description |
|-------|------|-------------|
| id | str | Unique block identifier |
| type | str | Block type (text, heading, image, etc.) |
| page_id | str | Parent page ID |
| parent_id | Optional[str] | Parent block ID for nesting |
| position | int | Position within parent |
| content | dict | Block-specific content |
| properties | dict | Block properties (style, color, etc.) |
| children | List[str] | Child block IDs |
| created_at | datetime | Creation timestamp |
| modified_at | datetime | Last modification timestamp |

### Block Types

#### TextBlock
| Field | Type | Description |
|-------|------|-------------|
| text | str | Plain text content |
| font_family | str | Font name |
| font_size | int | Font size in pixels |
| font_weight | str | normal, bold |
| font_style | str | normal, italic, underline, strikethrough |
| color | str | Text color (hex) |
| alignment | str | left, center, right, justify |

#### HeadingBlock (extends TextBlock)
| Field | Type | Description |
|-------|------|-------------|
| level | int | Heading level (1, 2, 3) |

#### ImageBlock
| Field | Type | Description |
|-------|------|-------------|
| source | str | Image file path or URL |
| width | float | Display width |
| height | float | Display height |
| alt_text | str | Alternative text |
| caption | str | Image caption |
| alignment | str | Image alignment |

#### PDFBlock
| Field | Type | Description |
|-------|------|-------------|
| pdf_path | str | Source PDF file path |
| page_range | Tuple[int, int] | Page range to display |
| zoom | float | Zoom level |
| show_controls | bool | Show page navigation controls |

#### AIBlock
| Field | Type | Description |
|-------|------|-------------|
| prompt | str | AI generation prompt |
| result | dict | Generated content |
| status | str | pending, generating, complete, error |
| variations | List[dict] | Alternative generations |

### Workspace
User's document collection and settings.

| Field | Type | Description |
|-------|------|-------------|
| id | str | Workspace identifier |
| name | str | Workspace name |
| documents | List[str] | Document IDs |
| favorites | List[str] | Favorited document IDs |
| recent | List[str] | Recently opened document IDs |
| tags | Dict[str, List[str]] | Tag to document mapping |
| settings | dict | User preferences |
| created_at | datetime | Creation timestamp |

### Style
Reusable styling configuration.

| Field | Type | Description |
|-------|------|-------------|
| id | str | Style identifier |
| name | str | Style name |
| type | str | document, block, theme |
| colors | dict | Color definitions |
| fonts | dict | Font configurations |
| spacing | dict | Spacing values |
| is_default | bool | Is default style |

### AIJob
Represents an AI generation request.

| Field | Type | Description |
|-------|------|-------------|
| id | str | Job identifier |
| type | str | generate_design, suggest_style, generate_content |
| prompt | str | User prompt |
| context | dict | Document context |
| status | str | pending, processing, complete, failed |
| result | dict | Generated output |
| created_at | datetime | Request timestamp |
| completed_at | Optional[datetime] | Completion timestamp |

## State Transitions

### Document States
```
[Draft] → [Published] → [Archived]
   ↑           ↓
   └───────────┘
```

### Block States
```
[Empty] → [Editing] → [Saved]
            ↓
         [Deleted]
```

### AI Job States
```
[Pending] → [Processing] → [Complete]
                ↓
             [Failed] → [Retrying] → [Processing]
```

## Relationships

```
Workspace 1──* Document 1──* Page 1──* Block
                    │                    │
                    └── Style            └── Block (children)
                    
AIJob ── Document (context)
```

## Validation Rules

1. Block position must be unique within its parent
2. Document title cannot be empty
3. Page number must be positive and sequential
4. Block children must exist within the same page
5. Parent reference must not create circular dependencies
6. AI job prompt must be between 10-5000 characters
7. Style colors must be valid hex values
