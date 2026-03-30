# Tasks: Premium UI Functional Implementation

**Input**: Design documents from `/specs/010-premium-ui-functional/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - only included where explicitly needed.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `pdfmaster/` at repository root
- Structure: `ui/`, `core/`, `pdf/`, `converters/`, `extractors/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and directory structure

- [ ] T001 Create core module structure in pdfmaster/core/
- [ ] T002 Create pdf module structure in pdfmaster/pdf/
- [ ] T003 Create converters module structure in pdfmaster/converters/
- [ ] T004 Create extractors module structure in pdfmaster/extractors/
- [ ] T005 Create dialogs structure in pdfmaster/ui/dialogs/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 Create SQLite database schema in pdfmaster/core/database.py
- [ ] T007 Implement Workspace model in pdfmaster/core/workspace.py
- [ ] T008 Implement PDFDocument model in pdfmaster/core/document.py
- [ ] T009 Implement Collection model in pdfmaster/core/collection.py
- [ ] T010 Implement Annotation model in pdfmaster/core/annotation.py
- [ ] T011 [P] Create database initialization and migration utilities in pdfmaster/core/db_init.py
- [ ] T012 [P] Implement file path validation utilities in pdfmaster/core/path_utils.py
- [ ] T013 Implement database connection manager in pdfmaster/core/db_manager.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 5 - Navigation and Search (Priority: P1) 🎯 MVP

**Goal**: Working sidebar navigation and search functionality to move between sections and find documents

**Independent Test**: Click each sidebar item, verify correct page loads. Type in search, verify results appear.

### Implementation for User Story 5

- [ ] T014 [P] [US5] Create LibraryManager in pdfmaster/core/library.py
- [ ] T015 [P] [US5] Implement document scanning in pdfmaster/core/library.py (scan method)
- [ ] T016 [P] [US5] Implement get_documents with filtering in pdfmaster/core/library.py
- [ ] T017 [P] [US5] Implement get_recent in pdfmaster/core/library.py
- [ ] T018 [P] [US5] Implement get_storage_usage in pdfmaster/core/library.py
- [ ] T019 [US5] Update premium_sidebar.py navigation signals in pdfmaster/ui/widgets/premium_sidebar.py
- [ ] T020 [US5] Implement page_changed signal handling in pdfmaster/ui/premium_main.py
- [ ] T021 [US5] Implement search functionality in pdfmaster/core/library.py (search method)
- [ ] T022 [US5] Add file upload dialog in pdfmaster/ui/dialogs/upload_dialog.py
- [ ] T023 [US5] Connect Upload PDF button to file dialog in pdfmaster/ui/widgets/premium_sidebar.py
- [ ] T024 [US5] Implement Quick Access collection filtering in pdfmaster/ui/widgets/premium_sidebar.py

**Checkpoint**: Navigation works, search works, upload works

---

## Phase 4: User Story 1 - Workspace Overview Dashboard (Priority: P1)

**Goal**: Display real storage data, recent documents, and provide quick action buttons

**Independent Test**: Launch app, verify storage shows actual file sizes, recent documents are real files, clicking items navigates correctly

### Implementation for User Story 1

- [ ] T025 [P] [US1] Connect storage display to LibraryManager in pdfmaster/ui/pages/workspace_overview.py
- [ ] T026 [P] [US1] Create DocumentItemWidget for real documents in pdfmaster/ui/widgets/document_item.py
- [ ] T027 [US1] Implement RecentDocuments list with real data in pdfmaster/ui/pages/workspace_overview.py
- [ ] T028 [US1] Connect document click to open in editor in pdfmaster/ui/pages/workspace_overview.py
- [ ] T029 [US1] Connect View All Library button in pdfmaster/ui/pages/workspace_overview.py
- [ ] T030 [US1] Implement Merge Assets button navigation in pdfmaster/ui/pages/workspace_overview.py
- [ ] T031 [US1] Implement Compress File button with file dialog in pdfmaster/ui/pages/workspace_overview.py
- [ ] T032 [P] [US1] Create CollectionItemWidget for collections in pdfmaster/ui/widgets/collection_item.py
- [ ] T033 [US1] Connect Active Collections display in pdfmaster/ui/pages/workspace_overview.py
- [ ] T034 [US1] Implement collection click filtering in pdfmaster/ui/pages/workspace_overview.py

**Checkpoint**: Workspace Overview shows real data, buttons navigate correctly

---

## Phase 5: User Story 2 - Document Library Management (Priority: P1)

**Goal**: Show all PDF files with working filtering, sorting, and document management

**Independent Test**: Navigate to Library, verify files listed, filtering works, sorting works, file actions work

### Implementation for User Story 2

- [ ] T035 [P] [US2] Implement document list rendering in pdfmaster/ui/pages/document_library.py
- [ ] T036 [P] [US2] Create DocumentRow widget with metadata in pdfmaster/ui/widgets/document_row.py
- [ ] T037 [US2] Implement filter buttons (All, PDFs, Scans, Markups) in pdfmaster/ui/pages/document_library.py
- [ ] T038 [US2] Implement sort functionality (name, date, size) in pdfmaster/ui/pages/document_library.py
- [ ] T039 [US2] Implement double-click to open document in pdfmaster/ui/pages/document_library.py
- [ ] T040 [US2] Create document actions context menu in pdfmaster/ui/dialogs/document_actions.py
- [ ] T041 [US2] Implement rename document action in pdfmaster/core/library.py
- [ ] T042 [US2] Implement delete document action in pdfmaster/core/library.py
- [ ] T043 [US2] Create collection dialog in pdfmaster/ui/dialogs/collection_dialog.py
- [ ] T044 [US2] Implement New Collection button in pdfmaster/ui/pages/document_library.py
- [ ] T045 [US2] Implement move to collection action in pdfmaster/ui/dialogs/document_actions.py
- [ ] T046 [US2] Implement View Analytics dialog in pdfmaster/ui/dialogs/analytics_dialog.py
- [ ] T047 [US2] Implement star/unstar document action in pdfmaster/core/library.py
- [ ] T048 [US2] Implement CuratedSpace card with collection data in pdfmaster/ui/pages/document_library.py

**Checkpoint**: Document Library fully functional with filtering, sorting, actions

---

## Phase 6: User Story 3 - Utility Library Tools (Priority: P2)

**Goal**: All PDF tools (merge, split, convert, compress, encrypt, sign, redact) are functional

**Independent Test**: Click each tool, perform operation, verify output file created correctly

### Implementation for User Story 3

- [ ] T049 [P] [US3] Implement PDFMerger in pdfmaster/pdf/merger.py
- [ ] T050 [P] [US3] Implement PDFSplitter in pdfmaster/pdf/splitter.py
- [ ] T051 [P] [US3] Implement PDFCompressor in pdfmaster/pdf/compressor.py
- [ ] T052 [P] [US3] Implement PDFEncryptor in pdfmaster/pdf/encryptor.py
- [ ] T053 [P] [US3] Implement PDFSigner in pdfmaster/pdf/signer.py
- [ ] T054 [P] [US3] Implement PDFRedactor in pdfmaster/pdf/redactor.py
- [ ] T055 [P] [US3] Implement DOCX/XLSX to PDF converter in pdfmaster/converters/to_pdf.py
- [ ] T056 [P] [US3] Implement PDF to HTML converter in pdfmaster/converters/to_html.py
- [ ] T057 [P] [US3] Implement image extractor in pdfmaster/extractors/images.py
- [ ] T058 [P] [US3] Implement text extractor in pdfmaster/extractors/text.py
- [ ] T059 [US3] Create tool dialog base class in pdfmaster/ui/dialogs/tool_dialogs/base_tool_dialog.py
- [ ] T060 [US3] Create merge dialog in pdfmaster/ui/dialogs/tool_dialogs/merge_dialog.py
- [ ] T061 [US3] Create split dialog in pdfmaster/ui/dialogs/tool_dialogs/split_dialog.py
- [ ] T062 [US3] Create compress dialog in pdfmaster/ui/dialogs/tool_dialogs/compress_dialog.py
- [ ] T063 [US3] Create encrypt dialog in pdfmaster/ui/dialogs/tool_dialogs/encrypt_dialog.py
- [ ] T064 [US3] Create signature dialog in pdfmaster/ui/dialogs/tool_dialogs/signature_dialog.py
- [ ] T065 [US3] Create redact dialog in pdfmaster/ui/dialogs/tool_dialogs/redact_dialog.py
- [ ] T066 [US3] Create convert dialog in pdfmaster/ui/dialogs/tool_dialogs/convert_dialog.py
- [ ] T067 [US3] Connect utility library buttons to tool dialogs in pdfmaster/ui/pages/utility_library.py
- [ ] T068 [US3] Add progress indicator for long operations in pdfmaster/ui/widgets/progress_dialog.py

**Checkpoint**: All PDF tools functional with dialogs

---

## Phase 7: User Story 4 - PDF Editor Functionality (Priority: P2)

**Goal**: PDF viewer with rendering, zoom, navigation, and annotation support

**Independent Test**: Open PDF, navigate pages, zoom, add annotations, save changes

### Implementation for User Story 4

- [ ] T069 [P] [US4] Implement PDFReader using PyMuPDF in pdfmaster/pdf/reader.py
- [ ] T070 [P] [US4] Create PDFViewer widget using QGraphicsView in pdfmaster/ui/widgets/pdf_viewer.py
- [ ] T071 [US4] Implement page rendering with pixmap in pdfmaster/ui/widgets/pdf_viewer.py
- [ ] T072 [US4] Implement zoom controls (50%-400%) in pdfmaster/ui/widgets/pdf_viewer.py
- [ ] T073 [US4] Implement page navigation (prev/next/first/last) in pdfmaster/ui/widgets/pdf_viewer.py
- [ ] T074 [US4] Implement scroll-based page navigation in pdfmaster/ui/widgets/pdf_viewer.py
- [ ] T075 [US4] Connect open document from library in pdfmaster/ui/pages/pdf_editor.py
- [ ] T076 [US4] Implement password prompt for protected PDFs in pdfmaster/ui/dialogs/password_dialog.py
- [ ] T077 [US4] Implement text annotation tool in pdfmaster/ui/widgets/pdf_viewer.py
- [ ] T078 [US4] Implement highlight annotation tool in pdfmaster/ui/widgets/pdf_viewer.py
- [ ] T079 [US4] Implement note annotation tool in pdfmaster/ui/widgets/pdf_viewer.py
- [ ] T080 [US4] Connect editing tools panel buttons in pdfmaster/ui/pages/pdf_editor.py
- [ ] T081 [US4] Implement save changes functionality in pdfmaster/pdf/writer.py
- [ ] T082 [US4] Connect Save Changes button in pdfmaster/ui/pages/pdf_editor.py
- [ ] T083 [US4] Implement export functionality (PDF, Image) in pdfmaster/ui/pages/pdf_editor.py
- [ ] T084 [US4] Display document metrics (file size, version, readability) in pdfmaster/ui/pages/pdf_editor.py
- [ ] T085 [US4] Implement recent comments display in pdfmaster/ui/pages/pdf_editor.py

**Checkpoint**: PDF Editor fully functional with viewing and basic editing

---

## Phase 8: User Story 6 - Theme Toggle (Priority: P3)

**Goal**: Toggle between light and dark themes with persistence

**Independent Test**: Press Ctrl+D to toggle, verify all pages update, restart app, verify theme persists

### Implementation for User Story 6

- [ ] T086 [P] [US6] Update premium_theme.py with complete dark theme colors in pdfmaster/ui/styles/premium_theme.py
- [ ] T087 [US6] Implement theme toggle hotkey (Ctrl+D) in pdfmaster/ui/premium_main.py
- [ ] T088 [US6] Connect theme toggle to all page widgets in pdfmaster/ui/premium_main.py
- [ ] T089 [US6] Persist theme preference in Workspace model in pdfmaster/core/workspace.py
- [ ] T090 [US6] Load theme preference on startup in pdfmaster/ui/premium_main.py
- [ ] T091 [US6] Test dark theme on all pages for visual consistency in pdfmaster/ui/pages/

**Checkpoint**: Theme toggle works across all pages with persistence

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and error handling

- [ ] T092 [P] Add error handling for file operations across all modules
- [ ] T093 [P] Add progress indicators for long PDF operations
- [ ] T094 [P] Implement empty state displays for no results/errors
- [ ] T095 [P] Add file system watcher for real-time library updates in pdfmaster/core/library.py
- [ ] T096 [P] Implement background processing with QThreadPool for PDF operations
- [ ] T097 Add comprehensive logging throughout the application
- [ ] T098 Implement keyboard shortcuts (Ctrl+O, Ctrl+S, etc.)
- [ ] T099 Add tooltips to all toolbar buttons
- [ ] T100 Run quickstart.md validation steps

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-8)**: All depend on Foundational phase completion
  - Phase 3 (US5 Navigation) should come first as it enables all other navigation
  - Phase 4 (US1 Workspace) depends on US5 for navigation
  - Phase 5 (US2 Library) depends on US5 for navigation
  - Phases 6-8 can proceed after their dependencies
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 5 (P1)**: No story dependencies - implements core navigation
- **User Story 1 (P1)**: Depends on US5 for navigation - implements dashboard
- **User Story 2 (P1)**: Depends on US5 for navigation - implements library
- **User Story 3 (P2)**: Can integrate with US1/US2 for file selection
- **User Story 4 (P2)**: Depends on US2 for document opening
- **User Story 6 (P3)**: Independent - can be done anytime

### Within Each User Story

- Models before services
- Services before UI integration
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks (T001-T005) can run in parallel
- All Foundational model tasks (T007-T010) can run in parallel
- PDF tool implementations (T049-T058) can all run in parallel
- Theme updates across pages (T086-T091) can run in parallel
- Polish tasks (T092-T100) can run in parallel

---

## Implementation Strategy

### MVP First (User Stories 5 + 1 + 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 5 (Navigation)
4. Complete Phase 4: User Story 1 (Dashboard)
5. Complete Phase 5: User Story 2 (Library)
6. **STOP and VALIDATE**: Test navigation, dashboard, library independently
7. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Navigation (US5) → Working navigation → Test
3. Dashboard (US1) → Working dashboard with real data → Test → Demo
4. Library (US2) → Working file management → Test → Demo
5. Tools (US3) → Working PDF tools → Test → Demo
6. Editor (US4) → Working PDF editor → Test → Demo
7. Theme (US6) → Polished UI → Final demo

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently

---

## Task Summary

| Phase | Tasks | Story |
|-------|-------|-------|
| Setup | T001-T005 | - |
| Foundational | T006-T013 | - |
| US5 Navigation | T014-T024 | US5 |
| US1 Dashboard | T025-T034 | US1 |
| US2 Library | T035-T048 | US2 |
| US3 Tools | T049-T068 | US3 |
| US4 Editor | T069-T085 | US4 |
| US6 Theme | T086-T091 | US6 |
| Polish | T092-T100 | - |
| **Total** | **100 tasks** | |

**MVP Scope**: T001-T048 (Setup through US2 Library)
