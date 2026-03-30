"""
PDF Editor Page for PDF Master
Based on Editorial Workspace design - Image 8
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QScrollArea,
    QSplitter,
    QTextEdit,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont


class EditorToolbar(QFrame):
    """PDF Editor floating toolbar"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 24px;
                padding: 8px 16px;
            }
        """)
        self.setFixedHeight(48)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        # Zoom controls
        zoom_out = self.create_icon_btn("🔍-")
        layout.addWidget(zoom_out)

        zoom_level = QLabel("100%")
        zoom_level.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: 600;
                color: #171c22;
                min-width: 40px;
                text-align: center;
            }
        """)
        layout.addWidget(zoom_level)

        zoom_in = self.create_icon_btn("🔍+")
        layout.addWidget(zoom_in)

        # Divider
        layout.addWidget(self.create_divider())

        # Undo/Redo
        undo_btn = self.create_icon_btn("↩️")
        layout.addWidget(undo_btn)

        redo_btn = self.create_icon_btn("↪️")
        layout.addWidget(redo_btn)

        # Divider
        layout.addWidget(self.create_divider())

        # Tools
        pan_btn = self.create_icon_btn("✋")
        layout.addWidget(pan_btn)

        edit_btn = self.create_icon_btn("✏️", active=True)
        layout.addWidget(edit_btn)

        note_btn = self.create_icon_btn("📝")
        layout.addWidget(note_btn)

        # Divider
        layout.addWidget(self.create_divider())

        # Fullscreen
        fullscreen_btn = self.create_icon_btn("⛶")
        layout.addWidget(fullscreen_btn)

        layout.addStretch()

    def create_icon_btn(self, icon, active=False):
        btn = QLabel(icon)
        btn.setFixedSize(32, 32)
        btn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)

        if active:
            btn.setStyleSheet("""
                QLabel {
                    background-color: rgba(0, 79, 143, 0.1);
                    border-radius: 8px;
                    font-size: 16px;
                }
            """)
        else:
            btn.setStyleSheet("""
                QLabel {
                    border-radius: 8px;
                    font-size: 16px;
                }
                QLabel:hover {
                    background-color: rgba(0, 0, 0, 0.05);
                }
            """)

        return btn

    def create_divider(self):
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.VLine)
        divider.setFixedWidth(1)
        divider.setStyleSheet("background-color: #e2e8f0;")
        return divider


class DocumentViewer(QFrame):
    """PDF Document viewer area"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #f0f4fc;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)

        # PDF Page mockup
        pdf_page = QFrame()
        pdf_page.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 4px;
            }
        """)

        page_layout = QVBoxLayout(pdf_page)
        page_layout.setContentsMargins(48, 48, 48, 48)
        page_layout.setSpacing(24)

        # Header
        header = QVBoxLayout()
        header.setSpacing(16)

        title = QLabel("Quarterly Strategic Initiatives 2024")
        title.setFont(QFont("Inter", 36, QFont.Weight.Bold))
        title.setStyleSheet("color: #171c22; letter-spacing: -0.02em;")
        title.setWordWrap(True)
        header.addWidget(title)

        meta = QHBoxLayout()

        badge = QLabel("CONFIDENTIAL")
        badge.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 79, 143, 0.1);
                color: #004f8f;
                padding: 4px 12px;
                border-radius: 4px;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 0.05em;
            }
        """)
        meta.addWidget(badge)

        version = QLabel("Draft v2.4")
        version.setStyleSheet("color: #414751; font-size: 12px;")
        meta.addWidget(version)

        dot = QLabel("●")
        dot.setStyleSheet("color: #c1c7d3; font-size: 8px;")
        meta.addWidget(dot)

        date = QLabel("Oct 12, 2023")
        date.setStyleSheet("color: #414751; font-size: 12px;")
        meta.addWidget(date)

        meta.addStretch()

        header.addLayout(meta)

        page_layout.addLayout(header)

        # Content columns
        content = QHBoxLayout()
        content.setSpacing(48)

        # Left column
        left_col = QVBoxLayout()
        left_col.setSpacing(24)

        section1 = QVBoxLayout()
        section1.setSpacing(8)

        section1_title = QLabel("01. MARKET POSITION")
        section1_title.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: 700;
                color: #004f8f;
                letter-spacing: 0.1em;
            }
        """)
        section1.addWidget(section1_title)

        section1_text = QLabel(
            "Analyzing the current shift in consumer digital adoption patterns within the North American sector. Focused on the transition from traditional media consumption to integrated experiential platforms."
        )
        section1_text.setStyleSheet("color: #414751; font-size: 14px; line-height: 1.6;")
        section1_text.setWordWrap(True)
        section1.addWidget(section1_text)

        left_col.addLayout(section1)

        section2 = QVBoxLayout()
        section2.setSpacing(8)

        section2_title = QLabel("02. INFRASTRUCTURE")
        section2_title.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: 700;
                color: #004f8f;
                letter-spacing: 0.1em;
            }
        """)
        section2.addWidget(section2_title)

        section2_text = QLabel(
            "Scaling the core architecture to support high-fidelity real-time rendering and collaborative editing modules for global teams across varying bandwidth constraints."
        )
        section2_text.setStyleSheet("color: #414751; font-size: 14px; line-height: 1.6;")
        section2_text.setWordWrap(True)
        section2.addWidget(section2_text)

        left_col.addLayout(section2)

        # Image placeholder
        image_placeholder = QFrame()
        image_placeholder.setFixedHeight(150)
        image_placeholder.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a365d, stop:1 #004f8f);
                border-radius: 8px;
            }
        """)
        image_label = QLabel("📊 Data Visualization")
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 14px;")
        image_placeholder.setLayout(QVBoxLayout())
        image_placeholder.layout().addWidget(image_label)
        left_col.addWidget(image_placeholder)

        content.addLayout(left_col, 1)

        # Right column
        right_col = QVBoxLayout()
        right_col.setSpacing(24)

        # Executive summary box
        summary_box = QFrame()
        summary_box.setStyleSheet("""
            QFrame {
                background-color: #f0f4fc;
                border-left: 4px solid #004f8f;
                border-radius: 0 8px 8px 0;
                padding: 20px;
            }
        """)
        summary_layout = QVBoxLayout(summary_box)
        summary_layout.setSpacing(8)

        summary_title = QLabel("Executive Summary")
        summary_title.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        summary_title.setStyleSheet("color: #171c22;")
        summary_layout.addWidget(summary_title)

        summary_quote = QLabel(
            '"The 2024 roadmap prioritizes velocity without compromising the editorial integrity of the platform\'s core experience."'
        )
        summary_quote.setStyleSheet(
            "color: #414751; font-size: 13px; font-style: italic; line-height: 1.6;"
        )
        summary_quote.setWordWrap(True)
        summary_layout.addWidget(summary_quote)

        right_col.addWidget(summary_box)

        # Stats
        stats = QVBoxLayout()
        stats.setSpacing(12)

        for label, value in [
            ("Growth Projection", "+24%"),
            ("User Retention", "92.4%"),
            ("System Uptime", "99.99%"),
        ]:
            stat_row = QHBoxLayout()

            stat_label = QLabel(label)
            stat_label.setStyleSheet("color: #414751; font-size: 13px;")
            stat_row.addWidget(stat_label)

            stat_row.addStretch()

            stat_value = QLabel(value)
            stat_value.setStyleSheet("color: #004f8f; font-size: 20px; font-weight: 700;")
            stat_row.addWidget(stat_value)

            stats.addLayout(stat_row)

            divider = QFrame()
            divider.setFrameShape(QFrame.Shape.HLine)
            divider.setStyleSheet("background-color: #e2e8f0;")
            stats.addWidget(divider)

        right_col.addLayout(stats)

        # Key insight box
        insight_box = QFrame()
        insight_box.setStyleSheet("""
            QFrame {
                background-color: #171c22;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        insight_layout = QVBoxLayout(insight_box)
        insight_layout.setSpacing(12)

        insight_header = QHBoxLayout()
        insight_icon = QLabel("💡")
        insight_header.addWidget(insight_icon)

        insight_title = QLabel("KEY INSIGHT")
        insight_title.setStyleSheet(
            "color: white; font-size: 11px; font-weight: 700; letter-spacing: 0.1em;"
        )
        insight_header.addWidget(insight_title)

        insight_header.addStretch()
        insight_layout.addLayout(insight_header)

        insight_text = QLabel(
            "Leverage existing user behavioral data to automate content categorization through a hybrid ML-Editorial approach."
        )
        insight_text.setStyleSheet(
            "color: rgba(255, 255, 255, 0.8); font-size: 13px; line-height: 1.6;"
        )
        insight_text.setWordWrap(True)
        insight_layout.addWidget(insight_text)

        right_col.addWidget(insight_box)

        content.addLayout(right_col, 1)

        page_layout.addLayout(content)

        # Footer
        footer = QHBoxLayout()
        footer.setSpacing(24)

        footer_left = QLabel("Proprietary Editorial Data")
        footer_left.setStyleSheet(
            "color: #c1c7d3; font-size: 10px; font-weight: 700; letter-spacing: 0.1em;"
        )
        footer.addWidget(footer_left)

        footer.addStretch()

        footer_right = QLabel("Page 01 of 12")
        footer_right.setStyleSheet(
            "color: #c1c7d3; font-size: 10px; font-weight: 700; letter-spacing: 0.1em;"
        )
        footer.addWidget(footer_right)

        page_layout.addLayout(footer)

        layout.addWidget(pdf_page)


class EditingToolsPanel(QFrame):
    """Right side panel with editing tools"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setFixedWidth(280)
        self.setStyleSheet("background-color: #f7f9ff;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(24)

        # Header
        header = QHBoxLayout()

        title = QLabel("Editing Tools")
        title.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #171c22;")
        header.addWidget(title)

        header.addStretch()

        settings_icon = QLabel("⚙️")
        settings_icon.setStyleSheet("font-size: 18px; color: #414751;")
        settings_icon.setCursor(Qt.CursorShape.PointingHandCursor)
        header.addWidget(settings_icon)

        layout.addLayout(header)

        # Tools grid
        tools_grid = QFrame()
        tools_grid.setStyleSheet("""
            QFrame {
                background-color: #f0f4fc;
                border-radius: 12px;
                padding: 12px;
            }
        """)
        grid_layout = QVBoxLayout(tools_grid)
        grid_layout.setSpacing(8)

        # Row 1
        row1 = QHBoxLayout()
        row1.setSpacing(8)

        row1.addWidget(self.create_tool_btn("Tt", "ADD TEXT"))
        row1.addWidget(self.create_tool_btn("✍️", "SIGN PDF"))

        grid_layout.addLayout(row1)

        # Row 2
        row2 = QHBoxLayout()
        row2.setSpacing(8)

        row2.addWidget(self.create_tool_btn("🖌️", "REDACT"))
        row2.addWidget(self.create_tool_btn("📄", "MERGE"))

        grid_layout.addLayout(row2)

        layout.addWidget(tools_grid)

        # Comments section
        comments_header = QHBoxLayout()

        comments_title = QLabel("RECENT COMMENTS")
        comments_title.setStyleSheet(
            "font-size: 11px; font-weight: 700; color: #414751; letter-spacing: 0.1em;"
        )
        comments_header.addWidget(comments_title)

        comments_badge = QLabel("3")
        comments_badge.setStyleSheet("""
            QLabel {
                background-color: #004f8f;
                color: white;
                font-size: 10px;
                font-weight: 700;
                padding: 2px 8px;
                border-radius: 4px;
            }
        """)
        comments_header.addWidget(comments_badge)

        layout.addLayout(comments_header)

        # Comment items
        layout.addWidget(
            self.create_comment_item(
                "JD",
                "Jane Doe",
                "2m ago",
                "Update the growth projection figure. The Q3 report shows a higher trend.",
                True,
            )
        )

        layout.addWidget(
            self.create_comment_item(
                "MK",
                "Marcus King",
                "1h ago",
                "Check typography consistency on footer page numbers.",
                False,
            )
        )

        layout.addStretch()

        # Metrics
        metrics = QFrame()
        metrics.setStyleSheet("""
            QFrame {
                background-color: #f0f4fc;
                border-radius: 12px;
                padding: 16px;
            }
        """)
        metrics_layout = QVBoxLayout(metrics)
        metrics_layout.setSpacing(12)

        metrics_header = QHBoxLayout()
        metrics_icon = QLabel("ℹ️")
        metrics_header.addWidget(metrics_icon)

        metrics_title = QLabel("DOCUMENT METRICS")
        metrics_title.setStyleSheet(
            "font-size: 11px; font-weight: 700; color: #414751; letter-spacing: 0.1em;"
        )
        metrics_header.addWidget(metrics_title)

        metrics_header.addStretch()
        metrics_layout.addLayout(metrics_header)

        for label, value in [
            ("File Size", "4.2 MB"),
            ("Version", "2.4.1"),
            ("Readability Score", "High"),
        ]:
            row = QHBoxLayout()

            row_label = QLabel(label)
            row_label.setStyleSheet("color: #414751; font-size: 12px; opacity: 0.6;")
            row.addWidget(row_label)

            row.addStretch()

            row_value = QLabel(value)
            if label == "Readability Score":
                row_value.setStyleSheet("color: #004f8f; font-size: 12px; font-weight: 600;")
            else:
                row_value.setStyleSheet("color: #171c22; font-size: 12px; font-weight: 600;")
            row.addWidget(row_value)

            metrics_layout.addLayout(row)

        layout.addWidget(metrics)

    def create_tool_btn(self, icon, text):
        btn = QFrame()
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 16px;
            }
            QFrame:hover {
                background-color: #f7f9ff;
            }
        """)

        layout = QVBoxLayout(btn)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(8)

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(icon_label)

        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setStyleSheet(
            "font-size: 10px; font-weight: 700; color: #414751; letter-spacing: 0.05em;"
        )
        layout.addWidget(text_label)

        return btn

    def create_comment_item(self, initials, name, time, text, highlighted=False):
        item = QFrame()

        if highlighted:
            item.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 12px;
                    border-left: 3px solid #004f8f;
                    padding: 16px;
                }
            """)
        else:
            item.setStyleSheet("""
                QFrame {
                    background-color: transparent;
                    border-radius: 12px;
                    padding: 16px;
                }
                QFrame:hover {
                    background-color: #f0f4fc;
                }
            """)

        layout = QVBoxLayout(item)
        layout.setSpacing(8)

        header = QHBoxLayout()

        avatar = QLabel(initials)
        avatar.setFixedSize(24, 24)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("""
            QLabel {
                background-color: #eaeef6;
                border-radius: 12px;
                font-size: 10px;
                font-weight: 700;
                color: #414751;
            }
        """)
        header.addWidget(avatar)

        name_label = QLabel(name)
        name_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #171c22;")
        header.addWidget(name_label)

        header.addStretch()

        time_label = QLabel(time)
        time_label.setStyleSheet("font-size: 11px; color: #c1c7d3;")
        header.addWidget(time_label)

        layout.addLayout(header)

        comment_text = QLabel(text)
        comment_text.setStyleSheet("font-size: 13px; color: #414751; line-height: 1.5;")
        comment_text.setWordWrap(True)
        layout.addWidget(comment_text)

        return item


class PDFEditor(QWidget):
    """PDF Editor page - Image 8 from design"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: #f7f9ff;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Toolbar
        toolbar_container = QFrame()
        toolbar_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-bottom: 1px solid #eaeef6;
            }
        """)
        toolbar_layout = QVBoxLayout(toolbar_container)
        toolbar_layout.setContentsMargins(24, 12, 24, 12)
        toolbar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        toolbar = EditorToolbar()
        toolbar_layout.addWidget(toolbar)

        main_layout.addWidget(toolbar_container)

        # Content splitter
        content = QSplitter(Qt.Orientation.Horizontal)
        content.setStyleSheet("""
            QSplitter::handle {
                background-color: #eaeef6;
                width: 1px;
            }
        """)

        # Document viewer
        viewer = DocumentViewer()
        content.addWidget(viewer)

        # Right panel
        panel = EditingToolsPanel()
        content.addWidget(panel)

        content.setStretchFactor(0, 3)
        content.setStretchFactor(1, 1)

        main_layout.addWidget(content, 1)
