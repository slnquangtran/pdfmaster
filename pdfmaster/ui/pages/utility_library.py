"""
Utility Library Page for PDF Master
Based on Editorial Workspace design - Image 4
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
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont


class ToolCard(QFrame):
    """Tool card component for utility library"""

    def __init__(
        self, icon, title, description, badge=None, icon_bg="#004f8f", large=False, parent=None
    ):
        super().__init__(parent)
        self.setup_ui(icon, title, description, badge, icon_bg, large)

    def setup_ui(self, icon, title, description, badge, icon_bg, large):
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        if large:
            self.setMinimumHeight(280)
            self.setStyleSheet("""
                QFrame {
                    background-color: #f0f4fc;
                    border-radius: 16px;
                    padding: 28px;
                }
                QFrame:hover {
                    background-color: #eaeef6;
                }
            """)
        else:
            self.setMinimumHeight(200)
            self.setStyleSheet("""
                QFrame {
                    background-color: #f0f4fc;
                    border-radius: 16px;
                    padding: 24px;
                }
                QFrame:hover {
                    background-color: #eaeef6;
                }
            """)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        # Icon and badge row
        top_row = QHBoxLayout()

        icon_container = QFrame()
        icon_container.setFixedSize(48, 48)
        icon_container.setStyleSheet(f"""
            QFrame {{
                background-color: {icon_bg};
                border-radius: 12px;
            }}
        """)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 24px; color: white;")
        icon_layout.addWidget(icon_label)

        top_row.addWidget(icon_container)

        top_row.addStretch()

        if badge:
            badge_label = QLabel(badge)
            badge_label.setStyleSheet("""
                QLabel {
                    background-color: #004f8f15;
                    color: #004f8f;
                    padding: 4px 10px;
                    border-radius: 4px;
                    font-size: 10px;
                    font-weight: 700;
                    letter-spacing: 0.05em;
                }
            """)
            top_row.addWidget(badge_label)

        layout.addLayout(top_row)

        if large:
            layout.addStretch()

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Inter", 18 if large else 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #171c22;")
        layout.addWidget(title_label)

        # Description
        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #414751; font-size: 14px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        if not large:
            layout.addStretch()


class UtilityLibrary(QWidget):
    """Utility Library page - Image 4 from design"""

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
        main_layout.setSpacing(40)

        # Header
        title = QLabel("Utility Library")
        title.setFont(QFont("Inter", 36, QFont.Weight.Bold))
        title.setStyleSheet("color: #171c22; letter-spacing: -0.02em;")
        main_layout.addWidget(title)

        subtitle = QLabel(
            "A high-precision workspace for your digital archives. Manage, convert, and protect your PDF assets with surgical accuracy."
        )
        subtitle.setStyleSheet("color: #414751; font-size: 16px;")
        subtitle.setWordWrap(True)
        main_layout.addWidget(subtitle)

        # Conversion Studio Section
        conversion_section = self.create_section("WORKFLOW ALPHA", "Conversion Studio")
        main_layout.addLayout(conversion_section)

        # Conversion grid
        conv_grid = QHBoxLayout()
        conv_grid.setSpacing(20)

        # Main card
        main_conv = ToolCard(
            "📄",
            "Multi-Format to PDF",
            "Batch convert Word, Excel, and PowerPoint files into high-fidelity PDF documents without losing layout integrity.",
            "MOST POPULAR",
            "#004f8f",
            True,
        )
        conv_grid.addWidget(main_conv, 2)

        # Side cards
        side_container = QVBoxLayout()
        side_container.setSpacing(20)

        extract_card = ToolCard(
            "🖼️",
            "Extract Images",
            "Pull high-resolution assets from any PDF instantly.",
            None,
            "#494e55",
        )
        side_container.addWidget(extract_card)

        conv_grid.addLayout(side_container, 1)

        main_layout.addLayout(conv_grid)

        # Small cards row
        small_conv_grid = QHBoxLayout()
        small_conv_grid.setSpacing(20)

        html_card = ToolCard(
            "HTML", "HTML Export", "Transform documents into responsive web pages.", None, "#494e55"
        )
        small_conv_grid.addWidget(html_card)

        text_card = ToolCard(
            "📝", "PDF to Text", "OCR-powered extraction for raw text analysis.", None, "#494e55"
        )
        small_conv_grid.addWidget(text_card)

        small_conv_grid.addStretch()

        main_layout.addLayout(small_conv_grid)

        # Management Suite Section
        mgmt_section = self.create_section("ORGANIZATION BETA", "Management Suite")
        main_layout.addLayout(mgmt_section)

        # Management grid
        mgmt_grid = QHBoxLayout()
        mgmt_grid.setSpacing(20)

        # Merger card (large)
        merger_widget = QFrame()
        merger_widget.setMinimumHeight(200)
        merger_widget.setStyleSheet("""
            QFrame {
                background-color: #f0f4fc;
                border-radius: 16px;
                padding: 24px;
            }
            QFrame:hover {
                background-color: #eaeef6;
            }
        """)
        merger_widget.setCursor(Qt.CursorShape.PointingHandCursor)

        merger_layout = QVBoxLayout(merger_widget)
        merger_layout.setSpacing(12)

        merger_title = QLabel("Smart Merger")
        merger_title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        merger_title.setStyleSheet("color: #171c22;")
        merger_layout.addWidget(merger_title)

        merger_desc = QLabel(
            "Combine thousands of pages with automatic table-of-contents generation and page numbering."
        )
        merger_desc.setStyleSheet("color: #414751; font-size: 14px;")
        merger_desc.setWordWrap(True)
        merger_layout.addWidget(merger_desc)

        merger_layout.addStretch()

        mgmt_grid.addWidget(merger_widget, 2)

        split_card = ToolCard("✂️", "Document Split", "Surgical page extraction.", None, "#006e2c")
        mgmt_grid.addWidget(split_card, 1)

        compress_card = ToolCard("🗜️", "Compress", "80% size reduction.", None, "#006e2c")
        mgmt_grid.addWidget(compress_card, 1)

        main_layout.addLayout(mgmt_grid)

        # Vault & Privacy Section
        vault_section = self.create_section("SECURITY GAMMA", "Vault & Privacy")
        main_layout.addLayout(vault_section)

        # Vault grid
        vault_grid = QHBoxLayout()
        vault_grid.setSpacing(20)

        encryption_card = QFrame()
        encryption_card.setMinimumHeight(220)
        encryption_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                padding: 24px;
                border: 1px solid #e2e8f0;
            }
            QFrame:hover {
                box-shadow: 0 12px 40px rgba(23, 28, 34, 0.06);
            }
        """)
        encryption_card.setCursor(Qt.CursorShape.PointingHandCursor)

        enc_layout = QVBoxLayout(encryption_card)
        enc_layout.setSpacing(16)

        enc_icon = QLabel("🔒")
        enc_icon.setFixedSize(48, 48)
        enc_icon.setStyleSheet("""
            QLabel {
                background-color: #171c22;
                color: white;
                border-radius: 12px;
                font-size: 24px;
            }
        """)
        enc_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        enc_layout.addWidget(enc_icon)

        enc_title = QLabel("AES-256 Encryption")
        enc_title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        enc_title.setStyleSheet("color: #171c22;")
        enc_layout.addWidget(enc_title)

        enc_desc = QLabel(
            "Military-grade protection for sensitive corporate archives. Local-first encryption keys."
        )
        enc_desc.setStyleSheet("color: #414751; font-size: 14px;")
        enc_desc.setWordWrap(True)
        enc_layout.addWidget(enc_desc)

        vault_grid.addWidget(encryption_card)

        signature_card = ToolCard(
            "✍️",
            "Digital Signature",
            "Legally binding e-signatures with comprehensive audit trails and timestamping.",
            None,
            "#494e55",
        )
        signature_card.setStyleSheet("""
            QFrame {
                background-color: #f0f4fc;
                border-radius: 16px;
                padding: 24px;
            }
            QFrame:hover {
                background-color: #eaeef6;
            }
        """)
        vault_grid.addWidget(signature_card)

        redaction_card = ToolCard(
            "🖌️",
            "Redaction Tool",
            "Permanently scrub PII and sensitive data before sharing with external parties.",
            None,
            "#494e55",
        )
        redaction_card.setStyleSheet("""
            QFrame {
                background-color: #f0f4fc;
                border-radius: 16px;
                padding: 24px;
            }
            QFrame:hover {
                background-color: #eaeef6;
            }
        """)
        vault_grid.addWidget(redaction_card)

        main_layout.addLayout(vault_grid)

        # Footer
        footer = self.create_footer()
        main_layout.addLayout(footer)

        main_layout.addStretch()

        scroll.setWidget(content)

        # Main layout
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(scroll)

    def create_section(self, badge_text, title_text):
        """Create a section header"""
        layout = QVBoxLayout()
        layout.setSpacing(8)

        badge = QLabel(badge_text)
        badge.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: 700;
                color: #004f8f;
                letter-spacing: 0.15em;
            }
        """)
        layout.addWidget(badge)

        title_row = QHBoxLayout()

        title = QLabel(title_text)
        title.setFont(QFont("Inter", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #171c22;")
        title_row.addWidget(title)

        # Divider line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #eaeef6; max-height: 1px;")
        title_row.addWidget(line, 1)

        layout.addLayout(title_row)

        return layout

    def create_footer(self):
        """Create footer section"""
        layout = QVBoxLayout()
        layout.setSpacing(24)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #eaeef6; max-height: 1px;")
        layout.addWidget(line)

        footer_content = QHBoxLayout()

        # Brand
        brand = QVBoxLayout()
        brand.setSpacing(8)

        brand_name = QLabel("Editorial System v4.2")
        brand_name.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        brand_name.setStyleSheet("color: #171c22;")
        brand.addWidget(brand_name)

        brand_desc = QLabel(
            "Designed for the digital curator. Precision tools for high-stakes documentation management."
        )
        brand_desc.setStyleSheet("color: #414751; font-size: 14px;")
        brand.addWidget(brand_desc)

        footer_content.addLayout(brand, 1)

        # Links
        links_layout = QHBoxLayout()
        links_layout.setSpacing(48)

        resources = QVBoxLayout()
        resources.setSpacing(12)

        resources_title = QLabel("Resources")
        resources_title.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        resources_title.setStyleSheet("color: #171c22;")
        resources.addWidget(resources_title)

        for text in ["API Documentation", "Enterprise Licensing", "Security Whitepaper"]:
            link = QLabel(text)
            link.setStyleSheet("""
                QLabel {
                    color: #414751;
                    font-size: 14px;
                }
                QLabel:hover {
                    color: #004f8f;
                }
            """)
            link.setCursor(Qt.CursorShape.PointingHandCursor)
            resources.addWidget(link)

        links_layout.addLayout(resources)

        legal = QVBoxLayout()
        legal.setSpacing(12)

        legal_title = QLabel("Legal")
        legal_title.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        legal_title.setStyleSheet("color: #171c22;")
        legal.addWidget(legal_title)

        for text in ["Privacy Policy", "Terms of Service", "Data Processing"]:
            link = QLabel(text)
            link.setStyleSheet("""
                QLabel {
                    color: #414751;
                    font-size: 14px;
                }
                QLabel:hover {
                    color: #004f8f;
                }
            """)
            link.setCursor(Qt.CursorShape.PointingHandCursor)
            legal.addWidget(link)

        links_layout.addLayout(legal)

        footer_content.addLayout(links_layout)

        layout.addLayout(footer_content)

        return layout
