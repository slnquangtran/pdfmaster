# Implementation Plan: Notion-Style UI with AI Design Features

**Branch**: `008-notion-ui-ai-design` | **Date**: 2026-03-23 | **Spec**: specs/008-notion-ui-ai-design/spec.md
**Input**: Feature specification from `/specs/008-notion-ui-ai-design/spec.md`

## Summary

Transform PDF Master into an AI-powered document design studio with a Notion-inspired UI. The implementation includes a block-based content editor with slash commands, collapsible sidebar navigation, AI-powered design generation (Google Stitch-like), properties panel, and a comprehensive theme system with Notion-accurate colors.

## Technical Context

**Language/Version**: Python 3.10+ (project uses 3.14)
**Primary Dependencies**: PyQt6 (GUI), PyMuPDF (PDF engine), OpenAI API (AI features), rapidfuzz (search)
**Storage**: File system (documents), SQLite (workspace metadata), QSettings (user preferences)
**Testing**: pytest
**Target Platform**: Windows desktop (cross-platform via PyQt6)
**Project Type**: Desktop application
**Performance Goals**: 60fps animations, <100ms search, <10s AI generation
**Constraints**: <500MB memory, offline-capable with AI fallback, Windows 10+ minimum
**Scale/Scope**: Single user, 1000+ documents, 50+ block types, 24-week development

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

No formal constitution defined for this project. Proceeding with implementation.

## Project Structure

### Documentation (this feature)

```text
specs/008-notion-ui-ai-design/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
pdfmaster/
├── src/
│   ├── core/
│   │   ├── engine/
│   │   │   ├── pdf_reader.py
│   │   │   └── pdf_writer.py
│   │   └── ai/
│   │       ├── service.py
│   │       ├── design_generator.py
│   │       └── style_advisor.py
│   │
│   ├── workspace/
│   │   ├── document.py
│   │   ├── workspace.py
│   │   ├── templates/
│   │   └── database.py
│   │
│   └── services/
│       ├── ai_service.py
│       ├── style_service.py
│       └── search_service.py
│
├── ui/
│   ├── components/
│   │   ├── blocks/
│   │   │   ├── base_block.py
│   │   │   ├── text_block.py
│   │   │   ├── image_block.py
│   │   │   ├── heading_block.py
│   │   │   ├── pdf_block.py
│   │   │   └── ai_block.py
│   │   ├── sidebar/
│   │   │   ├── sidebar.py
│   │   │   ├── navigation.py
│   │   │   └── quick_find.py
│   │   ├── panels/
│   │   │   ├── properties_panel.py
│   │   │   └── ai_assistant_panel.py
│   │   └── shared/
│   │       ├── slash_menu.py
│   │       ├── drag_handle.py
│   │       └── tooltip.py
│   │
│   ├── pages/
│   │   ├── home_page.py
│   │   ├── workspace_page.py
│   │   ├── editor_page.py
│   │   └── design_canvas.py
│   │
│   ├── styles/
│   │   ├── theme.py
│   │   ├── tokens.py
│   │   ├── animations.py
│   │   └── notion.qss
│   │
│   └── main_window.py
│
└── tests/
    ├── unit/
    │   ├── test_blocks.py
    │   ├── test_workspace.py
    │   └── test_ai_service.py
    ├── integration/
    │   └── test_editor_workflow.py
    └── e2e/
        └── test_user_scenarios.py
```

**Structure Decision**: Selected single project structure with clear separation between core logic (src/), UI components (ui/), and tests. The UI layer follows a component-based architecture mirroring Notion's patterns. AI integration is isolated in src/core/ai/ for easy provider swapping.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Block system with 15+ types | Covers all content types users expect (text, media, PDF-specific, AI) | Fewer blocks would require workarounds and limit expressiveness |
| AI service abstraction layer | Allows switching AI providers and local fallback | Direct API calls would make testing and provider switching difficult |
| Custom widget rendering | Notion-style blocks require pixel-perfect control beyond standard Qt widgets | Standard widgets cannot achieve the drag-drop, slash menu, and block interaction patterns |

## Research Areas (Phase 0)

### R-001: Block Editor Architecture
**Status**: NEEDS CLARIFICATION
**Questions**:
- Should blocks be QWidgets or custom painted?
- How to handle block nesting (children)?
- Memory management for documents with 100+ blocks?

### R-002: AI Integration Pattern
**Status**: NEEDS CLARIFICATION
**Questions**:
- OpenAI API vs local LLM (llama.cpp)?
- How to handle offline mode?
- Caching strategy for generated designs?

### R-003: Theme Token System
**Status**: In Progress
**Findings**:
- Use Qt stylesheets (.qss) with CSS-like syntax
- Define color tokens as constants
- Use QPalette for base theme, stylesheets for overrides

## Implementation Phases

### Phase 0: Research & Foundation (Weeks 1-2)
- Research block editor architecture patterns
- Design AI service abstraction layer
- Create design token system
- Set up testing infrastructure

### Phase 1: Core UI Components (Weeks 3-8)
- Implement base block classes
- Build slash command system
- Create sidebar navigation
- Implement properties panel
- Add theme system with light/dark modes

### Phase 2: Block Types (Weeks 9-14)
- Text blocks (paragraph, headings, lists)
- Media blocks (images, files)
- PDF-specific blocks (preview, page, TOC)
- AI blocks (design prompt, suggestions)

### Phase 3: Workspace Features (Weeks 15-18)
- Document hierarchy
- Search and quick find
- Favorites and recents
- Template system

### Phase 4: AI Integration (Weeks 19-22)
- AI design generation
- Style suggestions
- Content-aware layout
- Chat assistant

### Phase 5: Polish & Release (Weeks 23-24)
- Performance optimization
- Accessibility
- Documentation
- Beta testing
