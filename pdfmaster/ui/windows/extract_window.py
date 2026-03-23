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
    QGroupBox,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent


class ExtractTextWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, input_path):
        super().__init__()
        self.input_path = input_path

    def run(self):
        try:
            from pdfmaster.src.extractors.text_extractor import TextExtractor

            extractor = TextExtractor()
            text = extractor.extract(self.input_path)
            self.finished.emit(text)
        except Exception as e:
            self.error.emit(str(e))


class FileDropLine(QLineEdit):
    file_dropped = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setObjectName("fileDropLine")
        self.setPlaceholderText("📄 Drop PDF file here or click to browse...")
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


class ExtractWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.extracted_text = ""
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        self.setLayout(layout)

        input_group = QGroupBox("PDF File Selection")
        input_group.setObjectName("settingsGroup")
        input_layout = QVBoxLayout()
        input_layout.setSpacing(15)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        input_label = QLabel("📄 Select PDF File")
        input_label.setObjectName("fieldLabel")
        input_layout.addWidget(input_label)

        self.file_input = FileDropLine()
        self.file_input.setObjectName("inputField")
        input_layout.addWidget(self.file_input)

        info_label = QLabel("💡 Supported: Any PDF file with text content")
        info_label.setObjectName("infoLabel")
        input_layout.addWidget(info_label)

        self.progress = QProgressBar()
        self.progress.setObjectName("progressBar")
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        self.result_label = QLabel()
        self.result_label.setObjectName("resultLabel")
        layout.addWidget(self.result_label)

        button_layout = QHBoxLayout()
        
        extract_btn = QPushButton("📝 Extract Text")
        extract_btn.setObjectName("primaryButton")
        extract_btn.clicked.connect(self.extract_text)
        button_layout.addWidget(extract_btn)

        save_btn = QPushButton("💾 Save as TXT")
        save_btn.setObjectName("secondaryButton")
        save_btn.setProperty("secondary", True)
        save_btn.clicked.connect(self.save_text)
        button_layout.addWidget(save_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)

    def extract_text(self):
        input_path = self.file_input.text()
        if not input_path:
            QMessageBox.warning(self, "No File", "Please select a PDF file.")
            return

        self.progress.setVisible(True)
        self.result_label.setText("⏳ Extracting text...")
        self.worker = ExtractTextWorker(input_path)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self, text):
        self.progress.setVisible(False)
        self.extracted_text = text
        self.result_label.setText(f"✅ Extracted {len(text)} characters from PDF")
        QMessageBox.information(
            self, 
            "✅ Extraction Complete", 
            f"Text extracted successfully!\n\nLength: {len(text)} characters"
        )

    def on_error(self, error):
        self.progress.setVisible(False)
        self.result_label.setText("❌ Extraction failed")
        QMessageBox.critical(self, "❌ Error", f"Failed to extract text:\n{error}")

    def save_text(self):
        if not self.extracted_text:
            QMessageBox.warning(self, "No Text", "Please extract text first.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Text",
            "extracted.txt",
            "Text Files (*.txt)",
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.extracted_text)
                QMessageBox.information(self, "✅ Saved", f"Text saved to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "❌ Error", f"Failed to save:\n{e}")