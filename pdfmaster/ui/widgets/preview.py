import sys
from pathlib import Path
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
)
from PyQt6.QtGui import QPixmap, QImage


class PDFPreviewWidget(QWidget):
    file_loaded = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        self.placeholder = QLabel("📄 PDF Preview\n\nClick 'Generate Preview' to see your PDF")
        self.placeholder.setObjectName("previewPlaceholder")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.placeholder)
        
        self.info_label = QLabel()
        self.info_label.setObjectName("previewInfo")
        self.info_label.setVisible(False)
        layout.addWidget(self.info_label)
    
    def load_pdf_info(self, pdf_path):
        if not pdf_path or not Path(pdf_path).exists():
            return
        
        pdf_path = Path(pdf_path)
        self.current_file = pdf_path
        
        try:
            import fitz
            doc = fitz.open(pdf_path)
            page_count = len(doc)
            size_kb = pdf_path.stat().st_size / 1024
            
            info_text = f"📄 {pdf_path.name}\n📊 {page_count} page(s) • {size_kb:.1f} KB"
            self.info_label.setText(info_text)
            self.info_label.setVisible(True)
            self.placeholder.setVisible(False)
            
            doc.close()
            self.file_loaded.emit(str(pdf_path))
            
        except Exception as e:
            self.info_label.setText(f"❌ Cannot preview: {str(e)}")
            self.info_label.setVisible(True)
    
    def clear(self):
        self.current_file = None
        self.info_label.setVisible(False)
        self.placeholder.setVisible(True)
    
    @property
    def is_empty(self):
        return self.current_file is None