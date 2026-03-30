"""
PDF Master Premium Main Window
Based on Editorial Workspace design specification
"""

import sys
from pathlib import Path
from PyQt6.QtCore import Qt, QSettings, QSize
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QFrame,
    QScrollArea,
    QSplitter,
    QMessageBox,
    QStatusBar,
    QMenuBar,
    QMenu,
    QFileDialog,
    QDialog,
    QDialogButtonBox,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QAction, QIcon, QFont, QPixmap


class PremiumHeader(QFrame):
    """Premium header component with search and actions"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("headerContainer")
        self.setFixedHeight(64)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(24)

        # Search input
        search_container = QHBoxLayout()
        search_container.setSpacing(8)

        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("font-size: 16px; color: #414751;")
        search_container.addWidget(search_icon)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("Search documents, annotations, or tags...")
        self.search_input.setFixedWidth(320)
        search_container.addWidget(self.search_input)

        layout.addLayout(search_container)

        # Navigation links
        nav_links = QHBoxLayout()
        nav_links.setSpacing(24)

        for text in ["Tools", "Export", "Share"]:
            link = QLabel(text)
            link.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    font-weight: 500;
                    color: #414751;
                    padding: 4px 0;
                }
                QLabel:hover {
                    color: #004f8f;
                }
            """)
            link.setCursor(Qt.CursorShape.PointingHandCursor)
            nav_links.addWidget(link)

        layout.addLayout(nav_links)

        layout.addStretch()

        # Right actions
        actions = QHBoxLayout()
        actions.setSpacing(12)

        download_btn = QLabel("⬇️")
        download_btn.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #414751;
                padding: 8px;
                border-radius: 8px;
            }
            QLabel:hover {
                background-color: #eaeef6;
            }
        """)
        download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        actions.addWidget(download_btn)

        more_btn = QLabel("⋮")
        more_btn.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #414751;
                padding: 8px;
                border-radius: 8px;
            }
            QLabel:hover {
                background-color: #eaeef6;
            }
        """)
        more_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        actions.addWidget(more_btn)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.VLine)
        divider.setFixedWidth(1)
        divider.setStyleSheet("background-color: #e2e8f0;")
        actions.addWidget(divider)

        preview_btn = QLabel("Preview")
        preview_btn.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #004f8f;
                padding: 8px 16px;
            }
            QLabel:hover {
                background-color: #eaeef6;
                border-radius: 8px;
            }
        """)
        preview_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        actions.addWidget(preview_btn)

        save_btn = QPushButton("Save Changes")
        save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #004f8f, stop:1 #0067b8);
                color: white;
                border: none;
                padding: 10px 24px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0067b8, stop:1 #004f8f);
            }
        """)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        actions.addWidget(save_btn)

        # User avatar
        avatar = QLabel("👤")
        avatar.setFixedSize(36, 36)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("""
            QLabel {
                background-color: #004f8f;
                border-radius: 18px;
                font-size: 16px;
            }
        """)
        avatar.setCursor(Qt.CursorShape.PointingHandCursor)
        actions.addWidget(avatar)

        layout.addLayout(actions)


class PremiumMainWindow(QMainWindow):
    """Premium main window based on Editorial Workspace design"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Master - Editorial Workspace")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

        self.settings = QSettings("PDFMaster", "PDFMaster")
        self.current_theme = self.settings.value("theme", "light")

        self.setup_ui()
        self.setup_menu()
        self.apply_theme()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Premium Sidebar
        from pdfmaster.ui.widgets.premium_sidebar import PremiumSidebar

        self.sidebar = PremiumSidebar()
        self.sidebar.page_changed.connect(self.on_page_changed)
        main_layout.addWidget(self.sidebar)

        # Content area
        content_area = QWidget()
        content_area.setObjectName("contentContainer")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Header
        self.header = PremiumHeader()
        content_layout.addWidget(self.header)

        # Pages stack
        self.pages = QStackedWidget()
        self.pages.setObjectName("pagesStack")

        # Import premium pages
        from pdfmaster.ui.pages.workspace_overview import WorkspaceOverview
        from pdfmaster.ui.pages.document_library import DocumentLibrary
        from pdfmaster.ui.pages.utility_library import UtilityLibrary
        from pdfmaster.ui.pages.pdf_editor import PDFEditor

        # Create pages
        self.workspace_page = WorkspaceOverview()
        self.library_page = DocumentLibrary()
        self.utility_page = UtilityLibrary()
        self.editor_page = PDFEditor()

        # Add legacy pages for compatibility
        from pdfmaster.ui.windows.create_window import CreateWindow
        from pdfmaster.ui.windows.convert_window import ConvertWindow
        from pdfmaster.ui.windows.merge_window import MergeWindow
        from pdfmaster.ui.windows.design_window import DesignWindow
        from pdfmaster.ui.windows.extract_window import ExtractWindow
        from pdfmaster.ui.windows.extract_schema_window import ExtractSchemaWindow

        self.create_window = CreateWindow()
        self.convert_window = ConvertWindow()
        self.merge_window = MergeWindow()
        self.design_window = DesignWindow()
        self.extract_window = ExtractWindow()
        self.extract_schema_window = ExtractSchemaWindow()

        # Add all pages to stack
        self.pages.addWidget(self.workspace_page)  # 0 - Workspace Overview
        self.pages.addWidget(self.library_page)  # 1 - Document Library
        self.pages.addWidget(self.library_page)  # 2 - Starred (reuse library)
        self.pages.addWidget(self.library_page)  # 3 - Annotated (reuse library)
        self.pages.addWidget(self.library_page)  # 4 - Archive (reuse library)
        self.pages.addWidget(self.utility_page)  # 5 - Utility Library
        self.pages.addWidget(self.editor_page)  # 6 - PDF Editor
        self.pages.addWidget(self.create_window)  # 7
        self.pages.addWidget(self.convert_window)  # 8
        self.pages.addWidget(self.merge_window)  # 9
        self.pages.addWidget(self.design_window)  # 10
        self.pages.addWidget(self.extract_window)  # 11
        self.pages.addWidget(self.extract_schema_window)  # 12

        content_layout.addWidget(self.pages, 1)

        main_layout.addWidget(content_area, 1)

        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.setObjectName("statusBar")
        self.status_bar.showMessage("Ready • PDF Master v3.0.0 - Premium Editorial Workspace")
        self.setStatusBar(self.status_bar)

        # Show workspace page by default
        self.pages.setCurrentIndex(0)

    def setup_menu(self):
        menubar = self.menuBar()
        menubar.setObjectName("menuBar")

        # File menu
        file_menu = menubar.addMenu("File")

        new_action = QAction("New Document", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(lambda: self.sidebar.page_changed.emit("workspace"))
        file_menu.addAction(new_action)

        open_action = QAction("Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        upload_action = QAction("Upload PDF", self)
        upload_action.triggered.connect(self.upload_pdf)
        file_menu.addAction(upload_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("View")

        workspace_action = QAction("Workspace Overview", self)
        workspace_action.triggered.connect(lambda: self.on_page_changed("library"))
        view_menu.addAction(workspace_action)

        library_action = QAction("Document Library", self)
        library_action.triggered.connect(lambda: self.on_page_changed("library"))
        view_menu.addAction(library_action)

        view_menu.addSeparator()

        theme_action = QAction("Toggle Dark Mode", self)
        theme_action.setShortcut("Ctrl+D")
        theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(theme_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About PDF Master", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def on_page_changed(self, page_id):
        """Handle navigation from sidebar"""
        page_map = {
            "library": 1,
            "recent": 1,
            "starred": 2,
            "annotated": 3,
            "archive": 4,
            "settings": 0,
            "support": 0,
            "upload": 0,
            "annual_reports": 1,
            "research_papers": 1,
        }

        index = page_map.get(page_id, 0)
        self.pages.setCurrentIndex(index)
        self.status_bar.showMessage(f"PDF Master • {page_id.replace('_', ' ').title()}")

    def toggle_theme(self):
        """Toggle between light and dark theme"""
        if self.current_theme == "light":
            self.current_theme = "dark"
        else:
            self.current_theme = "light"
        self.settings.setValue("theme", self.current_theme)
        self.apply_theme()

    def apply_theme(self):
        """Apply the premium theme"""
        from pdfmaster.ui.styles.premium_theme import apply_premium_theme

        app = QApplication.instance()
        if app:
            apply_premium_theme(app, self.current_theme)

    def open_file(self):
        """Open a PDF file"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if file_path:
            self.status_bar.showMessage(f"Opened: {file_path}")
            # Navigate to editor
            self.pages.setCurrentIndex(6)

    def upload_pdf(self):
        """Upload a new PDF"""
        self.upload_pdf_file()

    def upload_pdf_file(self):
        """Handle PDF file upload"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload PDF", "", "PDF Files (*.pdf)")
        if file_path:
            self.status_bar.showMessage(f"Uploaded: {file_path}")

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About PDF Master",
            "PDF Master v3.0.0 - Premium Editorial Workspace\n\n"
            "A premium PDF management application with editorial-grade\n"
            "tools for creating, editing, and managing digital documents.\n\n"
            "Features:\n"
            "• Premium Notion-like UI design\n"
            "• Dark/Light theme support\n"
            "• Document library management\n"
            "• PDF editing and annotation\n"
            "• Advanced conversion tools\n"
            "• Security and encryption\n\n"
            "© 2026 PDF Master Team",
        )


def main():
    """Main entry point for premium application"""
    app = QApplication(sys.argv)
    app.setApplicationName("PDF Master")
    app.setApplicationVersion("3.0.0")
    app.setOrganizationName("PDFMaster")

    window = PremiumMainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
