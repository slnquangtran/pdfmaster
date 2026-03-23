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
    QGroupBox,
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
        layout.setSpacing(20)
        self.setLayout(layout)

        form_container = QWidget()
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        form_container.setLayout(form_layout)
        layout.addWidget(form_container)

        input_group = QGroupBox("Document Settings")
        input_group.setObjectName("settingsGroup")
        input_group_layout = QVBoxLayout()
        input_group_layout.setSpacing(15)
        input_group.setLayout(input_group_layout)
        form_layout.addWidget(input_group)

        title_row = QHBoxLayout()
        title_label = QLabel("📝 Document Title")
        title_label.setObjectName("fieldLabel")
        title_row.addWidget(title_label)
        title_row.addStretch()
        input_group_layout.addLayout(title_row)
        
        self.title_input = QLineEdit()
        self.title_input.setObjectName("inputField")
        self.title_input.setPlaceholderText("Enter document title...")
        input_group_layout.addWidget(self.title_input)

        author_row = QHBoxLayout()
        author_label = QLabel("👤 Author")
        author_label.setObjectName("fieldLabel")
        author_row.addWidget(author_label)
        author_row.addStretch()
        input_group_layout.addLayout(author_row)
        
        self.author_input = QLineEdit()
        self.author_input.setObjectName("inputField")
        self.author_input.setPlaceholderText("Enter author name...")
        input_group_layout.addWidget(self.author_input)

        page_size_row = QHBoxLayout()
        page_label = QLabel("📄 Page Size")
        page_label.setObjectName("fieldLabel")
        page_size_row.addWidget(page_label)
        page_size_row.addStretch()
        input_group_layout.addLayout(page_size_row)
        
        self.page_size_combo = QComboBox()
        self.page_size_combo.setObjectName("comboBox")
        self.page_size_combo.addItems(["A4 (210 x 297 mm)", "Letter (8.5 x 11 in)", "Legal (8.5 x 14 in)"])
        input_group_layout.addWidget(self.page_size_combo)

        content_group = QGroupBox("Document Content")
        content_group.setObjectName("contentGroup")
        content_layout = QVBoxLayout()
        content_group.setLayout(content_layout)
        form_layout.addWidget(content_group)

        content_label = QLabel("📃 Content")
        content_label.setObjectName("fieldLabel")
        content_layout.addWidget(content_label)

        self.content_text = QTextEdit()
        self.content_text.setObjectName("contentText")
        self.content_text.setPlaceholderText("Enter your document content here...\n\nYou can add multiple paragraphs.")
        self.content_text.setMinimumHeight(250)
        content_layout.addWidget(self.content_text)

        stats_label = QLabel("💡 Tip: Each line will be a new paragraph in the PDF")
        stats_label.setObjectName("tipLabel")
        form_layout.addWidget(stats_label)

        self.progress = QProgressBar()
        self.progress.setObjectName("progressBar")
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.preview_btn = QPushButton("👁️ Preview")
        self.preview_btn.setObjectName("secondaryButton")
        self.preview_btn.setProperty("secondary", True)
        self.preview_btn.clicked.connect(self.preview)
        button_layout.addWidget(self.preview_btn)

        self.save_btn = QPushButton("💾 Save PDF")
        self.save_btn.setObjectName("primaryButton")
        self.save_btn.clicked.connect(self.save_pdf)
        button_layout.addWidget(self.save_btn)

        self.clear_btn = QPushButton("🗑️ Clear")
        self.clear_btn.setObjectName("secondaryButton")
        self.clear_btn.setProperty("secondary", True)
        self.clear_btn.clicked.connect(self.clear)
        button_layout.addWidget(self.clear_btn)

        button_layout.addStretch()
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

        page_size = "A4"
        if "Letter" in self.page_size_combo.currentText():
            page_size = "Letter"
        elif "Legal" in self.page_size_combo.currentText():
            page_size = "Legal"

        self.worker = PDFCreateWorker(
            self.title_input.text(),
            self.author_input.text(),
            self.content_text.toPlainText(),
            page_size,
            file_path,
        )
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self, path):
        self.progress.setVisible(False)
        self.save_btn.setEnabled(True)
        QMessageBox.information(self, "✅ Success", f"PDF saved to:\n{path}")
        self.clear()

    def on_error(self, error):
        self.progress.setVisible(False)
        self.save_btn.setEnabled(True)
        QMessageBox.critical(self, "❌ Error", f"Failed to create PDF:\n{error}")

    def clear(self):
        self.title_input.clear()
        self.author_input.clear()
        self.content_text.clear()
        self.page_size_combo.setCurrentIndex(0)