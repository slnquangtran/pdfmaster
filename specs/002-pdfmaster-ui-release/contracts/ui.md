# PDF Master - UI Interface Contracts

## Main Window

**Purpose**: Central navigation hub for all PDF operations

### Components

- Menu bar with File, Edit, View, Help
- Navigation sidebar with operation categories
- Content area for active operation
- Status bar showing current operation status

### Window Properties

- Default size: 1000x700 pixels
- Minimum size: 800x600 pixels
- Resizable: Yes
- Native window frame with standard controls

---

## Create PDF Window

**Purpose**: Create new PDF documents

### Input Fields

- Title input (text field, optional)
- Author input (text field, optional)
- Page size dropdown (A4, Letter, Legal)
- Content text area (multiline)
- Add Image button with file browser

### Actions

- Preview button (opens PDF preview)
- Save button (shows save dialog)
- Clear button (resets form)

### Output

- PDF file saved to user-selected location

---

## Convert File Window

**Purpose**: Convert various formats to PDF

### Input

- Drag-and-drop zone (accepts files)
- OR file browser button
- Multiple file selection support

### Controls

- Output format selector (PDF only)
- Output directory selector

### Actions

- Convert button (starts conversion)
- Progress bar during conversion
- Results list showing success/failure

### Output

- PDF files in selected output directory

---

## Extract Window

**Purpose**: Extract text or SQL schema from PDFs

### Input

- File drop zone for PDF input
- File browser button
- Operation type selector (Text / SQL Schema)

### For SQL Schema

- Table name input (optional)
- Preview of detected tables

### Actions

- Extract button
- Export button (save result)

### Output

- TXT file or SQL file

---

## Preview Window

**Purpose**: Preview PDF before saving/exporting

### Features

- PDF renderer (embedded viewer)
- Page navigation (previous/next, page number)
- Zoom controls (fit page, zoom in/out)
- Scroll for multi-page documents

### Window Properties

- Modal or non-modal (based on context)
- Default size: 800x900 pixels

---

## Error Display

### Types

- Modal error dialog (critical errors)
- Inline error message (validation errors)
- Status bar message (warnings)

### Format

- Error icon
- Error title (bold)
- Error description
- Optional "Details" expandable section