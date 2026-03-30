# Quickstart: Notion-Style UI with AI Design Features

**Feature**: 008-notion-ui-ai-design  
**Date**: 2026-03-23

## Quick Start

### Launch Application
```bash
python -m pdfmaster
```

### Creating a Document

1. Click **+ New** in sidebar or press `Ctrl+N`
2. Enter document title
3. Start typing or use `/` for slash commands

### Using Slash Commands

1. In any text block, type `/`
2. Command menu appears with categories:
   - **Basic**: Text, Headings, Lists
   - **PDF**: PDF Page, Preview, TOC
   - **AI**: Generate Design, Suggest Layout
3. Type to filter commands
4. Press `Enter` to select

### Navigation

| Action | Shortcut |
|--------|----------|
| Quick Find | `Ctrl+K` |
| New Document | `Ctrl+N` |
| Toggle Sidebar | `Ctrl+\` |
| Theme Toggle | `Ctrl+Shift+L` |

### AI Design Generation

1. Open AI Assistant panel (click 🤖 or `Ctrl+Shift+A`)
2. Enter design description:
   ```
   Create a professional quarterly report with:
   - Executive summary
   - Financial highlights
   - Key metrics dashboard
   ```
3. Select style preference
4. Click **Generate**
5. Review and edit generated design

### Block Operations

| Action | Method |
|--------|--------|
| Add block below | `Enter` at end of block |
| Delete block | `Backspace` on empty block |
| Move block | Drag handle (⋮⋮) |
| Duplicate | Right-click → Duplicate |
| Change type | Right-click → Turn into |

### Theme Customization

1. Press `Ctrl+Shift+L` or click theme toggle
2. Choose Light or Dark mode
3. Preference persists across sessions

## Key Features

### Block Types Available

**Text Blocks**
- Paragraph
- Heading 1, 2, 3
- Bulleted List
- Numbered List
- To-do List
- Quote
- Callout
- Code Block
- Divider

**Media Blocks**
- Image
- File Attachment
- Bookmark

**PDF Blocks**
- PDF Preview
- PDF Page Extract
- Table of Contents
- Page Numbers

**AI Blocks**
- AI Design Prompt
- AI Content Generation
- AI Layout Suggestion

### Workspace Organization

```
Workspace
├── ⭐ Favorites
│   ├── Recent Document
│   └── Pinned Project
├── 📄 Documents
│   ├── Report Q1
│   │   ├── Executive Summary
│   │   └── Financial Data
│   └── Invoice Template
├── 📁 Templates
└── 🤖 AI Designs
```

### Properties Panel

Select any element to view/edit properties:

- **Document**: Title, icon, cover, tags, status
- **Block**: Style, color, alignment, constraints
- **AI**: Prompt history, variations, apply suggestions

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Slash menu not appearing | Ensure you're in a text block, not an empty line |
| AI generation slow | Check internet connection, try simpler prompt |
| Theme not persisting | Check QSettings permissions |
| Drag-drop not working | Release mouse button over drop target |

## Next Steps

- Read full documentation in Help menu
- Explore templates for quick starts
- Try AI design with different style prompts
- Customize sidebar with your document structure
