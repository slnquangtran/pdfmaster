import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QLineEdit,
    QProgressBar,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent


class ExtractSchemaWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, input_path, table_name):
        super().__init__()
        self.input_path = input_path
        self.table_name = table_name

    def run(self):
        try:
            from pdfmaster.src.extractors.schema_generator import SchemaGenerator

            generator = SchemaGenerator()
            schema = generator.extract(self.input_path, table_name=self.table_name or None)
            self.finished.emit(schema)
        except Exception as e:
            self.error.emit(str(e))


class ExtractSchemaWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.schema_content = ""
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel("Extract SQL Schema from PDF")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("PDF File:"))
        self.file_input = FileDropLine()
        input_layout.addWidget(self.file_input)
        layout.addLayout(input_layout)

        table_layout = QHBoxLayout()
        table_layout.addWidget(QLabel("Table Name (optional):"))
        self.table_name_input = QLineEdit()
        self.table_name_input.setPlaceholderText("e.g., products, users")
        table_layout.addWidget(self.table_name_input)
        table_layout.addStretch()
        layout.addLayout(table_layout)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        button_layout = QHBoxLayout()
        extract_btn = QPushButton("Extract Schema")
        extract_btn.clicked.connect(self.extract_schema)
        button_layout.addWidget(extract_btn)

        save_btn = QPushButton("Save as SQL")
        save_btn.clicked.connect(self.save_sql)
        button_layout.addWidget(save_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)

    def extract_schema(self):
        input_path = self.file_input.text()
        if not input_path:
            QMessageBox.warning(self, "No File", "Please select a PDF file.")
            return

        self.progress.setVisible(True)
        self.worker = ExtractSchemaWorker(
            input_path, self.table_name_input.text()
        )
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self, schema):
        self.progress.setVisible(False)
        self.schema_content = schema
        QMessageBox.information(
            self,
            "Extraction Complete",
            "SQL schema extracted successfully!\n\nClick 'Save as SQL' to save the schema."
        )

    def on_error(self, error):
        self.progress.setVisible(False)
        QMessageBox.critical(self, "Error", f"Failed to extract schema:\n{error}")

    def save_sql(self):
        if not self.schema_content:
            QMessageBox.warning(self, "No Schema", "Please extract schema first.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save SQL Schema",
            "schema.sql",
            "SQL Files (*.sql)",
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.schema_content)
                QMessageBox.information(self, "Saved", f"Schema saved to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save:\n{e}")


class FileDropLine(QLineEdit):
    file_dropped = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setPlaceholderText("Drop PDF file here or click to browse")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith('.pdf'):
                self.setText(path)
                self.file_dropped.emit(path)

    def mousePressEvent(self, event):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select PDF", "", "PDF Files (*.pdf)"
        )
        if file_path:
            self.setText(file_path)
            self.file_dropped.emit(file_path)