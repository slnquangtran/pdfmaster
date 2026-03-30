# Quickstart: AI Agent Builder Framework

**Feature**: 009-ai-agent-builder  
**Date**: 2026-03-23

## Quick Start

### Access Agent Builder
1. Open PDF Master
2. Navigate to sidebar → **🤖 Agent Builder**
3. Or use Quick Find (`Ctrl+K`) → "Agent Builder"

### Create Your First Agent

#### Option 1: From Pre-built Template
1. Click **Library** tab
2. Browse categories or search (e.g., "summarizer")
3. Click template card → **Use This Template**
4. Customize as needed → **Save**

#### Option 2: From Scratch
1. Click **+ New Agent**
2. Fill in **Basic Info**:
   - Name: "My PDF Assistant"
   - Description: "Helps with PDF tasks"
   - Category: Select from dropdown
3. Add **Instructions**:
   - Click **+ Add Instruction Block**
   - Select type: "Persona" (required first)
   - Write your agent's persona
4. Add **Tools**:
   - Check tools the agent can use
   - Each tool requires specific permissions
5. Set **Behavior Rules** (optional):
   - Add constraints like "Never modify original files"
6. **Save** template

### Test Your Agent

1. Click **Playground** tab
2. Select your agent from dropdown
3. Type a test message
4. View responses and tool calls in real-time
5. Toggle **Debug Mode** for detailed logs
6. Save test session if needed

### Using Pre-built Templates

| Template | Use Case |
|----------|----------|
| 📄 Document Summarizer | Extract key points from PDFs |
| 📋 Form Extractor | Pull data from form fields |
| 📊 Report Generator | Create formatted reports |
| 🎨 Design Assistant | Suggest layouts and styles |
| 📈 Data Analyzer | Analyze PDF data and tables |

### Agent Chaining (Advanced)

1. Go to **Chains** tab
2. Click **+ New Chain**
3. Drag agents to create sequence:
   ```
   Extractor → Formatter → Designer
   ```
4. Configure data flow between steps
5. Test the full chain
6. Save for reuse

## Instruction Template Format

Agents follow the Claude instruction pattern:

```yaml
instructions:
  - type: persona
    content: |
      You are a professional PDF assistant specializing in document analysis.
      You are helpful, accurate, and efficient.
      
  - type: rules
    content: |
      - NEVER modify the original PDF file
      - Always preserve document formatting
      - Use provided tools for all PDF operations
      
  - type: examples
    content: |
      User: "Extract all tables from this PDF"
      Assistant: [Uses table extraction tool]
      
  - type: format
    content: |
      - Respond in JSON format with keys: summary, tables, metadata
      - Include page numbers for all extracted content
```

## Variable Placeholders

Use `{variable_name}` in instructions:

```
Hello {user_name}, I'm working on {document_name}.
```

Define variables when creating agents. Values are provided when running the agent.

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| New Agent | `Ctrl+Shift+N` |
| Save Agent | `Ctrl+S` |
| Test Agent | `Ctrl+Enter` |
| Toggle Debug | `Ctrl+D` |
| Open Library | `Ctrl+L` |

## Export/Share Agents

1. Open agent in editor
2. Click **⋮** menu → **Export**
3. Choose format: JSON or YAML
4. Save file to share with others

Import: Click **Import** in library, select file

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Agent not responding | Check tool permissions are enabled |
| Variables not working | Ensure {var_name} matches defined variables |
| Export fails | Verify template passes validation |
| Playground slow | Reduce max_tokens or simplify instructions |
