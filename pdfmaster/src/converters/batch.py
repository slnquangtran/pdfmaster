import logging
from pathlib import Path
from typing import Union, Dict

from pdfmaster.src.converters import convert_file

logger = logging.getLogger(__name__)


def batch_convert_directory(
    input_dir: Union[str, Path],
    output_dir: Union[str, Path],
    pattern: str = "*.*",
) -> Dict[str, int]:
    if isinstance(input_dir, str):
        input_dir = Path(input_dir)
    if isinstance(output_dir, str):
        output_dir = Path(output_dir)

    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    input_files = list(input_dir.glob(pattern))
    supported_extensions = {
        ".docx",
        ".doc",
        ".txt",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".bmp",
        ".html",
        ".htm",
        ".xlsx",
        ".xls",
    }
    input_files = [f for f in input_files if f.suffix.lower() in supported_extensions]

    success = 0
    failed = 0
    errors = []

    for input_file in input_files:
        output_file = output_dir / f"{input_file.stem}.pdf"
        try:
            convert_file(input_file, output_file)
            success += 1
            logger.info(f"Converted: {input_file.name}")
        except Exception as e:
            failed += 1
            error_msg = f"{input_file.name}: {str(e)}"
            errors.append(error_msg)
            logger.error(f"Failed to convert {input_file.name}: {e}")

    result = {"total": len(input_files), "success": success, "failed": failed}
    if errors:
        result["errors"] = errors

    return result
