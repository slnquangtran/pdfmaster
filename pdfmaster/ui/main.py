import sys
from pathlib import Path

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
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Master")
        self.setMinimumSize(900, 600)
        self.resize(1000, 700)

        self.setup_ui()
        self.setup_menu()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.addItems(
            [
                "Create PDF",
                "Convert Files",
                "Extract Text",
                "Extract SQL Schema",
            ]
        )
        self.sidebar.currentRowChanged.connect(self.change_page)
        main_layout.addWidget(self.sidebar)

        self.pages = QStackedWidget()

        from pdfmaster.ui.windows.create_window import CreateWindow
        from pdfmaster.ui.windows.convert_window import ConvertWindow
        from pdfmaster.ui.windows.extract_window import ExtractWindow
        from pdfmaster.ui.windows.extract_schema_window import ExtractSchemaWindow

        self.create_window = CreateWindow()
        self.convert_window = ConvertWindow()
        self.extract_window = ExtractWindow()
        self.extract_schema_window = ExtractSchemaWindow()

        self.pages.addWidget(self.create_window)
        self.pages.addWidget(self.convert_window)
        self.pages.addWidget(self.extract_window)
        self.pages.addWidget(self.extract_schema_window)

        main_layout.addWidget(self.pages)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def setup_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def change_page(self, index):
        self.pages.setCurrentIndex(index)

    def new_file(self):
        self.sidebar.setCurrentRow(0)
        self.create_window.clear()

    def open_file(self):
        from PyQt6.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open PDF", "", "PDF Files (*.pdf)"
        )
        if file_path:
            self.status_bar.showMessage(f"Opened: {file_path}")

    def show_about(self):
        QMessageBox.about(
            self,
            "About PDF Master",
            "PDF Master v1.0.0\n\n"
            "A comprehensive PDF application for creation, "
            "editing, conversion, and extraction.\n\n"
            "(c) 2026 PDF Master Team",
        )


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PDF Master")
    app.setApplicationVersion("1.0.0")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()