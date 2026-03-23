# Data Model: PDF Master Suite

## Entities

### 1. PDF Document

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| file_path | string | Path to PDF file |
| page_count | integer | Number of pages |
| metadata | dict | Title, author, creation date |
| created_at | timestamp | Creation timestamp |
| modified_at | timestamp | Last modification timestamp |

**Relationships**: Can contain multiple pages, images, text elements

---

### 2. PDF Page

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| document_id | UUID | Parent document reference |
| page_number | integer | Page sequence (1-based) |
| width | float | Page width in points |
| height | float | Page height in points |
| elements | list | Text, images, shapes on page |

---

### 3. Template

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| name | string | Template name |
| description | string | Template description |
| layout | dict | Page layout configuration |
| placeholders | list | Defined placeholder fields |
| created_at | timestamp | Creation timestamp |

---

### 4. Conversion Job

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| input_path | string | Source file path |
| output_path | string | Destination file path |
| input_format | string | Source format (docx, xlsx, txt, etc.) |
| output_format | string | Target format (pdf) |
| status | enum | pending, processing, completed, failed |
| error_message | string | Error details if failed |
| created_at | timestamp | Job creation time |
| completed_at | timestamp | Job completion time |

**State Transitions**: pending → processing → completed | failed

---

### 5. Extracted Table

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| source_pdf | string | Source PDF path |
| page_number | integer | Page where table found |
| headers | list | Column headers |
| rows | list | Data rows |
| confidence | float | Extraction confidence (0-1) |

---

### 6. SQL Schema

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| name | string | Table name |
| columns | list | Column definitions (name, type, constraints) |
| primary_key | list | Primary key columns |
| foreign_keys | list | Foreign key relationships |
| source_table_id | UUID | Reference to Extracted Table |

---

## Validation Rules

- PDF Document: file_path must exist and be valid PDF
- Conversion Job: input_format must be in supported formats list
- Extracted Table: confidence must be between 0 and 1
- SQL Schema: column names must be valid SQL identifiers

---

## Module Boundaries

| Module | Entities Managed |
|--------|------------------|
| core | PDF Document, PDF Page |
| templates | Template |
| converters | Conversion Job |
| extractors | Extracted Table |
| designers | SQL Schema |