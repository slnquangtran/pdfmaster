import logging
from pathlib import Path
from typing import Union
import fitz

logger = logging.getLogger(__name__)


def add_watermark(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    text: str,
    font_size: int = 60,
    color: tuple = (0.75, 0.75, 0.75),
    rotate: float = 45.0,
) -> Path:
    input_path = Path(input_path) if isinstance(input_path, str) else input_path
    output_path = Path(output_path) if isinstance(output_path, str) else output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(input_path))
    for page in doc:
        # Draw a large, light watermark across the page
        rect = page.rect
        page.insert_textbox(rect, text, fontsize=font_size, rotate=rotate, color=color, align=1)
    doc.save(str(output_path))
    doc.close()
    logger.info(f"Watermark applied: {output_path}")
    return output_path
