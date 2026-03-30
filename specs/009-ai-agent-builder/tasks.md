# Tasks: AI Agent Builder Framework

**Input**: Design documents from `/specs/009-ai-agent-builder/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Single project structure: `pdfmaster/src/`, `pdfmaster/tests/` at repository root
- UI components: `pdfmaster/ui/components/`
- Templates: `pdfmaster/templates/agents/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize Python package with required dependencies (PyQt6, PyYAML, jsonschema)
- [ ] T003 [P] Configure linting (ruff) and formatting (black) tools
- [ ] T004 [P] Setup test framework (pytest) configuration in pytest.ini
- [ ] T005 Create directory structure: `pdfmaster/src/agents/`, `pdfmaster/src/tools/`, `pdfmaster/src/storage/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 Create `BaseTool` abstract class in `pdfmaster/src/tools/base.py` with execute(), parameters(), validate() methods
- [ ] T007 Create `ParamDef` dataclass in `pdfmaster/src/tools/base.py` for tool parameter definitions
- [ ] T008 Create `ToolResult` dataclass in `pdfmaster/src/tools/base.py` for tool execution results
- [ ] T009 Setup SQLite schema in `pdfmaster/src/storage/schema.sql` with tables: agent_templates, tools, sessions, favorites
- [ ] T010 [P] Create `ToolRegistry` class in `pdfmaster/src/agents/registry.py` for tool registration and lookup
- [ ] T011 [P] Create JSON Schema for template validation in `pdfmaster/schemas/agent_template.json`
- [ ] T012 [P] Create base theme tokens in `pdfmaster/ui/styles/agent_tokens.py`
- [ ] T013 [P] Create YAML export/import utilities in `pdfmaster/src/storage/yaml_utils.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Agent Template Creation (Priority: P1) MVP

**Goal**: Enable users to create, edit, and save agent templates with instructions, tools, and behavior rules

**Independent Test**: Create a new agent template with defined persona, rules, and tool access; verify it saves and loads correctly

### Implementation for User Story 1

- [ ] T014 [P] [US1] Create `InstructionBlock` dataclass in `pdfmaster/src/agents/template.py`
- [ ] T015 [P] [US1] Create `BehaviorRule` dataclass in `pdfmaster/src/agents/template.py`
- [ ] T016 [P] [US1] Create `ResponseFormat` dataclass in `pdfmaster/src/agents/template.py`
- [ ] T017 [P] [US1] Create `VariableDef` dataclass in `pdfmaster/src/agents/template.py`
- [ ] T018 [US1] Create `AgentTemplate` class in `pdfmaster/src/agents/template.py` (depends on T014-T017)
- [ ] T019 [US1] Create `TemplateValidator` class in `pdfmaster/src/agents/validator.py` with multi-stage validation
- [ ] T020 [US1] Create `AgentManager` class in `pdfmaster/src/agents/manager.py` for CRUD operations (depends on T018, T019)
- [ ] T021 [US1] Create `AgentStore` class in `pdfmaster/src/storage/agent_store.py` for SQLite persistence
- [ ] T022 [P] [US1] Create instruction editor widget in `pdfmaster/ui/components/agent_editor/instruction_editor.py`
- [ ] T023 [P] [US1] Create tool selector widget in `pdfmaster/ui/components/agent_editor/tool_selector.py`
- [ ] T024 [P] [US1] Create behavior rules widget in `pdfmaster/ui/components/agent_editor/behavior_rules.py`
- [ ] T025 [US1] Create main template editor in `pdfmaster/ui/components/agent_editor/template_editor.py` (depends on T022-T024)
- [ ] T026 [US1] Create template save/load functions in AgentManager
- [ ] T027 [US1] Add YAML serialization to AgentTemplate
- [ ] T028 [US1] Create template editor page in `pdfmaster/ui/pages/agent_builder_page.py`

**Checkpoint**: User Story 1 should be fully functional - users can create and save agent templates

---

## Phase 4: User Story 2 - Agent Configuration System (Priority: P1)

**Goal**: Enable users to configure agent behavior with tool access control, response formatting, and safety rules

**Independent Test**: Create an agent with specific tools enabled, run a test task, verify only configured tools are accessible

### Implementation for User Story 2

- [ ] T029 [P] [US2] Create `ToolAccessControl` class in `pdfmaster/src/agents/registry.py` for permission checking
- [ ] T030 [US2] Implement tool execution with permission validation in `pdfmaster/src/agents/executor.py`
- [ ] T031 [US2] Create response format validation (JSON, text, markdown) in `pdfmaster/src/agents/template.py`
- [ ] T032 [US2] Implement behavior rule evaluation engine in `pdfmaster/src/agents/validator.py`
- [ ] T033 [US2] Create variable substitution processor in `pdfmaster/src/agents/template.py`
- [ ] T034 [US2] Add tool call logging to executor
- [ ] T035 [US2] Create tool access configuration UI in template editor
- [ ] T036 [US2] Implement safety rule validation and warnings
- [ ] T037 [US2] Add response format selection UI (JSON schema editor)
- [ ] T038 [US2] Create template validation feedback panel

**Checkpoint**: User Story 2 complete - agents can be configured with specific tool access and validated behavior

---

## Phase 5: User Story 3 - Agent Library Management (Priority: P2)

**Goal**: Enable users to organize, browse, search, and manage their agent template collection

**Independent Test**: Create 10+ agents, categorize them, search for specific agents, mark favorites, export one template

### Implementation for User Story 3

- [ ] T039 [P] [US3] Add search functionality to AgentStore with fuzzy matching in `pdfmaster/src/storage/agent_store.py`
- [ ] T040 [P] [US3] Add category and tag support to AgentStore
- [ ] T041 [P] [US3] Add favorites management to AgentStore
- [ ] T042 [US3] Create `LibraryView` widget in `pdfmaster/ui/components/agent_library/library_view.py`
- [ ] T043 [P] [US3] Create `AgentCard` widget in `pdfmaster/ui/components/agent_library/agent_card.py`
- [ ] T044 [P] [US3] Create `SearchBar` widget in `pdfmaster/ui/components/agent_library/search_bar.py`
- [ ] T045 [US3] Create agent library page in `pdfmaster/ui/pages/agent_library_page.py`
- [ ] T046 [US3] Implement export to YAML functionality in AgentManager
- [ ] T047 [US3] Implement import from YAML functionality in AgentManager
- [ ] T048 [US3] Add template validation on import
- [ ] T049 [US3] Implement template duplicate functionality
- [ ] T050 [US3] Implement template delete with confirmation

**Checkpoint**: User Story 3 complete - users can organize, search, and share agent templates

---

## Phase 6: User Story 4 - Agent Testing Playground (Priority: P2)

**Goal**: Enable users to test agents in an interactive playground with conversation history and debug information

**Independent Test**: Select an agent, send test messages, view responses with tool calls logged, enable debug mode

### Implementation for User Story 4

- [ ] T051 [P] [US4] Create `AgentSession` dataclass in `pdfmaster/src/agents/template.py`
- [ ] T052 [P] [US4] Create `Message` dataclass in `pdfmaster/src/agents/template.py`
- [ ] T053 [P] [US4] Create `ToolCall` dataclass in `pdfmaster/src/agents/template.py`
- [ ] T054 [US4] Create `SessionStore` class in `pdfmaster/src/storage/session_store.py` for session persistence
- [ ] T055 [US4] Create `ChatInterface` widget in `pdfmaster/ui/components/playground/chat_interface.py`
- [ ] T056 [P] [US4] Create `ToolCallDisplay` widget in `pdfmaster/ui/components/playground/tool_call_display.py`
- [ ] T057 [P] [US4] Create `DebugPanel` widget in `pdfmaster/ui/components/playground/debug_panel.py`
- [ ] T058 [US4] Create playground page in `pdfmaster/ui/pages/playground_page.py`
- [ ] T059 [US4] Implement message history display with timestamps
- [ ] T060 [US4] Implement tool call visualization (input/output)
- [ ] T061 [US4] Implement debug mode toggle with verbose logging
- [ ] T062 [US4] Implement session save/load functionality
- [ ] T063 [US4] Add copy response to clipboard feature

**Checkpoint**: User Story 4 complete - users can test agents interactively with full debug capabilities

---

## Phase 7: User Story 5 - Pre-built Agent Templates (Priority: P2)

**Goal**: Provide 5 pre-built agent templates for common PDF Master tasks that work out-of-the-box

**Independent Test**: Load Document Summarizer template, test with a sample PDF, verify it summarizes correctly

### Implementation for User Story 5

- [ ] T064 [P] [US5] Create Document Summarizer template in `pdfmaster/templates/agents/document_summarizer.yaml`
- [ ] T065 [P] [US5] Create Form Extractor template in `pdfmaster/templates/agents/form_extractor.yaml`
- [ ] T066 [P] [US5] Create Report Generator template in `pdfmaster/templates/agents/report_generator.yaml`
- [ ] T065 [P] [US5] Create Design Assistant template in `pdfmaster/templates/agents/design_assistant.yaml`
- [ ] T066 [P] [US5] Create Data Analyzer template in `pdfmaster/templates/agents/data_analyzer.yaml`
- [ ] T067 [US5] Create template loader that loads pre-built templates on first run
- [ ] T068 [US5] Add "Use Template" button to library view
- [ ] T069 [US5] Create template description tooltip with usage instructions
- [ ] T070 [US5] Mark pre-built templates with special category "pre-built"

**Checkpoint**: User Story 5 complete - users have ready-to-use templates for common tasks

---

## Phase 8: User Story 6 - Agent Chaining (Priority: P3)

**Goal**: Enable users to chain multiple agents together for complex document processing pipelines

**Independent Test**: Create a 2-agent chain (Extractor → Formatter), run with test data, verify output flows correctly

### Implementation for User Story 6

- [ ] T071 [P] [US6] Create `AgentChain` dataclass in `pdfmaster/src/agents/chain.py`
- [ ] T072 [P] [US6] Create `ChainStep` dataclass in `pdfmaster/src/agents/chain.py`
- [ ] T073 [US6] Create `ChainExecutor` class in `pdfmaster/src/agents/chain.py` for pipeline execution
- [ ] T074 [US6] Implement data transformation between chain steps
- [ ] T075 [US6] Implement error handling and rollback for chain failures
- [ ] T076 [US6] Create chain builder page in `pdfmaster/ui/pages/chain_builder_page.py`
- [ ] T077 [US6] Create chain step configuration UI
- [ ] T078 [US6] Create chain execution progress display
- [ ] T079 [US6] Add chain save/load functionality
- [ ] T080 [US6] Add chain template for reuse

**Checkpoint**: User Story 6 complete - users can create multi-agent pipelines

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T081 [P] Add keyboard shortcuts throughout agent builder
- [ ] T082 [P] Add tooltips and help text to all UI components
- [ ] T083 Performance optimization for large template libraries (>100 templates)
- [ ] T084 Add undo/redo functionality to template editor
- [ ] T085 Create quickstart documentation page
- [ ] T086 Add agent performance metrics display (response time, tool usage)
- [ ] T087 Add template versioning with rollback capability
- [ ] T088 [P] Write unit tests for AgentTemplate validation
- [ ] T089 [P] Write unit tests for ToolRegistry
- [ ] T090 [P] Write unit tests for storage layer

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-8)**: All depend on Foundational phase completion
  - US1 (P1): Template Creation - Core foundation
  - US2 (P1): Configuration - Depends on US1 template structures
  - US3 (P2): Library - Independent after Foundational
  - US4 (P2): Playground - Independent after Foundational
  - US5 (P2): Pre-built Templates - Depends on US1
  - US6 (P3): Chaining - Depends on US1, US2
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### Parallel Opportunities

```bash
# Setup phase - all parallel:
Task: "Configure linting tools"
Task: "Setup test framework"
Task: "Create directory structure"

# Foundational phase - all parallel:
Task: "Create BaseTool abstract class"
Task: "Create SQLite schema"
Task: "Create ToolRegistry"
Task: "Create JSON Schema for validation"

# After Foundational, US1 and US2 can run in parallel:
# User Story 1 (Template Creation)
Task: "Create InstructionBlock dataclass"
Task: "Create BehaviorRule dataclass"

# User Story 2 (Configuration)
Task: "Create ToolAccessControl"
Task: "Implement response format validation"

# US3 and US4 can run in parallel (independent):
# User Story 3 (Library)
Task: "Add search functionality to AgentStore"
Task: "Create LibraryView widget"

# User Story 4 (Playground)
Task: "Create AgentSession dataclass"
Task: "Create ChatInterface widget"

# US5 pre-built templates can all run in parallel:
Task: "Create Document Summarizer template"
Task: "Create Form Extractor template"
Task: "Create Report Generator template"
Task: "Create Design Assistant template"
Task: "Create Data Analyzer template"
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 - Template Creation
4. Complete Phase 4: User Story 2 - Configuration
5. **STOP and VALIDATE**: Test template creation and configuration independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 (Template Creation) + US2 (Configuration) → Test → Deploy (MVP!)
3. Add US3 (Library) → Test → Deploy
4. Add US4 (Playground) → Test → Deploy
5. Add US5 (Pre-built Templates) → Test → Deploy
6. Add US6 (Chaining) → Test → Deploy

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: US1 + US2 (core features)
   - Developer B: US3 + US4 (library & playground)
   - Developer C: US5 (pre-built templates)
3. US6 (chaining) after US1 + US2 complete
4. Stories complete and integrate independently

---

## Summary

| Phase | User Story | Priority | Task Count | Independent Test |
|-------|------------|----------|------------|------------------|
| 1 | Setup | - | 5 | Project structure exists |
| 2 | Foundational | - | 8 | Core classes compile |
| 3 | Template Creation | P1 | 15 | Create & save template |
| 4 | Configuration | P1 | 10 | Tool access control works |
| 5 | Library | P2 | 12 | Search & organize agents |
| 6 | Playground | P2 | 13 | Test agents interactively |
| 7 | Pre-built Templates | P2 | 7 | Templates load & work |
| 8 | Chaining | P3 | 10 | 2-agent chain executes |
| 9 | Polish | - | 10 | All improvements applied |

**Total Tasks**: 90  
**Parallel Tasks**: 28 marked [P]  
**MVP Scope**: Phases 1-4 (Setup + Foundational + US1 + US2)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Pre-built templates (US5) can be worked on in parallel with US3/US4
