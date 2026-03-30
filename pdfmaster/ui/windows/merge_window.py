"""
PDF Merge and Split Window

Provides a GUI for merging multiple PDFs and splitting PDFs
by page ranges or into individual pages.
"""

import sys
from pathlib import Path
from typing import Optional, List

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QMessageBox,
    QProgressBar,
    QLineEdit,
    QGroupBox,
    QTabWidget,
    QRadioButton,
    QButtonGroup,
    QSpinBox,
    QTextEdit,
    QComboBox,
    QCheckBox,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMimeData
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QDragMoveEvent

from pdfmaster.src.core.merger import PDFMerger, PDFSplitter, merge_pdfs, split_pdf


class MergeWorker(QThread):
    """Worker thread for PDF merge operations"""

    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str, str)  # success, message, output_path

    def __init__(self, files: List[str], output_path: str):
        super().__init__()
        self.files = files
        self.output_path = output_path

    def run(self):
        try:
            result = merge_pdfs(self.files, self.output_path, progress_callback=self._on_progress)
            self.finished.emit(True, "Merge completed successfully!", str(result))
        except Exception as e:
            self.finished.emit(False, str(e), "")

    def _on_progress(self, percent: int, message: str):
        self.progress.emit(percent, message)


class SplitWorker(QThread):
    """Worker thread for PDF split operations"""

    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str, object)  # success, message, result

    def __init__(self, input_path: str, output_path: str, mode: str, **kwargs):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.mode = mode
        self.kwargs = kwargs

    def run(self):
        try:
            result = split_pdf(
                self.input_path,
                self.output_path,
                progress_callback=self._on_progress,
                **self.kwargs,
            )
            if isinstance(result, list):
                msg = f"Created {len(result)} files"
            else:
                msg = "Split completed successfully!"
            self.finished.emit(True, msg, result)
        except Exception as e:
            self.finished.emit(False, str(e), None)

    def _on_progress(self, percent: int, message: str):
        self.progress.emit(percent, message)


class MergeFileListWidget(QListWidget):
    """Drag-and-drop enabled file list for merge operations"""

    files_dropped = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(".pdf"):
                files.append(file_path)
        if files:
            self.files_dropped.emit(files)
        event.acceptProposedAction()


class MergeWindow(QWidget):
    """Window for PDF merge and split operations"""

    def __init__(self):
        super().__init__()
        self.merge_worker: Optional[MergeWorker] = None
        self.split_worker: Optional[SplitWorker] = None
        self.merge_files: List[str] = []
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        self.setLayout(main_layout)

        # Tab widget for Merge/Split
        self.tabs = QTabWidget()
        self.tabs.setObjectName("mergeSplitTabs")
        main_layout.addWidget(self.tabs)

        # Create Merge tab
        self.merge_tab = self._create_merge_tab()
        self.tabs.addTab(self.merge_tab, "🔗 Merge PDFs")

        # Create Split tab
        self.split_tab = self._create_split_tab()
        self.tabs.addTab(self.split_tab, "✂️ Split PDF")

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setObjectName("progressBar")
        self.progress.setVisible(False)
        main_layout.addWidget(self.progress)

        # Status label
        self.status_label = QLabel("💡 Select operation to begin")
        self.status_label.setObjectName("statusLabel")
        main_layout.addWidget(self.status_label)

    def _create_merge_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        tab.setLayout(layout)

        # File selection group
        files_group = QGroupBox("PDF Files to Merge")
        files_group.setObjectName("filesGroup")
        files_layout = QVBoxLayout()
        files_group.setLayout(files_layout)
        layout.addWidget(files_group, 1)

        # Instructions
        instruction = QLabel("Drag and drop PDF files below, or click 'Add Files' to browse.")
        instruction.setObjectName("instructionLabel")
        instruction.setWordWrap(True)
        files_layout.addWidget(instruction)

        # File list
        self.merge_file_list = MergeFileListWidget()
        self.merge_file_list.setObjectName("fileList")
        self.merge_file_list.setMinimumHeight(200)
        self.merge_file_list.files_dropped.connect(self._add_merge_files)
        files_layout.addWidget(self.merge_file_list)

        # File list buttons
        list_buttons = QHBoxLayout()

        add_btn = QPushButton("➕ Add Files")
        add_btn.setObjectName("secondaryButton")
        add_btn.setProperty("secondary", True)
        add_btn.clicked.connect(self._browse_merge_files)
        list_buttons.addWidget(add_btn)

        remove_btn = QPushButton("❌ Remove Selected")
        remove_btn.setObjectName("secondaryButton")
        remove_btn.setProperty("secondary", True)
        remove_btn.clicked.connect(self._remove_merge_file)
        list_buttons.addWidget(remove_btn)

        clear_btn = QPushButton("🗑️ Clear All")
        clear_btn.setObjectName("secondaryButton")
        clear_btn.setProperty("secondary", True)
        clear_btn.clicked.connect(self._clear_merge_files)
        list_buttons.addWidget(clear_btn)

        list_buttons.addStretch()

        move_up_btn = QPushButton("⬆️ Move Up")
        move_up_btn.setObjectName("secondaryButton")
        move_up_btn.setProperty("secondary", True)
        move_up_btn.clicked.connect(self._move_merge_file_up)
        list_buttons.addWidget(move_up_btn)

        move_down_btn = QPushButton("⬇️ Move Down")
        move_down_btn.setObjectName("secondaryButton")
        move_down_btn.setProperty("secondary", True)
        move_down_btn.clicked.connect(self._move_merge_file_down)
        list_buttons.addWidget(move_down_btn)

        files_layout.addLayout(list_buttons)

        # Output settings
        output_group = QGroupBox("Output Settings")
        output_group.setObjectName("settingsGroup")
        output_layout = QHBoxLayout()
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        output_label = QLabel("Save to:")
        output_label.setObjectName("fieldLabel")
        output_layout.addWidget(output_label)

        self.merge_output_input = QLineEdit()
        self.merge_output_input.setObjectName("inputField")
        self.merge_output_input.setPlaceholderText("Choose output file location...")
        output_layout.addWidget(self.merge_output_input, 1)

        browse_output_btn = QPushButton("📂 Browse")
        browse_output_btn.setObjectName("secondaryButton")
        browse_output_btn.setProperty("secondary", True)
        browse_output_btn.clicked.connect(self._browse_merge_output)
        output_layout.addWidget(browse_output_btn)

        # Merge button
        merge_btn = QPushButton("🔗 Merge PDFs")
        merge_btn.setObjectName("primaryButton")
        merge_btn.clicked.connect(self._execute_merge)
        layout.addWidget(merge_btn)

        return tab

    def _create_split_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        tab.setLayout(layout)

        # File selection group
        file_group = QGroupBox("Select PDF to Split")
        file_group.setObjectName("fileGroup")
        file_layout = QHBoxLayout()
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        self.split_file_input = QLineEdit()
        self.split_file_input.setObjectName("inputField")
        self.split_file_input.setPlaceholderText("Select a PDF file...")
        self.split_file_input.setReadOnly(True)
        file_layout.addWidget(self.split_file_input, 1)

        browse_file_btn = QPushButton("📂 Browse")
        browse_file_btn.setObjectName("secondaryButton")
        browse_file_btn.setProperty("secondary", True)
        browse_file_btn.clicked.connect(self._browse_split_file)
        file_layout.addWidget(browse_file_btn)

        # File info label
        self.split_info_label = QLabel("")
        self.split_info_label.setObjectName("infoLabel")
        layout.addWidget(self.split_info_label)

        # Split mode group
        mode_group = QGroupBox("Split Mode")
        mode_group.setObjectName("modeGroup")
        mode_layout = QVBoxLayout()
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        # Split mode radio buttons
        self.mode_group = QButtonGroup()

        self.range_radio = QRadioButton("Split by page range")
        self.range_radio.setChecked(True)
        self.mode_group.addButton(self.range_radio, 0)
        mode_layout.addWidget(self.range_radio)

        # Page range options
        range_widget = QWidget()
        range_layout = QHBoxLayout()
        range_layout.setContentsMargins(30, 0, 0, 0)
        range_widget.setLayout(range_layout)
        mode_layout.addWidget(range_widget)

        range_label = QLabel("Pages:")
        range_label.setObjectName("fieldLabel")
        range_layout.addWidget(range_label)

        self.page_range_input = QLineEdit()
        self.page_range_input.setObjectName("inputField")
        self.page_range_input.setPlaceholderText("e.g., 1-5, 10-15, 20")
        range_layout.addWidget(self.page_range_input, 1)

        range_hint = QLabel("(1-5, 10-, -5, 1,3,5)")
        range_hint.setObjectName("hintLabel")
        range_layout.addWidget(range_hint)

        self.individual_radio = QRadioButton("Split into individual pages")
        self.mode_group.addButton(self.individual_radio, 1)
        mode_layout.addWidget(self.individual_radio)

        self.chunk_radio = QRadioButton("Split every N pages")
        self.mode_group.addButton(self.chunk_radio, 2)
        mode_layout.addWidget(self.chunk_radio)

        # Chunk size option
        chunk_widget = QWidget()
        chunk_layout = QHBoxLayout()
        chunk_layout.setContentsMargins(30, 0, 0, 0)
        chunk_widget.setLayout(chunk_layout)
        chunk_widget.setVisible(False)
        mode_layout.addWidget(chunk_widget)

        chunk_label = QLabel("Pages per file:")
        chunk_label.setObjectName("fieldLabel")
        chunk_layout.addWidget(chunk_label)

        self.chunk_size_spin = QSpinBox()
        self.chunk_size_spin.setMinimum(1)
        self.chunk_size_spin.setMaximum(9999)
        self.chunk_size_spin.setValue(10)
        chunk_layout.addWidget(self.chunk_size_spin)

        chunk_layout.addStretch()

        # Connect radio buttons to show/hide options
        self.range_radio.toggled.connect(lambda checked: range_widget.setVisible(checked))
        self.chunk_radio.toggled.connect(lambda checked: chunk_widget.setVisible(checked))

        # Output settings
        output_group = QGroupBox("Output Settings")
        output_group.setObjectName("settingsGroup")
        output_layout = QHBoxLayout()
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        output_label = QLabel("Save to:")
        output_label.setObjectName("fieldLabel")
        output_layout.addWidget(output_label)

        self.split_output_input = QLineEdit()
        self.split_output_input.setObjectName("inputField")
        self.split_output_input.setPlaceholderText("Choose output location...")
        output_layout.addWidget(self.split_output_input, 1)

        browse_output_btn = QPushButton("📂 Browse")
        browse_output_btn.setObjectName("secondaryButton")
        browse_output_btn.setProperty("secondary", True)
        browse_output_btn.clicked.connect(self._browse_split_output)
        output_layout.addWidget(browse_output_btn)

        # Split button
        split_btn = QPushButton("✂️ Split PDF")
        split_btn.setObjectName("primaryButton")
        split_btn.clicked.connect(self._execute_split)
        layout.addWidget(split_btn)

        return tab

    # Merge operations
    def _browse_merge_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select PDF Files to Merge", "", "PDF Files (*.pdf);;All Files (*)"
        )
        if files:
            self._add_merge_files(files)

    def _add_merge_files(self, files: List[str]):
        for file_path in files:
            if file_path not in self.merge_files:
                self.merge_files.append(file_path)
                item = QListWidgetItem(f"📄 {Path(file_path).name}")
                item.setToolTip(file_path)
                self.merge_file_list.addItem(item)
        self._update_merge_status()

    def _remove_merge_file(self):
        for item in self.merge_file_list.selectedItems():
            row = self.merge_file_list.row(item)
            self.merge_file_list.takeItem(row)
            self.merge_files.pop(row)
        self._update_merge_status()

    def _clear_merge_files(self):
        self.merge_files.clear()
        self.merge_file_list.clear()
        self._update_merge_status()

    def _move_merge_file_up(self):
        current_row = self.merge_file_list.currentRow()
        if current_row > 0:
            # Swap in list
            self.merge_files[current_row], self.merge_files[current_row - 1] = (
                self.merge_files[current_row - 1],
                self.merge_files[current_row],
            )
            # Update UI
            item = self.merge_file_list.takeItem(current_row)
            self.merge_file_list.insertItem(current_row - 1, item)
            self.merge_file_list.setCurrentRow(current_row - 1)

    def _move_merge_file_down(self):
        current_row = self.merge_file_list.currentRow()
        if current_row < self.merge_file_list.count() - 1:
            # Swap in list
            self.merge_files[current_row], self.merge_files[current_row + 1] = (
                self.merge_files[current_row + 1],
                self.merge_files[current_row],
            )
            # Update UI
            item = self.merge_file_list.takeItem(current_row)
            self.merge_file_list.insertItem(current_row + 1, item)
            self.merge_file_list.setCurrentRow(current_row + 1)

    def _browse_merge_output(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Merged PDF As",
            str(Path.home() / "Documents" / "merged.pdf"),
            "PDF Files (*.pdf);;All Files (*)",
        )
        if file_path:
            self.merge_output_input.setText(file_path)

    def _update_merge_status(self):
        count = len(self.merge_files)
        if count == 0:
            self.status_label.setText("💡 Add PDF files to merge")
        else:
            self.status_label.setText(f"📊 {count} file(s) ready to merge")

    def _execute_merge(self):
        if not self.merge_files:
            QMessageBox.warning(self, "No Files", "Please add PDF files to merge.")
            return

        output_path = self.merge_output_input.text()
        if not output_path:
            QMessageBox.warning(self, "No Output", "Please select an output file location.")
            return

        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.status_label.setText("🔄 Merging PDFs...")

        self.merge_worker = MergeWorker(self.merge_files, output_path)
        self.merge_worker.progress.connect(self._on_merge_progress)
        self.merge_worker.finished.connect(self._on_merge_finished)
        self.merge_worker.start()

    def _on_merge_progress(self, percent: int, message: str):
        self.progress.setValue(percent)
        self.status_label.setText(f"🔄 {message}")

    def _on_merge_finished(self, success: bool, message: str, output_path: str):
        self.progress.setVisible(False)
        if success:
            QMessageBox.information(self, "✅ Success", f"{message}\n\nSaved to:\n{output_path}")
            self._clear_merge_files()
            self.merge_output_input.clear()
        else:
            QMessageBox.critical(self, "❌ Error", f"Merge failed:\n{message}")
        self.status_label.setText("💡 Select operation to begin")

    # Split operations
    def _browse_split_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select PDF to Split", "", "PDF Files (*.pdf);;All Files (*)"
        )
        if file_path:
            self.split_file_input.setText(file_path)
            try:
                with PDFSplitter(file_path) as splitter:
                    page_count = splitter.page_count
                    self.split_info_label.setText(f"📄 {Path(file_path).name} - {page_count} pages")
                    self.page_range_input.setPlaceholderText(f"e.g., 1-{page_count}")
            except Exception as e:
                self.split_info_label.setText(f"⚠️ Cannot read file: {str(e)}")

    def _browse_split_output(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Output Directory", str(Path.home() / "Documents")
        )
        if dir_path:
            self.split_output_input.setText(dir_path)

    def _execute_split(self):
        input_path = self.split_file_input.text()
        if not input_path:
            QMessageBox.warning(self, "No File", "Please select a PDF file to split.")
            return

        output_path = self.split_output_input.text()
        if not output_path:
            QMessageBox.warning(self, "No Output", "Please select an output location.")
            return

        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.status_label.setText("🔄 Splitting PDF...")

        # Determine split mode and parameters
        checked_id = self.mode_group.checkedId()

        if checked_id == 0:  # Range
            page_range = self.page_range_input.text()
            if not page_range:
                QMessageBox.warning(self, "No Range", "Please enter a page range.")
                self.progress.setVisible(False)
                return
            output_path = Path(output_path) / f"{Path(input_path).stem}_split.pdf"
            kwargs = {"page_range": page_range}
        elif checked_id == 1:  # Individual
            kwargs = {"individual": True}
        else:  # Chunk
            kwargs = {"chunk_size": self.chunk_size_spin.value()}

        self.split_worker = SplitWorker(
            input_path,
            str(output_path),
            mode="range" if checked_id == 0 else ("individual" if checked_id == 1 else "chunk"),
            **kwargs,
        )
        self.split_worker.progress.connect(self._on_split_progress)
        self.split_worker.finished.connect(self._on_split_finished)
        self.split_worker.start()

    def _on_split_progress(self, percent: int, message: str):
        self.progress.setValue(percent)
        self.status_label.setText(f"🔄 {message}")

    def _on_split_finished(self, success: bool, message: str, result):
        self.progress.setVisible(False)
        if success:
            if isinstance(result, list):
                details = f"\n\nCreated files:\n" + "\n".join(
                    f"• {Path(f).name}" for f in result[:5]
                )
                if len(result) > 5:
                    details += f"\n... and {len(result) - 5} more"
            else:
                details = f"\n\nSaved to:\n{result}"
            QMessageBox.information(self, "✅ Success", f"{message}{details}")
            self.split_file_input.clear()
            self.split_info_label.setText("")
            self.split_output_input.clear()
        else:
            QMessageBox.critical(self, "❌ Error", f"Split failed:\n{message}")
        self.status_label.setText("💡 Select operation to begin")
