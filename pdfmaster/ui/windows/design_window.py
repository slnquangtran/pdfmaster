"""
PDF Design Window - GUI for PDF design operations
"""

import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QProgressBar,
    QLineEdit,
    QGroupBox,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox,
    QColorDialog,
    QTabWidget,
    QGridLayout,
    QScrollArea,
    QFrame,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor

from pdfmaster.src.design.designer import DocumentDesigner, DesignResult
from pdfmaster.src.design.decorators.watermark import WatermarkType
from pdfmaster.src.design.decorators.stamp import StampCategory, StampShape
from pdfmaster.src.design.decorators.page_numbers import PageNumberPosition, PageNumberFormat


class DesignWorker(QThread):
    """Worker thread for design operations"""

    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str, str)  # success, message, output_path

    def __init__(self, operation: str, input_path: str, output_path: str, **kwargs):
        super().__init__()
        self.operation = operation
        self.input_path = input_path
        self.output_path = output_path
        self.kwargs = kwargs

    def run(self):
        try:
            designer = DocumentDesigner(self.input_path)

            if self.operation == "watermark":
                result = designer.add_watermark(**self.kwargs)
            elif self.operation == "stamp":
                result = designer.add_stamp(**self.kwargs)
            elif self.operation == "custom_stamp":
                result = designer.add_custom_stamp(**self.kwargs)
            elif self.operation == "page_numbers":
                result = designer.add_page_numbers(**self.kwargs)
            elif self.operation == "custom_page_numbers":
                result = designer.add_custom_page_numbers(**self.kwargs)
            elif self.operation == "header_footer":
                result = designer.add_header_footer(**self.kwargs)
            elif self.operation == "header_logo":
                result = designer.add_header_with_logo(**self.kwargs)
            elif self.operation == "toc":
                result = designer.generate_toc(**self.kwargs)
            elif self.operation == "bookmarks":
                result = designer.add_bookmarks(**self.kwargs)
            else:
                result = DesignResult(False, f"Unknown operation: {self.operation}")

            if result.success:
                output = designer.save(self.output_path)
                designer.close()
                self.finished.emit(True, result.message, str(output))
            else:
                self.finished.emit(False, result.message, "")

        except Exception as e:
            self.finished.emit(False, str(e), "")


class ColorButton(QPushButton):
    """Button that opens color picker"""

    colorChanged = pyqtSignal(QColor)

    def __init__(self, color: QColor = QColor(0, 0, 0)):
        super().__init__()
        self._color = color
        self.setFixedSize(40, 25)
        self.update_button_color()
        self.clicked.connect(self.pick_color)

    def update_button_color(self):
        self.setStyleSheet(f"background-color: {self._color.name()}; border: 1px solid #ccc;")

    def pick_color(self):
        color = QColorDialog.getColor(self._color, self, "Select Color")
        if color.isValid():
            self._color = color
            self.update_button_color()
            self.colorChanged.emit(color)

    def get_color(self) -> tuple:
        return (self._color.red(), self._color.green(), self._color.blue())


class DesignWindow(QWidget):
    """Window for PDF design operations"""

    def __init__(self):
        super().__init__()
        self.worker: Optional[DesignWorker] = None
        self.input_path: Optional[str] = None
        self.output_path: Optional[str] = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        self.setLayout(main_layout)

        # File selection
        file_group = QGroupBox("PDF File")
        file_group.setObjectName("fileGroup")
        file_layout = QHBoxLayout()
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)

        self.file_input = QLineEdit()
        self.file_input.setObjectName("inputField")
        self.file_input.setPlaceholderText("Select a PDF file to design...")
        self.file_input.setReadOnly(True)
        file_layout.addWidget(self.file_input, 1)

        browse_btn = QPushButton("📂 Browse")
        browse_btn.setObjectName("secondaryButton")
        browse_btn.setProperty("secondary", True)
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)

        # Info label
        self.info_label = QLabel("")
        self.info_label.setObjectName("infoLabel")
        main_layout.addWidget(self.info_label)

        # Tabs for different operations
        self.tabs = QTabWidget()
        self.tabs.setObjectName("designTabs")
        main_layout.addWidget(self.tabs, 1)

        # Create tabs
        self.watermark_tab = self._create_watermark_tab()
        self.tabs.addTab(self.watermark_tab, "💧 Watermark")

        self.stamp_tab = self._create_stamp_tab()
        self.tabs.addTab(self.stamp_tab, "📌 Stamps")

        self.page_number_tab = self._create_page_number_tab()
        self.tabs.addTab(self.page_number_tab, "#️⃣ Page Numbers")

        self.header_footer_tab = self._create_header_footer_tab()
        self.tabs.addTab(self.header_footer_tab, "📄 Header/Footer")

        self.structure_tab = self._create_structure_tab()
        self.tabs.addTab(self.structure_tab, "📑 Structure")

        # Progress
        self.progress = QProgressBar()
        self.progress.setObjectName("progressBar")
        self.progress.setVisible(False)
        main_layout.addWidget(self.progress)

        # Status
        self.status_label = QLabel("💡 Select a PDF file and choose a design operation")
        self.status_label.setObjectName("statusLabel")
        main_layout.addWidget(self.status_label)

        # Apply button
        self.apply_btn = QPushButton("✨ Apply Design")
        self.apply_btn.setObjectName("primaryButton")
        self.apply_btn.clicked.connect(self.apply_design)
        self.apply_btn.setEnabled(False)
        main_layout.addWidget(self.apply_btn)

    def _create_watermark_tab(self) -> QWidget:
        tab = QWidget()
        layout = QGridLayout()
        layout.setSpacing(10)
        tab.setLayout(layout)

        # Watermark type
        layout.addWidget(QLabel("Type:"), 0, 0)
        self.wm_type = QComboBox()
        self.wm_type.addItems(["Diagonal Text", "Centered Text", "Tiled", "Image"])
        layout.addWidget(self.wm_type, 0, 1, 1, 2)

        # Text
        layout.addWidget(QLabel("Text:"), 1, 0)
        self.wm_text = QLineEdit("DRAFT")
        layout.addWidget(self.wm_text, 1, 1, 1, 2)

        # Font size
        layout.addWidget(QLabel("Font Size:"), 2, 0)
        self.wm_font_size = QSpinBox()
        self.wm_font_size.setRange(8, 200)
        self.wm_font_size.setValue(48)
        layout.addWidget(self.wm_font_size, 2, 1)

        # Color
        layout.addWidget(QLabel("Color:"), 3, 0)
        self.wm_color = ColorButton(QColor(192, 192, 192))
        layout.addWidget(self.wm_color, 3, 1)

        # Opacity
        layout.addWidget(QLabel("Opacity:"), 4, 0)
        self.wm_opacity = QDoubleSpinBox()
        self.wm_opacity.setRange(0.05, 1.0)
        self.wm_opacity.setSingleStep(0.05)
        self.wm_opacity.setValue(0.3)
        layout.addWidget(self.wm_opacity, 4, 1)

        # Rotation
        layout.addWidget(QLabel("Rotation:"), 5, 0)
        self.wm_rotation = QSpinBox()
        self.wm_rotation.setRange(-90, 90)
        self.wm_rotation.setValue(45)
        layout.addWidget(self.wm_rotation, 5, 1)

        layout.setRowStretch(6, 1)

        return tab

    def _create_stamp_tab(self) -> QWidget:
        tab = QWidget()
        layout = QGridLayout()
        layout.setSpacing(10)
        tab.setLayout(layout)

        # Category
        layout.addWidget(QLabel("Category:"), 0, 0)
        self.stamp_category = QComboBox()
        self.stamp_category.addItems(["Approval", "Status", "Custom"])
        layout.addWidget(self.stamp_category, 0, 1, 1, 2)

        # Stamp type
        layout.addWidget(QLabel("Stamp:"), 1, 0)
        self.stamp_type = QComboBox()
        self.stamp_type.addItems(["APPROVED", "REJECTED", "PENDING", "DRAFT", "FINAL"])
        layout.addWidget(self.stamp_type, 1, 1, 1, 2)

        # Custom text (for custom category)
        layout.addWidget(QLabel("Custom Text:"), 2, 0)
        self.stamp_custom_text = QLineEdit()
        self.stamp_custom_text.setPlaceholderText("Enter custom stamp text")
        layout.addWidget(self.stamp_custom_text, 2, 1, 1, 2)

        # Shape
        layout.addWidget(QLabel("Shape:"), 3, 0)
        self.stamp_shape = QComboBox()
        self.stamp_shape.addItems(["Rectangle", "Oval", "Circle"])
        layout.addWidget(self.stamp_shape, 3, 1)

        # Size
        layout.addWidget(QLabel("Width:"), 4, 0)
        self.stamp_width = QSpinBox()
        self.stamp_width.setRange(50, 300)
        self.stamp_width.setValue(150)
        layout.addWidget(self.stamp_width, 4, 1)

        layout.addWidget(QLabel("Height:"), 5, 0)
        self.stamp_height = QSpinBox()
        self.stamp_height.setRange(30, 200)
        self.stamp_height.setValue(60)
        layout.addWidget(self.stamp_height, 5, 1)

        # Rotation
        layout.addWidget(QLabel("Rotation:"), 6, 0)
        self.stamp_rotation = QSpinBox()
        self.stamp_rotation.setRange(-45, 45)
        self.stamp_rotation.setValue(-15)
        layout.addWidget(self.stamp_rotation, 6, 1)

        layout.setRowStretch(7, 1)

        return tab

    def _create_page_number_tab(self) -> QWidget:
        tab = QWidget()
        layout = QGridLayout()
        layout.setSpacing(10)
        tab.setLayout(layout)

        # Format
        layout.addWidget(QLabel("Format:"), 0, 0)
        self.pn_format = QComboBox()
        self.pn_format.addItems(
            ["Numeric (1, 2, 3)", "Roman (I, II, III)", "Alpha (A, B, C)", "Custom Template"]
        )
        layout.addWidget(self.pn_format, 0, 1, 1, 2)

        # Position
        layout.addWidget(QLabel("Position:"), 1, 0)
        self.pn_position = QComboBox()
        self.pn_position.addItems(
            ["Bottom Center", "Bottom Left", "Bottom Right", "Top Center", "Top Left", "Top Right"]
        )
        layout.addWidget(self.pn_position, 1, 1, 1, 2)

        # Custom template
        layout.addWidget(QLabel("Template:"), 2, 0)
        self.pn_template = QLineEdit("Page {number} of {total}")
        self.pn_template.setPlaceholderText("{number}, {total}, {prefix}, {suffix}")
        layout.addWidget(self.pn_template, 2, 1, 1, 2)

        # Font size
        layout.addWidget(QLabel("Font Size:"), 3, 0)
        self.pn_font_size = QSpinBox()
        self.pn_font_size.setRange(6, 24)
        self.pn_font_size.setValue(10)
        layout.addWidget(self.pn_font_size, 3, 1)

        # Color
        layout.addWidget(QLabel("Color:"), 4, 0)
        self.pn_color = ColorButton(QColor(0, 0, 0))
        layout.addWidget(self.pn_color, 4, 1)

        # Show total
        self.pn_show_total = QCheckBox("Show total pages")
        self.pn_show_total.setChecked(True)
        layout.addWidget(self.pn_show_total, 5, 0, 1, 2)

        layout.setRowStretch(6, 1)

        return tab

    def _create_header_footer_tab(self) -> QWidget:
        tab = QWidget()
        layout = QGridLayout()
        layout.setSpacing(10)
        tab.setLayout(layout)

        # Header title
        layout.addWidget(QLabel("Header Title:"), 0, 0)
        self.hf_header_title = QLineEdit()
        self.hf_header_title.setPlaceholderText("Document title for header")
        layout.addWidget(self.hf_header_title, 0, 1, 1, 2)

        # Footer text
        layout.addWidget(QLabel("Footer Text:"), 1, 0)
        self.hf_footer_text = QLineEdit()
        self.hf_footer_text.setPlaceholderText("Footer text")
        layout.addWidget(self.hf_footer_text, 1, 1, 1, 2)

        # Logo
        layout.addWidget(QLabel("Logo:"), 2, 0)
        self.hf_logo_path = QLineEdit()
        self.hf_logo_path.setPlaceholderText("Path to logo image")
        self.hf_logo_path.setReadOnly(True)
        layout.addWidget(self.hf_logo_path, 2, 1)

        browse_logo_btn = QPushButton("📂")
        browse_logo_btn.clicked.connect(self._browse_logo)
        layout.addWidget(browse_logo_btn, 2, 2)

        # Options
        self.hf_show_date = QCheckBox("Show date in header")
        self.hf_show_date.setChecked(True)
        layout.addWidget(self.hf_show_date, 3, 0, 1, 3)

        self.hf_show_line = QCheckBox("Show separator lines")
        self.hf_show_line.setChecked(True)
        layout.addWidget(self.hf_show_line, 4, 0, 1, 3)

        self.hf_skip_first = QCheckBox("Skip first page")
        self.hf_skip_first.setChecked(True)
        layout.addWidget(self.hf_skip_first, 5, 0, 1, 3)

        layout.setRowStretch(6, 1)

        return tab

    def _create_structure_tab(self) -> QWidget:
        tab = QWidget()
        layout = QGridLayout()
        layout.setSpacing(10)
        tab.setLayout(layout)

        # TOC
        toc_group = QGroupBox("Table of Contents")
        toc_layout = QGridLayout()
        toc_group.setLayout(toc_layout)
        layout.addWidget(toc_group, 0, 0, 1, 3)

        self.struct_toc_title = QLineEdit("Table of Contents")
        toc_layout.addWidget(QLabel("Title:"), 0, 0)
        toc_layout.addWidget(self.struct_toc_title, 0, 1)

        self.struct_toc_insert = QCheckBox("Insert TOC page")
        self.struct_toc_insert.setChecked(True)
        toc_layout.addWidget(self.struct_toc_insert, 1, 0, 1, 2)

        self.struct_toc_btn = QPushButton("📑 Generate TOC")
        self.struct_toc_btn.setObjectName("secondaryButton")
        self.struct_toc_btn.clicked.connect(lambda: self._apply_structure("toc"))
        toc_layout.addWidget(self.struct_toc_btn, 2, 0, 1, 2)

        # Bookmarks
        bm_group = QGroupBox("Bookmarks")
        bm_layout = QGridLayout()
        bm_group.setLayout(bm_layout)
        layout.addWidget(bm_group, 1, 0, 1, 3)

        self.struct_bm_entries = QLineEdit()
        self.struct_bm_entries.setPlaceholderText("Chapter1:1, Section1.1:3, Chapter2:5")
        bm_layout.addWidget(QLabel("Entries:"), 0, 0)
        bm_layout.addWidget(self.struct_bm_entries, 0, 1)

        self.struct_bm_btn = QPushButton("🔖 Add Bookmarks")
        self.struct_bm_btn.setObjectName("secondaryButton")
        self.struct_bm_btn.clicked.connect(lambda: self._apply_structure("bookmarks"))
        bm_layout.addWidget(self.struct_bm_btn, 1, 0, 1, 2)

        layout.setRowStretch(2, 1)

        return tab

    def _browse_logo(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Logo Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
        )
        if file_path:
            self.hf_logo_path.setText(file_path)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select PDF File", "", "PDF Files (*.pdf);;All Files (*)"
        )
        if file_path:
            self.input_path = file_path
            self.file_input.setText(file_path)

            # Update info
            try:
                designer = DocumentDesigner(file_path)
                info = designer.get_document_info()
                designer.close()
                self.info_label.setText(
                    f"📄 {Path(file_path).name} - {info.get('page_count', 0)} pages"
                )
                self.apply_btn.setEnabled(True)
            except Exception as e:
                self.info_label.setText(f"⚠️ Error: {str(e)}")
                self.apply_btn.setEnabled(False)

    def apply_design(self):
        if not self.input_path:
            QMessageBox.warning(self, "No File", "Please select a PDF file first.")
            return

        # Get output path
        default_name = Path(self.input_path).stem + "_designed.pdf"
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Designed PDF As",
            str(Path(self.input_path).parent / default_name),
            "PDF Files (*.pdf);;All Files (*)",
        )

        if not output_path:
            return

        self.output_path = output_path

        # Get current tab and build kwargs
        current_tab = self.tabs.currentIndex()

        if current_tab == 0:  # Watermark
            self._apply_watermark()
        elif current_tab == 1:  # Stamp
            self._apply_stamp()
        elif current_tab == 2:  # Page Numbers
            self._apply_page_numbers()
        elif current_tab == 3:  # Header/Footer
            self._apply_header_footer()

    def _apply_watermark(self):
        # Map UI values to enum
        type_map = {
            "Diagonal Text": WatermarkType.DIAGONAL,
            "Centered Text": WatermarkType.TEXT,
            "Tiled": WatermarkType.TILED,
            "Image": WatermarkType.IMAGE,
        }

        kwargs = {
            "text": self.wm_text.text(),
            "watermark_type": type_map.get(self.wm_type.currentText(), WatermarkType.DIAGONAL),
            "font_size": self.wm_font_size.value(),
            "color": self.wm_color.get_color(),
            "opacity": self.wm_opacity.value(),
            "rotation": self.wm_rotation.value(),
        }

        self._run_operation("watermark", kwargs)

    def _apply_stamp(self):
        # Map UI values
        category_map = {
            "Approval": StampCategory.APPROVAL,
            "Status": StampCategory.STATUS,
            "Custom": StampCategory.CUSTOM,
        }

        shape_map = {
            "Rectangle": StampShape.RECTANGLE,
            "Oval": StampShape.OVAL,
            "Circle": StampShape.CIRCLE,
        }

        kwargs = {
            "stamp_name": self.stamp_type.currentText(),
            "category": category_map.get(self.stamp_category.currentText(), StampCategory.APPROVAL),
            "shape": shape_map.get(self.stamp_shape.currentText(), StampShape.RECTANGLE),
            "rotation": self.stamp_rotation.value(),
        }

        if self.stamp_category.currentText() == "Custom" and self.stamp_custom_text.text():
            kwargs["stamp_name"] = self.stamp_custom_text.text()

        self._run_operation("stamp", kwargs)

    def _apply_page_numbers(self):
        position_map = {
            "Bottom Center": PageNumberPosition.BOTTOM_CENTER,
            "Bottom Left": PageNumberPosition.BOTTOM_LEFT,
            "Bottom Right": PageNumberPosition.BOTTOM_RIGHT,
            "Top Center": PageNumberPosition.TOP_CENTER,
            "Top Left": PageNumberPosition.TOP_LEFT,
            "Top Right": PageNumberPosition.TOP_RIGHT,
        }

        format_map = {
            "Numeric (1, 2, 3)": PageNumberFormat.NUMERIC,
            "Roman (I, II, III)": PageNumberFormat.ROMAN,
            "Alpha (A, B, C)": PageNumberFormat.ALPHA,
            "Custom Template": PageNumberFormat.CUSTOM,
        }

        if self.pn_format.currentText() == "Custom Template":
            operation = "custom_page_numbers"
            kwargs = {
                "template": self.pn_template.text(),
                "position": position_map.get(
                    self.pn_position.currentText(), PageNumberPosition.BOTTOM_CENTER
                ),
                "font_size": self.pn_font_size.value(),
                "color": self.pn_color.get_color(),
            }
        else:
            operation = "page_numbers"
            kwargs = {
                "position": position_map.get(
                    self.pn_position.currentText(), PageNumberPosition.BOTTOM_CENTER
                ),
                "number_format": format_map.get(
                    self.pn_format.currentText(), PageNumberFormat.NUMERIC
                ),
                "font_size": self.pn_font_size.value(),
                "color": self.pn_color.get_color(),
                "show_total": self.pn_show_total.isChecked(),
            }

        self._run_operation(operation, kwargs)

    def _apply_header_footer(self):
        kwargs = {
            "header_title": self.hf_header_title.text(),
            "footer_text": self.hf_footer_text.text(),
            "show_date": self.hf_show_date.isChecked(),
            "show_line": self.hf_show_line.isChecked(),
        }

        if self.hf_logo_path.text():
            operation = "header_logo"
            kwargs["logo_path"] = self.hf_logo_path.text()
        else:
            operation = "header_footer"

        self._run_operation(operation, kwargs)

    def _apply_structure(self, operation: str):
        if operation == "toc":
            kwargs = {
                "title": self.struct_toc_title.text(),
                "insert_toc_page": self.struct_toc_insert.isChecked(),
            }
        elif operation == "bookmarks":
            # Parse entries like "Chapter1:1, Section1.1:3"
            entries_str = self.struct_bm_entries.text()
            entries = []
            for item in entries_str.split(","):
                if ":" in item:
                    title, page = item.rsplit(":", 1)
                    try:
                        entries.append((title.strip(), int(page.strip())))
                    except ValueError:
                        pass
            kwargs = {"entries": entries}
        else:
            return

        self._run_operation(operation, kwargs)

    def _run_operation(self, operation: str, kwargs: dict):
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.status_label.setText(f"🔄 Applying {operation}...")
        self.apply_btn.setEnabled(False)

        self.worker = DesignWorker(operation, self.input_path, self.output_path, **kwargs)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _on_progress(self, percent: int, message: str):
        self.progress.setValue(percent)
        self.status_label.setText(f"🔄 {message}")

    def _on_finished(self, success: bool, message: str, output_path: str):
        self.progress.setVisible(False)
        self.apply_btn.setEnabled(True)

        if success:
            QMessageBox.information(self, "✅ Success", f"{message}\n\nSaved to:\n{output_path}")
            self.status_label.setText("✅ Design applied successfully")
        else:
            QMessageBox.critical(self, "❌ Error", f"Design failed:\n{message}")
            self.status_label.setText("❌ Design failed")
