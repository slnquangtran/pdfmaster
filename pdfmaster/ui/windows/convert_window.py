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
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMimeData
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
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #f9f9f9;
            }
            QWidget:drop {
                border: 2px solid #4CAF50;
                background-color: #e8f5e9;
            }
        """)

        self.label = QLabel("Drag & Drop files here\nor click to browse")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: #666; padding: 40px;")
        layout.addWidget(self.label)

        self.setMinimumHeight(150)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.label.setText("Drop files here!")
            self.label.setStyleSheet("color: #4CAF50; padding: 40px;")

    def dragLeaveEvent(self, event):
        self.label.setText("Drag & Drop files here\nor click to browse")
        self.label.setStyleSheet("color: #666; padding: 40px;")

    def dropEvent(self, event: QDropEvent):
        files = []
        for url in event.mimeData().urls():
            files.append(url.toLocalFile())
        if files:
            self.files_dropped.emit(files)

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
        self.setLayout(layout)

        title_label = QLabel("Convert Files to PDF")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Output Directory:"))
        self.output_dir_input = QLineEdit()
        self.output_dir_input.setText(str(Path.home() / "Documents"))
        output_layout.addWidget(self.output_dir_input)
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_output_dir)
        output_layout.addWidget(browse_btn)
        layout.addLayout(output_layout)

        self.drop_widget = FileDropWidget()
        self.drop_widget.files_dropped.connect(self.add_files)
        layout.addWidget(self.drop_widget)

        self.file_list = QListWidget()
        self.file_list.setMinimumHeight(150)
        layout.addWidget(self.file_list)

        list_buttons = QHBoxLayout()
        remove_btn = QPushButton("Remove Selected")
        remove_btn.clicked.connect(self.remove_selected)
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_files)
        list_buttons.addWidget(remove_btn)
        list_buttons.addWidget(clear_btn)
        list_buttons.addStretch()
        layout.addLayout(list_buttons)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        button_layout = QHBoxLayout()
        convert_btn = QPushButton("Convert All")
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
                self.file_list.addItem(Path(f).name)
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
        self.status_label.setText(f"{len(self.files)} file(s) ready to convert")

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
        self.status_label.setText(f"Converting {current} of {total}...")

    def on_file_finished(self, filename, success, result):
        if success:
            self.status_label.setText(f"Converted: {filename} -> {result}")
        else:
            self.status_label.setText(f"Failed: {filename} - {result}")

    def on_all_finished(self):
        self.progress.setVisible(False)
        QMessageBox.information(self, "Complete", "All files have been converted!")
        self.clear_files()