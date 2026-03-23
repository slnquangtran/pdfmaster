import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QFileDialog,
    QMessageBox,
    QProgressBar,
    QLineEdit,
    QGroupBox,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent


class ConvertWorker(QThread):
    progress = pyqtSignal(int, int)
    finished_file = pyqtSignal(str, bool, str)
    finished = pyqtSignal()

    def __init__(self, files, output_dir):
        super().__init__()
        self.files = files
        self.output_dir = Path(output_dir)

    def run(self):
        from pdfmaster.src.converters import convert_file

        total = len(self.files)
        for i, file_path in enumerate(self.files):
            try:
                file_path = Path(file_path)
                output_path = self.output_dir / f"{file_path.stem}.pdf"
                convert_file(file_path, output_path)
                self.finished_file.emit(str(file_path), True, str(output_path))
            except Exception as e:
                self.finished_file.emit(str(file_path), False, str(e))
            self.progress.emit(i + 1, total)
        self.finished.emit()


class FileDropWidget(QWidget):
    files_dropped = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setObjectName("dropZone")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(layout)

        self.label = QLabel("📁 Drag & Drop files here\nor click to browse")
        self.label.setObjectName("dropLabel")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.setMinimumHeight(150)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.label.setText("📥 Drop files here!")
            self.setObjectName("dropZoneActive")

    def dragLeaveEvent(self, event):
        self.label.setText("📁 Drag & Drop files here\nor click to browse")
        self.setObjectName("dropZone")

    def dropEvent(self, event: QDropEvent):
        files = []
        for url in event.mimeData().urls():
            files.append(url.toLocalFile())
        if files:
            self.files_dropped.emit(files)
        self.setObjectName("dropZone")

    def mousePressEvent(self, event):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files to Convert",
            "",
            "All Supported (*.docx *.doc *.txt *.png *.jpg *.jpeg *.html *.htm *.xlsx *.xls);;Word (*.docx *.doc);;Text (*.txt);;Images (*.png *.jpg *.jpeg);;HTML (*.html *.htm);;Excel (*.xlsx *.xls)",
        )
        if files:
            self.files_dropped.emit(files)


class ConvertWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.files = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        self.setLayout(layout)

        settings_group = QGroupBox("Output Settings")
        settings_group.setObjectName("settingsGroup")
        settings_layout = QHBoxLayout()
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        output_label = QLabel("📂 Output Directory:")
        output_label.setObjectName("fieldLabel")
        settings_layout.addWidget(output_label)

        self.output_dir_input = QLineEdit()
        self.output_dir_input.setObjectName("inputField")
        self.output_dir_input.setText(str(Path.home() / "Documents"))
        settings_layout.addWidget(self.output_dir_input, 1)

        browse_btn = QPushButton("📂 Browse")
        browse_btn.setObjectName("secondaryButton")
        browse_btn.setProperty("secondary", True)
        browse_btn.clicked.connect(self.browse_output_dir)
        settings_layout.addWidget(browse_btn)

        files_group = QGroupBox("Files to Convert")
        files_group.setObjectName("filesGroup")
        files_layout = QVBoxLayout()
        files_layout.setSpacing(10)
        files_group.setLayout(files_layout)
        layout.addWidget(files_group, 1)

        self.drop_widget = FileDropWidget()
        self.drop_widget.files_dropped.connect(self.add_files)
        files_layout.addWidget(self.drop_widget)

        self.file_list = QListWidget()
        self.file_list.setObjectName("fileList")
        self.file_list.setMinimumHeight(150)
        files_layout.addWidget(self.file_list)

        list_buttons = QHBoxLayout()
        
        remove_btn = QPushButton("❌ Remove Selected")
        remove_btn.setObjectName("secondaryButton")
        remove_btn.setProperty("secondary", True)
        remove_btn.clicked.connect(self.remove_selected)
        list_buttons.addWidget(remove_btn)

        clear_btn = QPushButton("🗑️ Clear All")
        clear_btn.setObjectName("secondaryButton")
        clear_btn.setProperty("secondary", True)
        clear_btn.clicked.connect(self.clear_files)
        list_buttons.addWidget(clear_btn)

        list_buttons.addStretch()
        files_layout.addLayout(list_buttons)

        self.progress = QProgressBar()
        self.progress.setObjectName("progressBar")
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        self.status_label = QLabel("💡 Add files to convert them to PDF")
        self.status_label.setObjectName("statusLabel")
        layout.addWidget(self.status_label)

        button_layout = QHBoxLayout()
        
        convert_btn = QPushButton("⚡ Convert All to PDF")
        convert_btn.setObjectName("primaryButton")
        convert_btn.clicked.connect(self.convert_files)
        button_layout.addWidget(convert_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)

    def browse_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_dir_input.setText(dir_path)

    def add_files(self, files):
        for f in files:
            if f not in self.files:
                self.files.append(f)
                self.file_list.addItem(f"📄 {Path(f).name}")
        self.update_status()

    def remove_selected(self):
        for item in self.file_list.selectedItems():
            row = self.file_list.row(item)
            self.file_list.takeItem(row)
            self.files.pop(row)
        self.update_status()

    def clear_files(self):
        self.files.clear()
        self.file_list.clear()
        self.update_status()

    def update_status(self):
        self.status_label.setText(f"📊 {len(self.files)} file(s) ready to convert")

    def convert_files(self):
        if not self.files:
            QMessageBox.warning(self, "No Files", "Please add files to convert.")
            return

        output_dir = self.output_dir_input.text()
        if not output_dir:
            QMessageBox.warning(self, "No Output", "Please select an output directory.")
            return

        self.worker = ConvertWorker(self.files, output_dir)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished_file.connect(self.on_file_finished)
        self.worker.finished.connect(self.on_all_finished)
        self.worker.start()

    def update_progress(self, current, total):
        self.progress.setVisible(True)
        self.progress.setMaximum(total)
        self.progress.setValue(current)
        self.status_label.setText(f"🔄 Converting {current} of {total}...")

    def on_file_finished(self, filename, success, result):
        if success:
            self.status_label.setText(f"✅ Converted: {Path(filename).name}")
        else:
            self.status_label.setText(f"❌ Failed: {Path(filename).name}")

    def on_all_finished(self):
        self.progress.setVisible(False)
        QMessageBox.information(self, "🎉 Complete", "All files have been converted!")
        self.clear_files()