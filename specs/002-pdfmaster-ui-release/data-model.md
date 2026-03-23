# Data Model: PDF Master UI and Release

## New Entities

### 1. Application State

| Field | Type | Description |
|-------|------|-------------|
| current_operation | enum | None, creating, converting, extracting |
| progress | float | 0.0 to 1.0 |
| last_output_path | Path | Path to last generated file |
| settings | dict | User preferences |

---

### 2. UI Window State

| Field | Type | Description |
|-------|------|-------------|
| window_type | enum | Main, Create, Convert, Extract |
| input_files | List[Path] | Selected input files |
| output_path | Path | Selected output path |
| options | dict | Operation-specific options |

---

### 3. Conversion Task

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique task identifier |
| input_path | Path | Source file |
| output_path | Path | Destination PDF |
| status | enum | pending, running, completed, failed |
| progress | float | Task progress |
| error_message | string | Error details if failed |

---

## Module Boundaries

| Module | Entities Managed |
|--------|------------------|
| ui/main.py | Application state, main window |
| ui/windows/* | UI window states |
| src/core | PDF operations (unchanged) |
| src/converters | File conversion (unchanged) |
| src/extractors | Text/schema extraction (unchanged) |