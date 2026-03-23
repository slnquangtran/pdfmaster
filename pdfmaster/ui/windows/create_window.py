import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QComboBox,
    QFileDialog,
    QMessageBox,
    QProgressBar,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal


class PDFCreateWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, title, author, content, page_size, output_path):
        super().__init__()
        self.title = title
        self.author = author
        self.content = content
        self.page_size = page_size
        self.output_path = output_path

    def run(self):
        try:
            from pdfmaster.src.core.creator import PDFCreator

            creator = PDFCreator(title=self.title, author=self.author, page_size=self.page_size)
            
            lines = self.content.split('\n')
            y = 720
            for line in lines:
                if line.strip():
                    creator.add_text(line, y=y)
                    y -= 20
                    if y < 50:
                        creator.new_page()
                        y = 720

            creator.save(self.output_path)
            self.finished.emit(self.output_path)
        except Exception as e:
            self.error.emit(str(e))


class CreateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel("Create New PDF")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        form_layout = QVBoxLayout()
        
        layout.addLayout(form_layout)

        input_group = QWidget()
        input_layout = QVBoxLayout()
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        title_row = QHBoxLayout()
        title_row.addWidget(QLabel("Title:"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Document title")
        title_row.addWidget(self.title_input)
        input_layout.addLayout(title_row)

        author_row = QHBoxLayout()
        author_row.addWidget(QLabel("Author:"))
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Author name")
        author_row.addWidget(self.author_input)
        input_layout.addLayout(author_row)

        page_size_row = QHBoxLayout()
        page_size_row.addWidget(QLabel("Page Size:"))
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["A4", "Letter", "Legal"])
        page_size_row.addWidget(self.page_size_combo)
        page_size_row.addStretch()
        input_layout.addLayout(page_size_row)

        content_label = QLabel("Content:")
        input_layout.addWidget(content_label)

        self.content_text = QTextEdit()
        self.content_text.setPlaceholderText("Enter your content here...")
        self.content_text.setMinimumHeight(300)
        input_layout.addWidget(self.content_text)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        button_layout = QHBoxLayout()
        
        self.preview_btn = QPushButton("Preview")
        self.preview_btn.clicked.connect(self.preview)
        button_layout.addWidget(self.preview_btn)

        self.save_btn = QPushButton("Save PDF")
        self.save_btn.clicked.connect(self.save_pdf)
        button_layout.addWidget(self.save_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear)
        button_layout.addWidget(self.clear_btn)

        layout.addLayout(button_layout)

    def preview(self):
        if not self.content_text.toPlainText().strip():
            QMessageBox.warning(self, "No Content", "Please enter some content to preview.")
            return
        self.save_pdf(preview=True)

    def save_pdf(self, preview=False):
        if not self.content_text.toPlainText().strip() and not preview:
            QMessageBox.warning(self, "No Content", "Please enter some content.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF",
            f"{self.title_input.text() or 'document'}.pdf",
            "PDF Files (*.pdf)",
        )

        if not file_path:
            return

        self.save_btn.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)

        self.worker = PDFCreateWorker(
            self.title_input.text(),
            self.author_input.text(),
            self.content_text.toPlainText(),
            self.page_size_combo.currentText(),
            file_path,
        )
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self, path):
        self.progress.setVisible(False)
        self.save_btn.setEnabled(True)
        QMessageBox.information(self, "Success", f"PDF saved to:\n{path}")
        self.clear()

    def on_error(self, error):
        self.progress.setVisible(False)
        self.save_btn.setEnabled(True)
        QMessageBox.critical(self, "Error", f"Failed to create PDF:\n{error}")

    def clear(self):
        self.title_input.clear()
        self.author_input.clear()
        self.content_text.clear()
        self.page_size_combo.setCurrentIndex(0)