"""
Premium Sidebar Widget for PDF Master
Based on Editorial Workspace design specification
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QFrame,
    QSpacerItem,
    QSizePolicy,
    QToolButton,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QColor, QPixmap, QPainter


class NavItem(QFrame):
    """Custom navigation item widget"""

    clicked = pyqtSignal(str)

    def __init__(self, icon_text, label, nav_id, parent=None):
        super().__init__(parent)
        self.nav_id = nav_id
        self.is_selected = False
        self.setup_ui(icon_text, label)

    def setup_ui(self, icon_text, label):
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(12)

        # Icon placeholder (using text)
        self.icon_label = QLabel(icon_text)
        self.icon_label.setObjectName("navIcon")
        self.icon_label.setFixedSize(24, 24)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.icon_label)

        # Label
        self.text_label = QLabel(label)
        self.text_label.setObjectName("navLabel")
        self.text_label.setFont(QFont("Inter", 11, QFont.Weight.Medium))
        layout.addWidget(self.text_label)

        layout.addStretch()

    def set_selected(self, selected):
        self.is_selected = selected
        if selected:
            self.setProperty("selected", True)
            self.style().unpolish(self)
            self.style().polish(self)
        else:
            self.setProperty("selected", False)
            self.style().unpolish(self)
            self.style().polish(self)

    def mousePressEvent(self, event):
        self.clicked.emit(self.nav_id)
        super().mousePressEvent(event)


class PremiumSidebar(QWidget):
    """Premium sidebar component based on Editorial Workspace design"""

    page_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.nav_items = {}
        self.current_page = "workspace"
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("sidebarContainer")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo Section
        logo_container = QWidget()
        logo_container.setObjectName("logoContainer")
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(16, 20, 16, 20)

        # Logo with icon
        logo_row = QHBoxLayout()
        logo_icon = QLabel("📘")
        logo_icon.setFixedSize(32, 32)
        logo_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_row.addWidget(logo_icon)

        logo_text = QLabel("Editorial\nWorkspace")
        logo_text.setObjectName("logoLabel")
        logo_text.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        logo_text.setWordWrap(True)
        logo_row.addWidget(logo_text, 1)

        logo_layout.addLayout(logo_row)

        # Upload Button
        upload_btn = QPushButton("⬆  Upload PDF")
        upload_btn.setObjectName("uploadPdfBtn")
        upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        upload_btn.clicked.connect(lambda: self.page_changed.emit("upload"))
        logo_layout.addWidget(upload_btn)

        layout.addWidget(logo_container)

        # Main Navigation
        nav_container = QWidget()
        nav_container.setObjectName("navContainer")
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(8, 8, 8, 8)
        nav_layout.setSpacing(2)

        # Primary navigation items
        self.add_nav_item(nav_layout, "📁", "Library", "library")
        self.add_nav_item(nav_layout, "🕐", "Recent", "recent")
        self.add_nav_item(nav_layout, "⭐", "Starred", "starred")
        self.add_nav_item(nav_layout, "✏️", "Annotated", "annotated")
        self.add_nav_item(nav_layout, "📦", "Archive", "archive")

        nav_layout.addStretch()
        layout.addWidget(nav_container, 1)

        # Quick Access Section
        quick_access_container = QWidget()
        quick_access_layout = QVBoxLayout(quick_access_container)
        quick_access_layout.setContentsMargins(8, 0, 8, 0)

        section_header = QLabel("QUICK ACCESS")
        section_header.setObjectName("sectionHeader")
        quick_access_layout.addWidget(section_header)

        self.add_nav_item(quick_access_layout, "📂", "Annual Reports", "annual_reports")
        self.add_nav_item(quick_access_layout, "📂", "Research Papers", "research_papers")

        layout.addWidget(quick_access_container)

        # Bottom Section
        bottom_container = QWidget()
        bottom_container.setObjectName("bottomContainer")
        bottom_layout = QVBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(8, 0, 8, 16)
        bottom_layout.setSpacing(4)

        # Settings and Support
        self.add_nav_item(bottom_layout, "⚙️", "Settings", "settings")
        self.add_nav_item(bottom_layout, "❓", "Support", "support")

        # User Profile
        profile_container = QWidget()
        profile_container.setObjectName("userProfile")
        profile_layout = QHBoxLayout(profile_container)
        profile_layout.setContentsMargins(12, 12, 12, 12)

        avatar = QLabel("👤")
        avatar.setFixedSize(40, 40)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("""
            QLabel {
                background-color: #004f8f;
                border-radius: 20px;
                font-size: 20px;
            }
        """)
        profile_layout.addWidget(avatar)

        profile_info = QVBoxLayout()
        profile_info.setSpacing(2)

        user_name = QLabel("Digital Curator")
        user_name.setObjectName("userName")
        user_name.setFont(QFont("Inter", 13, QFont.Weight.Bold))
        profile_info.addWidget(user_name)

        user_role = QLabel("Premium Account")
        user_role.setObjectName("userRole")
        user_role.setFont(QFont("Inter", 11))
        profile_info.addWidget(user_role)

        profile_layout.addLayout(profile_info, 1)
        bottom_layout.addWidget(profile_container)

        layout.addWidget(bottom_container)

        # Set initial selection
        self.set_selected("library")

    def add_nav_item(self, layout, icon, label, nav_id):
        item = NavItem(icon, label, nav_id)
        item.clicked.connect(self.on_nav_clicked)
        layout.addWidget(item)
        self.nav_items[nav_id] = item

    def on_nav_clicked(self, nav_id):
        self.set_selected(nav_id)
        self.page_changed.emit(nav_id)

    def set_selected(self, nav_id):
        self.current_page = nav_id
        for id, item in self.nav_items.items():
            item.set_selected(id == nav_id)

    def get_current_page(self):
        return self.current_page
