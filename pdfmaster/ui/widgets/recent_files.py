import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from PyQt6.QtCore import Qt, QSettings, pyqtSignal
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView


class RecentFilesWidget(QListWidget):
    file_opened = pyqtSignal(str)
    
    def __init__(self, max_items=10):
        super().__init__()
        self.max_items = max_items
        self.settings = QSettings("PDFMaster", "PDFMaster")
        self.load_recent_files()
        
        self.setObjectName("recentFiles")
        self.setMinimumHeight(150)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.itemDoubleClicked.connect(self.on_item_double_clicked)
    
    def load_recent_files(self):
        files = self.settings.value("recent_files", [])
        if files:
            for f in files[:self.max_items]:
                self.add_recent_item(f)
    
    def save_recent_files(self):
        files = []
        for i in range(self.count()):
            item = self.item(i)
            files.append(item.data(Qt.ItemDataRole.UserRole))
        self.settings.setValue("recent_files", files)
    
    def add_recent_item(self, file_path):
        file_path = Path(file_path)
        if not file_path.exists():
            return
        
        for i in range(self.count()):
            if self.item(i).data(Qt.ItemDataRole.UserRole) == str(file_path):
                self.takeItem(i)
                break
        
        icon = "📄"
        if file_path.suffix.lower() == ".pdf":
            icon = "📕"
        elif file_path.suffix.lower() in [".doc", ".docx"]:
            icon = "📘"
        elif file_path.suffix.lower() in [".txt"]:
            icon = "📝"
        elif file_path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
            icon = "🖼️"
        
        item = QListWidgetItem(f"{icon} {file_path.name}")
        item.setData(Qt.ItemDataRole.UserRole, str(file_path))
        item.setToolTip(str(file_path))
        
        self.insertItem(0, item)
        
        while self.count() > self.max_items:
            self.takeItem(self.count() - 1)
        
        self.save_recent_files()
    
    def on_item_double_clicked(self, item):
        file_path = item.data(Qt.ItemDataRole.UserRole)
        if file_path and Path(file_path).exists():
            self.file_opened.emit(file_path)
    
    def clear_recent(self):
        self.clear()
        self.settings.setValue("recent_files", [])
    
    def get_recent_files(self):
        return [self.item(i).data(Qt.ItemDataRole.UserRole) for i in range(self.count())]