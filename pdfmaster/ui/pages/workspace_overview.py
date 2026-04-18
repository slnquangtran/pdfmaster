"""
Workspace Overview Page for PDF Master
Based on Editorial Workspace design - Image 2
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
    QProgressBar,
    QSpacerItem,
    QSizePolicy,
    QListWidget,
    QListWidgetItem,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor


class StorageCard(QFrame):
    """Storage status card component"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("card")
        self.setMinimumHeight(180)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QHBoxLayout()

        title = QLabel("STORAGE STATUS")
        title.setObjectName("sectionHeader")
        title.setFont(QFont("Inter", 11, QFont.Weight.Bold))
        header.addWidget(title)

        header.addStretch()

        cloud_icon = QLabel("☁️")
        cloud_icon.setFixedSize(40, 40)
        cloud_icon.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 79, 143, 0.1);
                border-radius: 8px;
                font-size: 20px;
            }
        """)
        cloud_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.addWidget(cloud_icon)

        layout.addLayout(header)

        # Storage info
        storage_label = QLabel("12.4 GB")
        storage_label.setFont(QFont("Inter", 32, QFont.Weight.Bold))
        storage_label.setStyleSheet("color: #171c22;")
        layout.addWidget(storage_label)

        total_label = QLabel("/ 50 GB")
        total_label.setStyleSheet("color: #414751; font-size: 14px;")
        layout.addWidget(total_label)

        # Progress bar
        progress = QProgressBar()
        progress.setValue(25)
        progress.setTextVisible(False)
        progress.setFixedHeight(8)
        layout.addWidget(progress)

        # Footer
        footer = QHBoxLayout()

        workspace_label = QLabel("Personal Workspace")
        workspace_label.setStyleSheet("color: #414751; font-size: 12px;")
        footer.addWidget(workspace_label)

        footer.addStretch()

        percent_label = QLabel("25% utilized")
        percent_label.setStyleSheet("color: #414751; font-size: 12px;")
        footer.addWidget(percent_label)

        layout.addLayout(footer)


class ActionCard(QFrame):
    """Action card component"""

    def __init__(self, icon, title, description, accent_color="#004f8f", parent=None):
        super().__init__(parent)
        self.accent_color = accent_color
        self.setup_ui(icon, title, description)

    def setup_ui(self, icon, title, description):
        self.setObjectName("card")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(180)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Icon
        icon_label = QLabel(icon)
        icon_label.setFixedSize(64, 64)
        icon_label.setStyleSheet(f"""
            QLabel {{
                background-color: {self.accent_color}15;
                border-radius: 32px;
                font-size: 28px;
            }}
        """)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        # Title
        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        title_label.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        layout.addWidget(title_label)

        # Description
        desc_label = QLabel(description)
        desc_label.setObjectName("cardDescription")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        layout.addStretch()


class RecentDocumentItem(QFrame):
    """Recent document item component"""

    def __init__(self, icon, title, badge, badge_color, time, size, owner, parent=None):
        super().__init__(parent)
        self.setup_ui(icon, title, badge, badge_color, time, size, owner)

    def setup_ui(self, icon, title, badge, badge_color, time, size, owner):
        self.setObjectName("documentItem")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # Icon
        icon_container = QFrame()
        icon_container.setFixedSize(56, 72)
        icon_container.setStyleSheet(f"""
            QFrame {{
                background-color: #eaeef6;
                border-radius: 8px;
            }}
        """)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 24px;")
        icon_layout.addWidget(icon_label)

        # Blue line at bottom
        line = QFrame()
        line.setFixedHeight(4)
        line.setStyleSheet("background-color: #004f8f;")
        icon_layout.addWidget(line)

        layout.addWidget(icon_container)

        # Info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)

        # Title row
        title_row = QHBoxLayout()

        title_label = QLabel(title)
        title_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #171c22;")
        title_row.addWidget(title_label)

        if badge:
            badge_label = QLabel(badge)
            badge_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {badge_color}20;
                    color: {badge_color};
                    padding: 2px 8px;
                    border-radius: 4px;
                    font-size: 10px;
                    font-weight: 700;
                }}
            """)
            title_row.addWidget(badge_label)

        title_row.addStretch()
        info_layout.addLayout(title_row)

        # Meta row
        meta_row = QHBoxLayout()

        meta_label = QLabel(f"🕐 {time}   💾 {size}   👤 {owner}")
        meta_label.setStyleSheet("color: #414751; font-size: 12px;")
        meta_row.addWidget(meta_label)

        meta_row.addStretch()
        info_layout.addLayout(meta_row)

        layout.addLayout(info_layout, 1)

        # More button
        more_btn = QLabel("⋯")
        more_btn.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #414751;
                padding: 8px;
            }
            QLabel:hover {
                color: #004f8f;
            }
        """)
        more_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(more_btn)


class CollectionItem(QFrame):
    """Collection item component"""

    def __init__(self, color, name, count, parent=None):
        super().__init__(parent)
        self.setup_ui(color, name, count)

    def setup_ui(self, color, name, count):
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(12)

        dot = QLabel("●")
        dot.setStyleSheet(f"color: {color}; font-size: 12px;")
        layout.addWidget(dot)

        name_label = QLabel(name)
        name_label.setFont(QFont("Inter", 13, QFont.Weight.Medium))
        name_label.setStyleSheet("color: #171c22;")
        layout.addWidget(name_label, 1)

        count_label = QLabel(f"{count} files")
        count_label.setStyleSheet("color: #414751; font-size: 12px;")
        layout.addWidget(count_label)


class WorkspaceOverview(QWidget):
    """Workspace Overview page - Image 2 from design"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: #f7f9ff;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 32, 40, 32)
        main_layout.setSpacing(32)

        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)

        title = QLabel("Workspace Overview")
        title.setObjectName("pageTitle")
        title.setFont(QFont("Inter", 36, QFont.Weight.Bold))
        title.setStyleSheet("color: #171c22; letter-spacing: -0.02em;")
        header_layout.addWidget(title)

        subtitle = QLabel(
            "Welcome back. Your curated digital library is synced and ready for editorial review."
        )
        subtitle.setObjectName("pageSubtitle")
        subtitle.setStyleSheet("color: #414751; font-size: 16px;")
        subtitle.setWordWrap(True)
        header_layout.addWidget(subtitle)

        main_layout.addLayout(header_layout)

        # Stats Grid
        stats_grid = QHBoxLayout()
        stats_grid.setSpacing(24)

        # Storage card
        storage_card = StorageCard()
        stats_grid.addWidget(storage_card, 2)

        # Merge card
        merge_card = ActionCard(
            "⬆️", "Merge Assets", "Combine multiple manuscripts into a single volume.", "#006e2c"
        )
        stats_grid.addWidget(merge_card, 1)

        main_layout.addLayout(stats_grid)

        # Content Grid
        content_grid = QHBoxLayout()
        content_grid.setSpacing(32)

        # Left Column
        left_column = QVBoxLayout()
        left_column.setSpacing(24)

        # Compress card
        compress_card = QFrame()
        compress_card.setObjectName("card")
        compress_layout = QHBoxLayout(compress_card)
        compress_layout.setContentsMargins(20, 20, 20, 20)
        compress_layout.setSpacing(16)

        compress_icon = QLabel("🗜️")
        compress_icon.setFixedSize(48, 48)
        compress_icon.setStyleSheet("""
            QLabel {
                background-color: #ba1a1a15;
                border-radius: 8px;
                font-size: 24px;
            }
        """)
        compress_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        compress_layout.addWidget(compress_icon)

        compress_info = QVBoxLayout()
        compress_title = QLabel("Compress File")
        compress_title.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        compress_info.addWidget(compress_title)
        compress_desc = QLabel("Reduce size without quality loss")
        compress_desc.setStyleSheet("color: #414751; font-size: 12px;")
        compress_info.addWidget(compress_desc)
        compress_layout.addLayout(compress_info)

        left_column.addWidget(compress_card)

        # Collections card
        collections_card = QFrame()
        collections_card.setObjectName("card")
        collections_layout = QVBoxLayout(collections_card)
        collections_layout.setContentsMargins(20, 20, 20, 20)
        collections_layout.setSpacing(16)

        collections_title = QLabel("Active Collections")
        collections_title.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        collections_layout.addWidget(collections_title)

        collections_layout.addWidget(CollectionItem("#3b82f6", "Q3 Research Papers", 14))
        collections_layout.addWidget(CollectionItem("#10b981", "Design Guidelines", 8))
        collections_layout.addWidget(CollectionItem("#f59e0b", "Legal Drafts", 22))

        left_column.addWidget(collections_card)

        # Promo card
        promo_card = QFrame()
        promo_card.setMinimumHeight(256)
        promo_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a365d, stop:1 #2d3748);
                border-radius: 16px;
            }
        """)
        promo_layout = QVBoxLayout(promo_card)
        promo_layout.setContentsMargins(24, 24, 24, 24)
        promo_layout.setSpacing(12)
        promo_layout.addStretch()

        promo_title = QLabel("Editorial Pro")
        promo_title.setStyleSheet("color: white; font-size: 20px; font-weight: 700;")
        promo_layout.addWidget(promo_title)

        promo_desc = QLabel("Unlock advanced OCR and batch export features.")
        promo_desc.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 14px;")
        promo_layout.addWidget(promo_desc)

        upgrade_btn = QPushButton("UPGRADE NOW")
        upgrade_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1a365d;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: 700;
                font-size: 12px;
                letter-spacing: 0.05em;
            }
            QPushButton:hover {
                background-color: #f7f9ff;
            }
        """)
        upgrade_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        upgrade_btn.setFixedWidth(140)
        promo_layout.addWidget(upgrade_btn)

        left_column.addWidget(promo_card)

        content_grid.addLayout(left_column, 4)

        # Right Column - Recent Documents
        right_column = QVBoxLayout()
        right_column.setSpacing(20)

        # Recent header
        recent_header = QHBoxLayout()

        recent_title = QLabel("Recent Documents")
        recent_title.setFont(QFont("Inter", 20, QFont.Weight.Bold))
        recent_title.setStyleSheet("color: #171c22;")
        recent_header.addWidget(recent_title)

        recent_header.addStretch()

        view_all = QLabel("View All Library →")
        view_all.setStyleSheet("""
            QLabel {
                color: #004f8f;
                font-size: 14px;
                font-weight: 600;
            }
            QLabel:hover {
                text-decoration: underline;
            }
        """)
        view_all.setCursor(Qt.CursorShape.PointingHandCursor)
        recent_header.addWidget(view_all)

        right_column.addLayout(recent_header)

        # Document list
        docs_frame = QFrame()
        docs_frame.setObjectName("card")
        docs_layout = QVBoxLayout(docs_frame)
        docs_layout.setContentsMargins(8, 8, 8, 8)
        docs_layout.setSpacing(4)

        docs_layout.addWidget(
            RecentDocumentItem(
                "📄",
                "annual_report_2023_final.pdf",
                "ANNOTATED",
                "#004f8f",
                "2 hours ago",
                "4.2 MB",
                "You",
            )
        )

        docs_layout.addWidget(
            RecentDocumentItem(
                "📄",
                "brand_identity_guidelines_v2.pdf",
                "SHARED",
                "#006e2c",
                "Yesterday",
                "12.8 MB",
                "Sarah K.",
            )
        )

        docs_layout.addWidget(
            RecentDocumentItem(
                "📄", "q4_marketing_brief_draft.pdf", "", "", "Oct 12, 2023", "850 KB", "You"
            )
        )

        docs_layout.addWidget(
            RecentDocumentItem(
                "📄",
                "user_interview_transcripts.pdf",
                "PRIVATE",
                "#494e55",
                "Oct 10, 2023",
                "1.1 MB",
                "You",
            )
        )

        right_column.addWidget(docs_frame)

        content_grid.addLayout(right_column, 6)

        main_layout.addLayout(content_grid)

        # Floating Toolbar
        self.floating_toolbar = FloatingToolbar()
        self.floating_toolbar.show()


class FloatingToolbar(QFrame):
    """Floating block toolbar component"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("floatingToolbar")
        self.setFixedHeight(56)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(24)

        # Edit group
        edit_group = QHBoxLayout()
        edit_group.setSpacing(16)

        edit_btn = self.create_tool_button("✏️", "EDIT")
        edit_group.addWidget(edit_btn)

        annotate_btn = self.create_tool_button("📝", "ANNOTATE")
        edit_group.addWidget(annotate_btn)

        layout.addLayout(edit_group)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.VLine)
        divider.setStyleSheet("background-color: #e2e8f0;")
        layout.addWidget(divider)

        # Organize group
        organize_group = QHBoxLayout()
        organize_group.setSpacing(16)

        organize_btn = self.create_tool_button("⊞", "ORGANIZE")
        organize_group.addWidget(organize_btn)

        secure_btn = self.create_tool_button("🔒", "SECURE")
        organize_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        organize_group.addWidget(secure_btn)

        layout.addLayout(organize_group)

    def create_tool_button(self, icon, text):
        btn = QFrame()
        btn.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(btn)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(icon_label)

        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                font-weight: 700;
                color: #414751;
                letter-spacing: 0.05em;
            }
        """)
        layout.addWidget(text_label)

        return btn
