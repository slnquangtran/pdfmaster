import logging
import sys
from pathlib import Path
from typing import Optional, List


def setup_logging(name: str = "pdfmaster", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def validate_file_exists(path: Path) -> bool:
    if isinstance(path, str):
        path = Path(path)
    return path.exists() and path.is_file()


def validate_output_path(path: Path, must_not_exist: bool = False) -> bool:
    if isinstance(path, str):
        path = Path(path)
    if must_not_exist:
        return not path.exists()
    parent = path.parent
    return parent.exists() or parent == Path(".")


def get_file_extension(path: Path) -> str:
    if isinstance(path, str):
        path = Path(path)
    return path.suffix.lower().lstrip(".")


def get_supported_extensions() -> List[str]:
    return [
        "pdf",
        "docx",
        "doc",
        "xlsx",
        "xls",
        "txt",
        "png",
        "jpg",
        "jpeg",
        "gif",
        "bmp",
        "html",
        "htm",
    ]


def is_supported_format(extension: str) -> bool:
    ext = extension.lower().lstrip(".")
    return ext in get_supported_extensions()


def ensure_output_directory(path: Path) -> Path:
    if isinstance(path, str):
        path = Path(path)
    parent = path.parent
    if not parent.exists():
        parent.mkdir(parents=True, exist_ok=True)
    return path
