from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class PDFDocument:
    file_path: Path
    page_count: int = 0
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    title: Optional[str] = None
    author: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.file_path, str):
            self.file_path = Path(self.file_path)

    @property
    def exists(self) -> bool:
        return self.file_path.exists()

    @property
    def size(self) -> int:
        if self.exists:
            return self.file_path.stat().st_size
        return 0


@dataclass
class PDFPage:
    page_number: int
    width: float = 612.0
    height: float = 792.0
    elements: list = field(default_factory=list)


@dataclass
class ConversionJob:
    input_path: Path
    output_path: Path
    input_format: str
    output_format: str = "pdf"
    status: str = "pending"
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        if isinstance(self.input_path, str):
            self.input_path = Path(self.input_path)
        if isinstance(self.output_path, str):
            self.output_path = Path(self.output_path)
