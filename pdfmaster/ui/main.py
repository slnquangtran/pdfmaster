import sys
from pathlib import Path
from PyQt6.QtCore import Qt, QSettings

sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QStackedWidget,
    QLabel,
    QPushButton,
    QMenuBar,
    QMenu,
    QStatusBar,
    QMessageBox,
    QToolBar,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QAction, QIcon, QColor, QPalette


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Master")
        self.setMinimumSize(1000, 700)
        self.resize(1100, 750)

        self.settings = QSettings("PDFMaster", "PDFMaster")
        self.current_theme = self.settings.value("theme", "light")

        self.setup_ui()
        self.setup_menu()
        self.apply_theme()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setObjectName("centralWidget")

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(main_layout)

        sidebar_container = QWidget()
        sidebar_container.setObjectName("sidebarContainer")
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(10)
        sidebar_container.setLayout(sidebar_layout)

        logo_label = QLabel("PDF Master")
        logo_label.setObjectName("logoLabel")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(logo_label)

        subtitle = QLabel("Premium Edition")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(subtitle)

        sidebar_layout.addSpacing(20)

        self.sidebar = QListWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.addItems(
            [
                "🎨  Create PDF",
                "🔄  Convert Files",
                "🔗  Merge/Split",
                "📝  Extract Text",
                "🗄️  Extract SQL",
            ]
        )
        self.sidebar.currentRowChanged.connect(self.change_page)
        sidebar_layout.addWidget(self.sidebar)

        sidebar_layout.addStretch()

        theme_btn = QPushButton("🌙 Dark Mode")
        theme_btn.setObjectName("themeButton")
        theme_btn.setCheckable(True)
        theme_btn.clicked.connect(self.toggle_theme)
        if self.current_theme == "dark":
            theme_btn.setText("☀️ Light Mode")
            theme_btn.setChecked(True)
        sidebar_layout.addWidget(theme_btn)

        main_layout.addWidget(sidebar_container)

        content_container = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        content_container.setLayout(content_layout)

        header = QWidget()
        header_layout = QHBoxLayout()
        header.setLayout(header_layout)

        self.page_title = QLabel("Create PDF")
        self.page_title.setObjectName("pageTitle")
        header_layout.addWidget(self.page_title)

        header_layout.addStretch()

        actions = QPushButton("⚡ Quick Actions")
        actions.setObjectName("secondaryButton")
        actions.setProperty("secondary", True)
        actions.clicked.connect(self.show_quick_actions)
        header_layout.addWidget(actions)

        content_layout.addWidget(header)

        self.pages = QStackedWidget()
        self.pages.setObjectName("contentArea")

        from pdfmaster.ui.windows.create_window import CreateWindow
        from pdfmaster.ui.windows.convert_window import ConvertWindow
        from pdfmaster.ui.windows.merge_window import MergeWindow
        from pdfmaster.ui.windows.extract_window import ExtractWindow
        from pdfmaster.ui.windows.extract_schema_window import ExtractSchemaWindow

        self.create_window = CreateWindow()
        self.convert_window = ConvertWindow()
        self.merge_window = MergeWindow()
        self.extract_window = ExtractWindow()
        self.extract_schema_window = ExtractSchemaWindow()

        self.pages.addWidget(self.create_window)
        self.pages.addWidget(self.convert_window)
        self.pages.addWidget(self.merge_window)
        self.pages.addWidget(self.extract_window)
        self.pages.addWidget(self.extract_schema_window)

        content_layout.addWidget(self.pages)

        main_layout.addWidget(content_container, 1)

        self.status_bar = QStatusBar()
        self.status_bar.setObjectName("statusBar")
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready • PDF Master v1.1.0")

    def setup_menu(self):
        menubar = self.menuBar()
        menubar.setObjectName("menuBar")

        file_menu = menubar.addMenu("📁 File")
        file_menu.setObjectName("menuFile")

        new_action = QAction("📄 New Document", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("📂 Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        settings_action = QAction("⚙️ Settings", self)
        settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(settings_action)

        file_menu.addSeparator()

        exit_action = QAction("🚪 Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu("❓ Help")

        about_action = QAction("ℹ️ About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        help_menu.addSeparator()

        docs_action = QAction("📖 Documentation", self)
        help_menu.addAction(docs_action)

    def change_page(self, index):
        titles = [
            "Create PDF",
            "Convert Files",
            "Merge/Split PDFs",
            "Extract Text",
            "Extract SQL Schema",
        ]
        self.page_title.setText(titles[index])
        self.pages.setCurrentIndex(index)

    def toggle_theme(self):
        btn = self.sender()
        if self.current_theme == "light":
            self.current_theme = "dark"
            btn.setText("☀️ Light Mode")
            self.settings.setValue("theme", "dark")
        else:
            self.current_theme = "light"
            btn.setText("🌙 Dark Mode")
            self.settings.setValue("theme", "light")
        self.apply_theme()

    def apply_theme(self):
        from pdfmaster.ui.styles.theme import apply_theme

        app = QApplication.instance()
        if app:
            apply_theme(app, self.current_theme)

    def new_file(self):
        self.sidebar.setCurrentRow(0)
        self.create_window.clear()

    def open_file(self):
        from PyQt6.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if file_path:
            self.status_bar.showMessage(f"Opened: {file_path}")

    def show_settings(self):
        from pdfmaster.ui.widgets.recent_files import RecentFilesWidget

        from PyQt6.QtWidgets import QDialog, QDialogButtonBox

        dialog = QDialog(self)
        dialog.setWindowTitle("⚙️ Settings")
        layout = QVBoxLayout()

        title = QLabel("📋 Recent Files")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        self.recent_widget = RecentFilesWidget()
        layout.addWidget(self.recent_widget)

        clear_btn = QPushButton("🗑️ Clear Recent Files")
        clear_btn.setObjectName("secondaryButton")
        clear_btn.setProperty("secondary", True)
        clear_btn.clicked.connect(self.recent_widget.clear_recent)
        layout.addWidget(clear_btn)

        layout.addItem(
            QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)

        dialog.setLayout(layout)
        dialog.exec()

    def show_quick_actions(self):
        from PyQt6.QtWidgets import QMenu

        menu = QMenu(self)

        menu.addAction("📄 Create New PDF", lambda: self.sidebar.setCurrentRow(0))
        menu.addAction("🔄 Convert Files", lambda: self.sidebar.setCurrentRow(1))
        menu.addAction("🔗 Merge/Split PDFs", lambda: self.sidebar.setCurrentRow(2))
        menu.addAction("📝 Extract Text", lambda: self.sidebar.setCurrentRow(3))
        menu.addAction("🗄️ Extract SQL Schema", lambda: self.sidebar.setCurrentRow(4))

        menu.addSeparator()
        menu.addAction("📂 Open File", self.open_file)

        from PyQt6.QtWidgets import QPushButton

        btn = self.sender()
        if btn:
            menu.exec(btn.mapToGlobal(btn.rect().bottomLeft()))

    def show_about(self):
        QMessageBox.about(
            self,
            "About PDF Master",
            "📄 PDF Master v1.1.0 - Premium Edition\n\n"
            "A comprehensive PDF application for creation, "
            "editing, conversion, merging, and extraction.\n\n"
            "✨ Premium Features:\n"
            "- Modern Dark/Light Theme\n"
            "- Quick Actions Panel\n"
            "- PDF Merge & Split\n"
            "- Enhanced User Experience\n\n"
            "© 2026 PDF Master Team",
        )


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PDF Master")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("PDFMaster")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
