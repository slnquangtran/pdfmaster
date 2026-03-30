# PDF Design Features - Implementation Plan

**Project**: PDF Master Design Suite  
**Version**: 2.0 Design Features  
**Date**: 2026-03-23  
**Related Spec**: Feature enhancement for PDF design capabilities

---

## Executive Summary

This plan outlines a comprehensive PDF design system that transforms PDF Master from a utility tool into a professional document design studio. Users will be able to create visually stunning documents with watermarks, headers/footers, page numbers, table of contents, annotations, and rich styling options.

---

## 1. Feature Overview

### 1.1 Core Design Features

```
PDF Design Suite
├── Page Elements
│   ├── Headers & Footers
│   ├── Page Numbers
│   ├── Watermarks
│   └── Stamps
│
├── Document Structure
│   ├── Table of Contents (TOC)
│   ├── Bookmarks
│   ├── Chapters/Sections
│   └── Cross-references
│
├── Visual Elements
│   ├── Text Styling
│   ├── Image Handling
│   ├── Shapes & Lines
│   ├── Tables
│   └── Lists
│
├── Annotations
│   ├── Sticky Notes
│   ├── Highlights
│   ├── Underlines
│   ├── Shapes
│   └── Freehand Drawing
│
├── Template System
│   ├── Pre-built Templates
│   ├── Custom Templates
│   ├── Style Libraries
│   └── Branding Kits
│
└── Design Studio UI
    ├── Visual Editor
    ├── Element Properties Panel
    ├── Layer Management
    └── Preview Mode
```

---

## 2. Detailed Feature Specifications

### 2.1 Watermarks

#### Watermark Types
| Type | Description | Use Case |
|------|-------------|----------|
| Text | Text overlay with customization | "DRAFT", "CONFIDENTIAL" |
| Image | Logo or image overlay | Company branding |
| Diagonal | Angled text across page | Copyright notices |
| Tiled | Repeated pattern | Security marking |
| Gradient | Fading opacity | Subtle branding |

#### Watermark Properties
```python
@dataclass
class WatermarkConfig:
    type: Literal["text", "image", "diagonal", "tiled", "gradient"]
    content: str  # Text or image path
    opacity: float = 0.3  # 0.0 to 1.0
    rotation: float = 45  # Degrees for diagonal
    position: Tuple[float, float] = (0.5, 0.5)  # Center as percentage
    scale: float = 1.0
    color: Tuple[int, int, int] = (128, 128, 128)
    font_size: int = 48
    font_name: str = "Helvetica"
    apply_to_pages: Union[str, List[int]] = "all"  # "all", "first", "odd", "even", or list
```

#### Operations
- Apply watermark to existing PDF
- Remove watermark from PDF
- Modify watermark settings
- Batch watermark multiple PDFs
- Preview watermark before applying

---

### 2.2 Stamps

#### Stamp Categories
```
Stamps
├── Approval
│   ├── APPROVED (green)
│   ├── REJECTED (red)
│   ├── PENDING (yellow)
│   ├── REVISED (blue)
│   └── DRAFT (gray)
│
├── Status
│   ├── CONFIDENTIAL
│   ├── INTERNAL USE ONLY
│   ├── COPY
│   ├── SAMPLE
│   └── void
│
├── Custom
│   ├── Company Logo
│   ├── Date Stamp
│   ├── Signature Stamp
│   └── Custom Text
│
└── Special
    ├── Date/Time
    ├── Received
    ├── Filed
    └── FAX
```

#### Stamp Properties
```python
@dataclass
class StampConfig:
    stamp_type: Literal["approval", "status", "custom", "special"]
    name: str  # e.g., "APPROVED", "CONFIDENTIAL"
    shape: Literal["rectangle", "oval", "circle"] = "rectangle"
    color: Tuple[int, int, int] = (0, 128, 0)  # Border color
    fill_color: Tuple[int, int, int] = (255, 255, 255)
    border_width: float = 2.0
    opacity: float = 0.8
    rotation: float = 0
    font_size: int = 14
    position: Tuple[float, float] = (0.8, 0.8)  # Page position
    size: Tuple[float, float] = (150, 50)  # Width, Height
```

---

### 2.3 Headers and Footers

#### Header/Footer Elements
```python
@dataclass
class HeaderFooterConfig:
    # Content elements
    show_logo: bool = False
    logo_path: Optional[str] = None
    logo_size: Tuple[float, float] = (50, 25)
    logo_position: Literal["left", "center", "right"] = "left"

    show_title: bool = True
    title_text: str = ""
    title_font_size: int = 10

    show_author: bool = False
    author_text: str = ""

    show_date: bool = True
    date_format: str = "%Y-%m-%d"
    show_time: bool = False

    show_page_number: bool = True
    page_number_format: Literal["1", "1/N", "Page 1 of N", "custom"] = "1/N"
    page_number_position: Literal["left", "center", "right"] = "right"

    # Styling
    background_color: Optional[Tuple[int, int, int]] = None
    text_color: Tuple[int, int, int] = (0, 0, 0)
    font_name: str = "Helvetica"
    font_size: int = 10
    line_separator: bool = True
    line_color: Tuple[int, int, int] = (0, 0, 0)

    # Layout
    height: float = 50  # Points
    margin_left: float = 72
    margin_right: float = 72
    padding_top: float = 10
    padding_bottom: float = 10

    # Page range
    apply_to_pages: Union[str, List[int]] = "all"
    first_page_different: bool = False
    odd_even_different: bool = False
```

#### Placement Options
- Header only
- Footer only
- Both header and footer
- First page different (cover page)
- Odd/Even different (book style)

---

### 2.4 Page Numbers

#### Numbering Formats
| Format | Example | Description |
|--------|---------|-------------|
| Numeric | 1, 2, 3, ... | Standard numbering |
| Roman | I, II, III, ... | Roman numerals |
| Alpha | A, B, C, ... | Alphabetical |
| Custom prefix | Page 1, Page 2, ... | With prefix text |
| Chapter-based | 1-1, 1-2, 2-1, ... | Chapter-Page format |

#### Positioning
```
     Top Left    Top Center    Top Right
     ┌──────────────────────────────────┐
     │                                  │
     │                                  │
     │                                  │
     │                                  │
     │                                  │
     │                                  │
     └──────────────────────────────────┘
   Bottom Left  Bottom Center  Bottom Right
```

#### Configuration
```python
@dataclass
class PageNumberConfig:
    format: Literal["numeric", "roman", "alpha", "custom"] = "numeric"
    prefix: str = ""
    suffix: str = ""
    position: Literal["top-left", "top-center", "top-right", 
                       "bottom-left", "bottom-center", "bottom-right"] = "bottom-center"
    
    font_name: str = "Helvetica"
    font_size: int = 10
    color: Tuple[int, int, int] = (0, 0, 0)
    
    start_number: int = 1
    show_first_page: bool = True
    show_last_page: bool = True
    
    # Chapter-aware numbering
    chapter_aware: bool = False
    chapter_format: str = "{chapter}-{page}"
```

---

### 2.5 Table of Contents (TOC)

#### TOC Structure
```python
@dataclass
class TOCEntry:
    level: int  # 1, 2, 3 for nesting
    title: str
    page_number: int
    children: List['TOCEntry'] = field(default_factory=list)
    bookmark_id: Optional[str] = None

@dataclass
class TOCConfig:
    title: str = "Table of Contents"
    title_font_size: int = 18
    title_font_name: str = "Helvetica-Bold"
    
    # Styling
    entry_font_size: int = 12
    level_indent: float = 20  # Points per level
    show_dots: bool = True  # Dot leaders to page numbers
    dot_character: str = "."
    
    # Level styles (can customize each level)
    level_styles: Dict[int, TOCStyle] = field(default_factory=dict)
    
    # Page settings
    auto_generate: bool = True
    update_before_print: bool = True
    max_depth: int = 3
```

#### TOC Levels
```
1. Chapter Title ...................... 1
   1.1 Section Title .................. 2
       1.1.1 Subsection ............... 3
   1.2 Another Section ................ 5
2. Next Chapter ....................... 8
```

---

### 2.6 Bookmarks

#### Bookmark Features
```python
@dataclass
class Bookmark:
    title: str
    page_number: int
    children: List['Bookmark'] = field(default_factory=list)
    color: Optional[Tuple[int, int, int]] = None
    bold: bool = False
    italic: bool = False
    open: bool = True  # Expanded state

@dataclass
class BookmarkConfig:
    auto_generate_from_headings: bool = True
    heading_levels: List[int] = field(default_factory=lambda: [1, 2, 3])
    preserve_structure: bool = True
    max_depth: int = 4
```

#### Bookmark Operations
- Add manual bookmark at current view
- Add bookmark with page reference
- Reorder bookmarks (drag-drop)
- Nest bookmarks (create hierarchy)
- Delete bookmarks
- Export bookmarks to outline
- Import outline as bookmarks

---

### 2.7 Annotations

#### Annotation Types
```python
class AnnotationType(Enum):
    # Text annotations
    STICKY_NOTE = "sticky_note"
    TEXT_BOX = "text_box"
    CALLOUT = "callout"
    
    # Markup
    HIGHLIGHT = "highlight"
    UNDERLINE = "underline"
    STRIKETHROUGH = "strikethrough"
    SQUIGGLY = "squiggly"
    
    # Drawing
    FREEHAND = "freehand"
    ARROW = "arrow"
    LINE = "line"
    RECTANGLE = "rectangle"
    OVAL = "oval"
    POLYGON = "polygon"
    CLOUD = "cloud"
    
    # Special
    STAMP = "stamp"
    LINK = "link"
    FILE_ATTACHMENT = "file_attachment"
    SOUND = "sound"
    MOVIE = "movie"
```

#### Annotation Properties
```python
@dataclass
class AnnotationConfig:
    type: AnnotationType
    page: int
    
    # Position and size
    rect: Tuple[float, float, float, float]  # x1, y1, x2, y2
    
    # Appearance
    color: Tuple[int, int, int] = (255, 255, 0)  # Yellow for highlight
    opacity: float = 1.0
    border_width: float = 1.0
    
    # Content
    content: str = ""  # Text content or note
    author: str = ""
    subject: str = ""
    created: datetime = field(default_factory=datetime.now)
    modified: datetime = field(default_factory=datetime.now)
    
    # State
    open: bool = False  # For sticky notes
    icon: str = "Note"  # Note, Comment, Key, etc.
    
    # Special properties
    target: Optional[str] = None  # For links
    target_page: Optional[int] = None  # For internal links
```

#### Annotation Tools
```
Annotation Toolbar
├── 💬 Note (Sticky Note)
├── 📝 Text Box
├── 🔵 Highlight
├── ➖ Underline
├── ❌ Strikethrough
├── ✏️ Freehand
├── ↗️ Arrow
├── ── Line
├── ▢ Rectangle
├── ○ Oval
├── 🔗 Link
└── 📎 Attachment
```

---

### 2.8 Text Styling

#### Text Properties
```python
@dataclass
class TextStyle:
    # Font
    font_name: str = "Helvetica"
    font_size: int = 12
    font_weight: Literal["normal", "bold"] = "normal"
    font_style: Literal["normal", "italic", "oblique"] = "normal"
    
    # Color
    font_color: Tuple[int, int, int] = (0, 0, 0)
    
    # Spacing
    line_height: float = 1.2  # Multiplier
    letter_spacing: float = 0  # Additional spacing
    word_spacing: float = 0
    
    # Alignment
    alignment: Literal["left", "center", "right", "justify"] = "left"
    
    # Decorations
    underline: bool = False
    strikethrough: bool = False
    
    # Background
    background_color: Optional[Tuple[int, int, int]] = None
    highlight: bool = False
```

#### Available Fonts
```
Standard PDF Fonts:
├── Helvetica (Arial-like)
│   ├── Helvetica
│   ├── Helvetica-Bold
│   ├── Helvetica-Oblique
│   └── Helvetica-BoldOblique
│
├── Times (Times New Roman-like)
│   ├── Times-Roman
│   ├── Times-Bold
│   ├── Times-Italic
│   └── Times-BoldItalic
│
├── Courier (Monospace)
│   ├── Courier
│   ├── Courier-Bold
│   ├── Courier-Oblique
│   └── Courier-BoldOblique
│
└── Symbol Fonts
    ├── Symbol
    └── ZapfDingbats
```

---

### 2.9 Image Handling

#### Image Operations
```python
@dataclass
class ImageConfig:
    # Source
    source: Union[str, Path, bytes]
    
    # Position and size
    x: float
    y: float
    width: Optional[float] = None
    height: Optional[float] = None
    maintain_aspect: bool = True
    
    # Appearance
    opacity: float = 1.0
    rotation: float = 0
    
    # Border
    border_width: float = 0
    border_color: Tuple[int, int, int] = (0, 0, 0)
    border_radius: float = 0
    
    # Effects
    grayscale: bool = False
    brightness: float = 1.0
    contrast: float = 1.0
    
    # Layout
    page: int = 0
    layer: int = 0  # For stacking order
```

#### Image Features
- Insert images (PNG, JPG, BMP, GIF)
- Resize with aspect ratio lock
- Crop images
- Apply filters (grayscale, sepia, etc.)
- Add borders and shadows
- Image gallery management
- Watermark with images

---

### 2.10 Shapes and Lines

#### Shape Types
```python
class ShapeType(Enum):
    LINE = "line"
    ARROW = "arrow"
    RECTANGLE = "rectangle"
    ROUNDED_RECTANGLE = "rounded_rectangle"
    OVAL = "oval"
    CIRCLE = "circle"
    POLYGON = "polygon"
    STAR = "star"
    CLOUD = "cloud"
    HEART = "heart"
    CALLOUT = "callout"

@dataclass
class ShapeConfig:
    type: ShapeType
    x: float
    y: float
    width: float
    height: float
    
    # Fill
    fill_color: Optional[Tuple[int, int, int]] = None
    fill_opacity: float = 1.0
    
    # Stroke
    stroke_color: Tuple[int, int, int] = (0, 0, 0)
    stroke_width: float = 1.0
    stroke_style: Literal["solid", "dashed", "dotted"] = "solid"
    
    # Special
    rotation: float = 0
    corner_radius: float = 0  # For rounded rectangles
    
    # Text inside shape
    text: Optional[str] = None
    text_style: Optional[TextStyle] = None
```

---

### 2.11 Tables

#### Table Configuration
```python
@dataclass
class TableConfig:
    # Data
    headers: List[str]
    data: List[List[str]]
    
    # Dimensions
    column_widths: Optional[List[float]] = None
    row_height: float = 20
    
    # Position
    x: float = 72
    y: float = 720
    
    # Styling
    header_style: TableCellStyle = field(default_factory=lambda: TableCellStyle(
        background_color=(66, 133, 244),
        font_color=(255, 255, 255),
        font_weight="bold"
    ))
    
    row_style: TableCellStyle = field(default_factory=TableCellStyle)
    alt_row_style: Optional[TableCellStyle] = None  # Alternating rows
    
    # Borders
    show_borders: bool = True
    border_color: Tuple[int, int, int] = (0, 0, 0)
    border_width: float = 0.5
    cell_padding: float = 5
    
    # Special
    repeat_header: bool = True  # On page breaks
    split_cells: bool = True  # Allow split across pages
```

#### Table Features
- Auto-fit to content
- Merge cells
- Column/row spanning
- Sort by column
- Alternating row colors
- Header repetition on new pages

---

### 2.12 Lists

#### List Types
```python
class ListType(Enum):
    BULLET = "bullet"
    NUMBERED = "numbered"
    LETTERED = "lettered"
    ROMAN = "roman"
    CHECKBOX = "checkbox"
    CUSTOM = "custom"

@dataclass
class ListConfig:
    type: ListType = ListType.BULLET
    items: List[str] = field(default_factory=list)
    level: int = 0  # Nesting level
    indent: float = 36
    bullet_size: float = 6
    bullet_color: Tuple[int, int, int] = (0, 0, 0)
    
    # Custom bullets
    custom_bullet: Optional[str] = None
    
    # Numbering
    start_number: int = 1
    number_format: str = "{number}."
```

---

### 2.13 Template System

#### Template Categories
```
Templates
├── Business
│   ├── Business Report
│   ├── Business Letter
│   ├── Invoice
│   ├── Proposal
│   └── Meeting Minutes
│
├── Academic
│   ├── Research Paper
│   ├── Thesis
│   ├── Presentation Notes
│   └── Lab Report
│
├── Creative
│   ├── Newsletter
│   ├── Brochure
│   ├── Flyer
│   └── Poster
│
├── Personal
│   ├── Resume/CV
│   ├── Cover Letter
│   ├── Journal
│   └── Recipe Book
│
└── Custom
    ├── User Templates
    └── Brand Kits
```

#### Brand Kit
```python
@dataclass
class BrandKit:
    name: str
    
    # Colors
    primary_color: Tuple[int, int, int]
    secondary_color: Tuple[int, int, int]
    accent_color: Tuple[int, int, int]
    
    # Fonts
    heading_font: str
    body_font: str
    
    # Logos
    logo_primary: Optional[str] = None  # Path
    logo_secondary: Optional[str] = None  # White/inverse version
    favicon: Optional[str] = None
    
    # Boilerplate
    footer_text: str = ""
    header_text: str = ""
    disclaimer: str = ""
```

---

## 3. Design Studio UI

### 3.1 Main Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  📁 File  │ 📝 Edit  │ 🎨 Design  │ 👁 View  │ ⚙ Settings         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ┌─────────┐┌─────────────────────────────────────────────────────┐ │
│ │Tools    ││                                                     │ │
│ │┌───────┐││                                                     │ │
│ ││Select │││              PDF Page Canvas                        │ │
│ │├───────┤││                                                     │ │
│ ││Text   │││         [WYSIWYG Document Preview]                  │ │
│ │├───────┤││                                                     │ │
│ ││Image  │││                                                     │ │
│ │├───────┤││                                                     │ │
│ ││Shape  │││                                                     │ │
│ │├───────┤││                                                     │ │
│ ││Table  │││                                                     │ │
│ │├───────┤││                                                     │ │
│ ││Annot  │││                                                     │ │
│ │└───────┘││                                                     │ │
│ └─────────┘└─────────────────────────────────────────────────────┘ │
│                                                                     │
│ ┌──────────────────────────────────────────────────────────────┐   │
│ │ 📑 Pages: [1] [2] [3] [4]        Zoom: [100%] [-] [+]      │   │
│ └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Properties Panel

```
┌─────────────────────────┐
│ Properties              │
├─────────────────────────┤
│ Text Element            │
│                         │
│ Content:                │
│ ┌─────────────────────┐ │
│ │Hello World          │ │
│ └─────────────────────┘ │
│                         │
│ Font:                   │
│ ┌─────────────────────┐ │
│ │ Helvetica         ▼ │ │
│ └─────────────────────┘ │
│ Size: [24]              │
│                         │
│ Style:                  │
│ [B] [I] [U] [S]        │
│                         │
│ Color:  [██████]        │
│                         │
│ Alignment:              │
│ [≡] [≡] [≡] [≡]        │
│                         │
│ Position:               │
│ X: [100]  Y: [200]     │
│ W: [auto] H: [auto]    │
│                         │
│ ─────────────────────── │
│ [Apply to All Pages ▼]  │
└─────────────────────────┘
```

### 3.3 Layers Panel

```
┌─────────────────────────┐
│ Layers                  │
├─────────────────────────┤
│ 👁 🔒 Layer 3 (Top)    │
│ 👁 🔓 Layer 2          │
│ 👁 🔓 Layer 1          │
│ 👁 🔓 Background       │
│                         │
│ [+ Add Layer] [🗑]     │
└─────────────────────────┘
```

---

## 4. Architecture

### 4.1 Module Structure

```
pdfmaster/
├── src/
│   ├── design/
│   │   ├── __init__.py
│   │   ├── elements/
│   │   │   ├── base.py          # Base element class
│   │   │   ├── text.py          # Text element
│   │   │   ├── image.py         # Image element
│   │   │   ├── shape.py         # Shape elements
│   │   │   ├── table.py         # Table element
│   │   │   ├── list.py          # List element
│   │   │   └── annotation.py    # Annotation element
│   │   │
│   │   ├── decorators/
│   │   │   ├── watermark.py     # Watermark decorator
│   │   │   ├── stamp.py         # Stamp decorator
│   │   │   ├── header.py        # Header decorator
│   │   │   ├── footer.py        # Footer decorator
│   │   │   └── page_number.py   # Page number decorator
│   │   │
│   │   ├── structure/
│   │   │   ├── toc.py           # Table of contents
│   │   │   ├── bookmark.py      # Bookmarks
│   │   │   └── outline.py       # Document outline
│   │   │
│   │   ├── styling/
│   │   │   ├── text_style.py    # Text styling
│   │   │   ├── color.py         # Color utilities
│   │   │   └── gradient.py      # Gradient fills
│   │   │
│   │   └── templates/
│   │       ├── base.py          # Template base class
│   │       ├── builtin/         # Built-in templates
│   │       └── custom/          # User templates
│   │
│   └── core/
│       └── editor.py            # Enhanced editor
│
└── ui/
    └── windows/
        ├── design_window.py     # Design studio
        ├── watermark_dialog.py  # Watermark settings
        ├── stamp_dialog.py      # Stamp selection
        ├── annotation_dialog.py # Annotation tools
        └── style_dialog.py      # Style editor
```

### 4.2 Base Element Class

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Tuple
import fitz

@dataclass
class DesignElement(ABC):
    """Base class for all design elements"""
    
    # Identity
    id: str
    name: str
    type: str
    
    # Position
    x: float = 0
    y: float = 0
    width: float = 100
    height: float = 50
    
    # Appearance
    rotation: float = 0
    opacity: float = 1.0
    
    # Layer
    layer: int = 0
    locked: bool = False
    visible: bool = True
    
    @abstractmethod
    def render(self, page: fitz.Page) -> None:
        """Render element to PDF page"""
        pass
    
    @abstractmethod
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """Get element bounding box"""
        pass
    
    def contains_point(self, x: float, y: float) -> bool:
        """Check if point is within element"""
        x1, y1, x2, y2 = self.get_bounds()
        return x1 <= x <= x2 and y1 <= y <= y2
```

### 4.3 Document Designer Class

```python
class DocumentDesigner:
    """Main class for designing PDF documents"""
    
    def __init__(self, document_path: Optional[str] = None):
        self.document: Optional[fitz.Document] = None
        self.elements: Dict[str, DesignElement] = {}
        self.layers: List[str] = []
        self.history: List[HistoryEntry] = []
        self.history_index: int = -1
        
        if document_path:
            self.load(document_path)
    
    def load(self, path: str) -> None:
        """Load existing PDF"""
        self.document = fitz.open(path)
    
    def create(self, pagesize: str = "A4") -> None:
        """Create new document"""
        self.document = fitz.open()
        self.document.new_page(width=595, height=842)  # A4
    
    def save(self, path: str) -> None:
        """Save document"""
        self._apply_decorators()
        self.document.save(path)
    
    def add_element(self, element: DesignElement) -> None:
        """Add design element"""
        self.elements[element.id] = element
        self._record_history("add", element)
    
    def remove_element(self, element_id: str) -> None:
        """Remove design element"""
        if element_id in self.elements:
            del self.elements[element_id]
            self._record_history("remove", element_id)
    
    def apply_watermark(self, config: WatermarkConfig) -> None:
        """Apply watermark to document"""
        pass
    
    def apply_stamp(self, config: StampConfig, page: int = 0) -> None:
        """Apply stamp to page"""
        pass
    
    def generate_toc(self, config: TOCConfig) -> None:
        """Generate table of contents"""
        pass
    
    def add_page_numbers(self, config: PageNumberConfig) -> None:
        """Add page numbers"""
        pass
    
    def add_header_footer(self, config: HeaderFooterConfig) -> None:
        """Add headers and footers"""
        pass
```

---

## 5. Implementation Phases

### Phase 1: Core Design Elements (Weeks 1-3)

| Task | Duration | Priority |
|------|----------|----------|
| Base element classes | 3 days | P1 |
| Text element | 2 days | P1 |
| Image element | 2 days | P1 |
| Shape elements | 3 days | P1 |
| Element selection/transformation | 2 days | P1 |

### Phase 2: Page Decorators (Weeks 4-5)

| Task | Duration | Priority |
|------|----------|----------|
| Watermark system | 3 days | P1 |
| Stamp system | 2 days | P1 |
| Page numbers | 2 days | P1 |
| Headers & footers | 3 days | P1 |

### Phase 3: Document Structure (Weeks 6-7)

| Task | Duration | Priority |
|------|----------|----------|
| Table of contents | 3 days | P1 |
| Bookmarks | 2 days | P1 |
| TOC auto-generation | 2 days | P2 |

### Phase 4: Annotations (Week 8)

| Task | Duration | Priority |
|------|----------|----------|
| Sticky notes | 1 day | P2 |
| Highlight/underline | 2 days | P2 |
| Drawing annotations | 2 days | P2 |

### Phase 5: Advanced Elements (Weeks 9-10)

| Task | Duration | Priority |
|------|----------|----------|
| Table element | 3 days | P2 |
| List element | 2 days | P2 |
| Rich text styling | 3 days | P2 |

### Phase 6: Template System (Weeks 11-12)

| Task | Duration | Priority |
|------|----------|----------|
| Built-in templates | 4 days | P2 |
| Custom templates | 3 days | P2 |
| Brand kit support | 3 days | P3 |

### Phase 7: Design Studio UI (Weeks 13-16)

| Task | Duration | Priority |
|------|----------|----------|
| Canvas/editor | 1 week | P1 |
| Properties panel | 3 days | P1 |
| Toolbar | 2 days | P1 |
| Layers panel | 2 days | P2 |
| Preview mode | 2 days | P2 |

---

## 6. Dependencies

### Python Libraries
| Library | Purpose | Status |
|---------|---------|--------|
| PyMuPDF | PDF manipulation | ✅ Already in project |
| Pillow | Image processing | ✅ Already in project |
| ReportLab | PDF generation | ✅ Already in project |
| fonttools | Font handling | 📦 New |

### PyQt6 Components
| Component | Usage |
|-----------|-------|
| QGraphicsView/Scene | Canvas for visual editing |
| QDockWidget | Properties/layers panels |
| QToolBar | Tool buttons |
| QUndoStack | Undo/redo system |

---

## 7. Testing Strategy

### Unit Tests
```python
tests/
└── unit/
    └── design/
        ├── test_watermark.py
        ├── test_stamp.py
        ├── test_annotations.py
        ├── test_toc.py
        ├── test_page_numbers.py
        ├── test_header_footer.py
        └── test_elements/
            ├── test_text.py
            ├── test_image.py
            └── test_shape.py
```

### Integration Tests
```python
tests/
└── integration/
    └── design/
        ├── test_template_application.py
        ├── test_brand_kit.py
        └── test_document_design.py
```

---

## 8. Success Metrics

| Metric | Target |
|--------|--------|
| Watermark application time | < 2 seconds |
| TOC generation time | < 5 seconds (100 pages) |
| Design element render time | < 16ms (60fps) |
| Memory usage (100 elements) | < 200MB |
| Undo/redo depth | 50 operations |

---

## 9. User Stories

### US-1: Apply Watermark
**As a** user, **I want to** add a watermark to my PDF, **so that** I can mark documents as confidential or draft.

**Acceptance Criteria:**
- Can add text or image watermark
- Can adjust opacity and position
- Can apply to all or specific pages
- Can preview before applying

### US-2: Add Page Numbers
**As a** user, **I want to** add page numbers to my PDF, **so that** readers can easily reference pages.

**Acceptance Criteria:**
- Multiple formats (numeric, roman, alpha)
- Multiple positions
- Custom prefix/suffix
- First page exclusion option

### US-3: Create Table of Contents
**As a** user, **I want to** generate a TOC from my document headings, **so that** readers can navigate easily.

**Acceptance Criteria:**
- Auto-generate from headings
- Nested structure support
- Click to navigate
- Update when document changes

### US-4: Add Annotations
**As a** user, **I want to** add notes and highlights to PDFs, **so that** I can provide feedback and mark important content.

**Acceptance Criteria:**
- Multiple annotation types
- Custom colors
- Author attribution
- Export annotations

---

## 10. Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Large file performance | High | Medium | Lazy loading, caching |
| Font compatibility | Medium | Medium | Embed fonts, fallbacks |
| Complex layouts | Medium | Low | Progressive enhancement |
| Memory usage | High | Low | Object pooling, cleanup |

---

**Document Version**: 1.0  
**Status**: Planning Phase  
**Next Step**: Create feature specification and begin Phase 1
