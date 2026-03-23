# Research: PDF Master UI and Release

## Technology Decisions

### UI Framework: PyQt6

**Decision**: PyQt6

**Rationale**:
- Mature, full-featured Python GUI framework
- Cross-platform (Windows, macOS, Linux)
- Native look and feel on each platform
- Supports all required UI features (file dialogs, drag-drop, PDF viewing via QWebEngineView)
- Good documentation and community support
- PyInstaller compatible

**Alternatives considered**:
- PySimpleGUI: Too limited for complex UI
- Tkinter: Outdated look, limited features
- Electron + web: More complex, larger bundle size
- Tauri + web: Requires Rust knowledge, more complex setup

---

### Packaging: PyInstaller

**Decision**: PyInstaller

**Rationale**:
- Standard Python packaging solution
- Supports embedding Python interpreter
- Creates both one-file executable and directory-based
- Works well with PyQt6
- Large community and documentation

**Alternatives considered**:
- cx_Freeze: Less popular, fewer features
- Nuitka: Compiles to C, faster but more complex
- py2exe: Windows only
- cx_Freeze: Cross-platform but less maintained

---

### Distribution Strategy

**Decision**: Primary Windows installer (.exe NSIS) + Portable version

**Rationale**:
- NSIS creates familiar Windows installer experience
- Portable version for users who can't/won't install
- Both can be distributed via GitHub Releases
- Future: Can add Inno Setup or WiX for MSI

---

## Implementation Plan

### Phase 1: UI Development (Weeks 1-2)
- Set up PyQt6 project structure
- Implement main window with navigation
- Create PDF creation window
- Create file conversion window
- Create text/schema extraction windows

### Phase 2: Backend Integration (Week 2)
- Connect UI to existing Python modules
- Add progress indicators
- Add error handling and display

### Phase 3: PDF Preview (Week 3)
- Integrate PDF viewer (QWebEngineView + PDF.js)
- Add page navigation controls

### Phase 4: Packaging & Release (Week 3-4)
- Configure PyInstaller
- Create Windows installer (NSIS)
- Build portable version
- Test distribution packages

---

## Constitution Compliance

| Principle | Compliance | Notes |
|-----------|------------|-------|
| Library-First | ✓ Pass | Python backend modules are reusable libraries |
| CLI Interface | ✓ Pass | CLI preserved as fallback |
| Test-First | ✓ Pass | Tests required before implementation |
| Integration Testing | ✓ Pass | UI-to-backend integration tests |