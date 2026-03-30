import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import Qt, pyqtSignal


class QuickActionsWidget(QWidget):
    action_triggered = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        self.setLayout(layout)
        
        title = QLabel("⚡ Quick Actions")
        title.setObjectName("quickActionsTitle")
        layout.addWidget(title)
        
        grid = QGridLayout()
        grid.setSpacing(10)
        
        actions = [
            ("📄 New PDF", "new_pdf"),
            ("🔄 Convert", "convert"),
            ("📝 Extract", "extract"),
            ("🗄️ SQL Schema", "sql"),
            ("📁 Open File", "open"),
            ("⚙️ Settings", "settings"),
        ]
        
        for i, (label, action) in enumerate(actions):
            btn = QPushButton(label)
            btn.setObjectName("quickActionBtn")
            btn.clicked.connect(lambda checked, a=action: self.action_triggered.emit(a))
            grid.addWidget(btn, i // 2, i % 2)
        
        layout.addLayout(grid)