"""
Document Library Page for PDF Master
Based on Editorial Workspace design - Image 6
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QGridLayout,
    QScrollArea,
    QToolButton,
    QButtonGroup,
    QSizePolicy,
    QSpacerItem,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor


class FilterButton(QPushButton):
    """Filter button for library filtering"""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(QFont("Inter", 13))

    def set_active(self, active):
        self.setChecked(active)
        if active:
            self.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: #171c22;
                    border: none;
                    padding: 10px 16px;
                    border-radius: 8px;
                    font-weight: 600;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #414751;
                    border: none;
                    padding: 10px 16px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #eaeef6;
                }
            """)


class DocumentRow(QFrame):
    """Document row item in library list"""

    def __init__(self, icon, icon_color, name, path, date, size, parent=None):
        super().__init__(parent)
        self.setup_ui(icon, icon_color, name, path, date, size)

    def setup_ui(self, icon, icon_color, name, path, date, size):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(72)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(16)

        # Icon
        icon_container = QFrame()
        icon_container.setFixedSize(40, 48)
        icon_container.setStyleSheet(f"""
            QFrame {{
                background-color: {icon_color}15;
                border-radius: 8px;
            }}
        """)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"font-size: 20px; color: {icon_color};")
        icon_layout.addWidget(icon_label)

        layout.addWidget(icon_container)

        # Name and path
        name_layout = QVBoxLayout()
        name_layout.setSpacing(4)

        name_label = QLabel(name)
        name_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #171c22;")
        name_layout.addWidget(name_label)

        path_label = QLabel(path)
        path_label.setStyleSheet("color: #414751; font-size: 12px;")
        name_layout.addWidget(path_label)

        layout.addLayout(name_layout, 2)

        # Date
        date_label = QLabel(date)
        date_label.setStyleSheet("color: #414751; font-size: 13px;")
        layout.addWidget(date_label, 1)

        # Size
        size_label = QLabel(size)
        size_label.setStyleSheet("color: #414751; font-size: 13px;")
        layout.addWidget(size_label, 1)

        # Actions
        actions_btn = QLabel("⋯")
        actions_btn.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #414751;
                padding: 8px;
            }
            QLabel:hover {
                color: #004f8f;
            }
        """)
        actions_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(actions_btn)


class CuratedSpaceCard(QFrame):
    """Curated space feature card"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #eaeef6;
                border-radius: 16px;
            }
        """)
        self.setMinimumHeight(280)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)

        # Badge
        badge = QLabel("CURATED SPACE")
        badge.setStyleSheet("""
            QLabel {
                background-color: #004f8f;
                color: white;
                padding: 4px 12px;
                border-radius: 4px;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 0.05em;
            }
        """)
        badge.setFixedWidth(130)
        layout.addWidget(badge)

        # Title
        title = QLabel("Quarterly Performance Analysis Project")
        title.setFont(QFont("Inter", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #171c22;")
        title.setWordWrap(True)
        layout.addWidget(title)

        # Description
        desc = QLabel(
            "Organize and annotate all related financial datasets and stakeholder presentations."
        )
        desc.setStyleSheet("color: #414751; font-size: 14px;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        layout.addStretch()

        # Team
        team_layout = QHBoxLayout()

        # Avatars placeholder
        avatars = QLabel("👤 👤 +4")
        avatars.setStyleSheet("font-size: 14px;")
        team_layout.addWidget(avatars)

        team_text = QLabel('Shared with "The Strategist" team')
        team_text.setStyleSheet("color: #414751; font-size: 12px;")
        team_layout.addWidget(team_text)

        team_layout.addStretch()
        layout.addLayout(team_layout)


class SmartCurationCard(QFrame):
    """AI Smart Curation feature card"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0067b8, stop:1 #004f8f);
                border-radius: 16px;
            }
        """)
        self.setMinimumHeight(280)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)

        # Icon
        icon_label = QLabel("✨")
        icon_label.setStyleSheet("font-size: 32px;")
        layout.addWidget(icon_label)

        # Title
        title = QLabel("AI Smart Curation")
        title.setFont(QFont("Inter", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        # Description
        desc = QLabel("Let the Digital Curator auto-tag and categorize your last 50 uploads.")
        desc.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 14px;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        layout.addStretch()

        # Button
        enable_btn = QPushButton("ENABLE AUTO-PILOT")
        enable_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #004f8f;
                border: none;
                padding: 14px 24px;
                border-radius: 8px;
                font-weight: 700;
                font-size: 12px;
                letter-spacing: 0.05em;
            }
            QPushButton:hover {
                background-color: #f7f9ff;
            }
        """)
        enable_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(enable_btn)


class DocumentLibrary(QWidget):
    """Document Library page - Image 6 from design"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: #f7f9ff;")

        # Main scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        content = QWidget()
        main_layout = QVBoxLayout(content)
        main_layout.setContentsMargins(40, 32, 40, 32)
        main_layout.setSpacing(24)

        # Header
        header_layout = QHBoxLayout()

        title_section = QVBoxLayout()
        title_section.setSpacing(8)

        title = QLabel("Library")
        title.setObjectName("pageTitle")
        title.setFont(QFont("Inter", 36, QFont.Weight.Bold))
        title.setStyleSheet("color: #171c22; letter-spacing: -0.02em;")
        title_section.addWidget(title)

        subtitle = QLabel("Manage and curate your digital document collection.")
        subtitle.setObjectName("pageSubtitle")
        subtitle.setStyleSheet("color: #414751; font-size: 16px;")
        title_section.addWidget(subtitle)

        header_layout.addLayout(title_section, 1)

        # Header actions
        actions = QHBoxLayout()
        actions.setSpacing(12)

        analytics_btn = QPushButton("View Analytics")
        analytics_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #004f8f;
                border: none;
                padding: 12px 20px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #eaeef6;
                border-radius: 8px;
            }
        """)
        analytics_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        actions.addWidget(analytics_btn)

        new_collection_btn = QPushButton("+ New Collection")
        new_collection_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #004f8f, stop:1 #0067b8);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
            }
        """)
        new_collection_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        actions.addWidget(new_collection_btn)

        header_layout.addLayout(actions)

        main_layout.addLayout(header_layout)

        # Filter bar
        filter_bar = QFrame()
        filter_bar.setStyleSheet("""
            QFrame {
                background-color: #f0f4fc;
                border-radius: 12px;
                padding: 4px;
            }
        """)
        filter_layout = QHBoxLayout(filter_bar)
        filter_layout.setContentsMargins(8, 8, 8, 8)
        filter_layout.setSpacing(4)

        # Filter buttons
        self.all_btn = FilterButton("All Files")
        self.all_btn.set_active(True)
        filter_layout.addWidget(self.all_btn)

        self.pdfs_btn = FilterButton("PDFs")
        filter_layout.addWidget(self.pdfs_btn)

        self.scans_btn = FilterButton("Scans")
        filter_layout.addWidget(self.scans_btn)

        self.markups_btn = FilterButton("Markups")
        filter_layout.addWidget(self.markups_btn)

        filter_layout.addStretch()

        # Sort controls
        sort_label = QLabel("SORTED BY: NAME")
        sort_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: 700;
                color: #414751;
                letter-spacing: 0.1em;
            }
        """)
        filter_layout.addWidget(sort_label)

        sort_icon = QLabel("↕")
        sort_icon.setStyleSheet("font-size: 16px; color: #414751;")
        sort_icon.setCursor(Qt.CursorShape.PointingHandCursor)
        filter_layout.addWidget(sort_icon)

        view_icon = QLabel("☰")
        view_icon.setStyleSheet("font-size: 16px; color: #414751;")
        view_icon.setCursor(Qt.CursorShape.PointingHandCursor)
        filter_layout.addWidget(view_icon)

        main_layout.addWidget(filter_bar)

        # Table header
        table_header = QFrame()
        table_header.setStyleSheet("""
            QFrame {
                background-color: transparent;
                padding: 12px 16px;
            }
        """)
        table_header_layout = QHBoxLayout(table_header)
        table_header_layout.setContentsMargins(56, 12, 16, 12)

        col_name = QLabel("NAME")
        col_name.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: 700;
                color: #414751;
                letter-spacing: 0.1em;
            }
        """)
        table_header_layout.addWidget(col_name, 2)

        col_date = QLabel("DATE MODIFIED")
        col_date.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: 700;
                color: #414751;
                letter-spacing: 0.1em;
            }
        """)
        table_header_layout.addWidget(col_date, 1)

        col_size = QLabel("SIZE")
        col_size.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: 700;
                color: #414751;
                letter-spacing: 0.1em;
            }
        """)
        table_header_layout.addWidget(col_size, 1)

        col_actions = QLabel("ACTIONS")
        col_actions.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: 700;
                color: #414751;
                letter-spacing: 0.1em;
            }
        """)
        table_header_layout.addWidget(col_actions, 0)

        main_layout.addWidget(table_header)

        # Document list
        docs_frame = QFrame()
        docs_frame.setObjectName("card")
        docs_layout = QVBoxLayout(docs_frame)
        docs_layout.setContentsMargins(8, 8, 8, 8)
        docs_layout.setSpacing(4)

        docs_layout.addWidget(
            DocumentRow(
                "PDF",
                "#ba1a1a",
                "Q4_Financial_Summary_2023.pdf",
                "Annual Reports / Finance",
                "Dec 14, 2023, 11:24 AM",
                "2.4 MB",
            )
        )

        docs_layout.addWidget(
            DocumentRow(
                "PDF",
                "#004f8f",
                "Neural_Networks_Research_Draft.pdf",
                "Research Papers / AI",
                "Yesterday, 4:50 PM",
                "15.8 MB",
            )
        )

        docs_layout.addWidget(
            DocumentRow(
                "PDF",
                "#006e2c",
                "Brand_Identity_v2_FINAL.pdf",
                "Design System / Assets",
                "Oct 02, 2023, 09:12 AM",
                "42.1 MB",
            )
        )

        docs_layout.addWidget(
            DocumentRow(
                "PDF",
                "#494e55",
                "Employee_Handbook_2024.pdf",
                "HR / Onboarding",
                "Jan 05, 2024, 02:30 PM",
                "1.2 MB",
            )
        )

        main_layout.addWidget(docs_frame)

        # Featured section
        featured_layout = QHBoxLayout()
        featured_layout.setSpacing(24)

        curated_card = CuratedSpaceCard()
        featured_layout.addWidget(curated_card, 2)

        curation_card = SmartCurationCard()
        featured_layout.addWidget(curation_card, 1)

        main_layout.addLayout(featured_layout)

        main_layout.addStretch()

        scroll.setWidget(content)

        # Main layout for widget
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(scroll)
