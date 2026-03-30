"""
Watermark decorator for PDF documents
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Union
from pathlib import Path
from enum import Enum
import fitz

from pdfmaster.src.core.editor import PDFEditor


class WatermarkType(Enum):
    """Types of watermarks"""

    TEXT = "text"
    IMAGE = "image"
    DIAGONAL = "diagonal"
    TILED = "tiled"
    GRADIENT = "gradient"


class PageRange(Enum):
    """Page range options"""

    ALL = "all"
    FIRST = "first"
    LAST = "last"
    ODD = "odd"
    EVEN = "even"
    CUSTOM = "custom"


@dataclass
class WatermarkConfig:
    """Configuration for watermark"""

    # Type
    watermark_type: WatermarkType = WatermarkType.TEXT

    # Content
    text: str = "DRAFT"
    image_path: Optional[str] = None

    # Position (0.0 to 1.0 as percentage of page)
    x: float = 0.5
    y: float = 0.5

    # Appearance
    font_name: str = "Helvetica"
    font_size: int = 48
    color: Tuple[int, int, int] = (192, 192, 192)  # Light gray
    opacity: float = 0.3

    # Rotation (degrees)
    rotation: float = 45  # For diagonal

    # Tiling
    tile_spacing_x: float = 200
    tile_spacing_y: float = 200

    # Scale for images
    scale: float = 1.0

    # Page range
    page_range_type: PageRange = PageRange.ALL
    custom_pages: List[int] = field(default_factory=list)


class WatermarkApplier:
    """Apply watermarks to PDF documents"""

    def __init__(self, config: WatermarkConfig):
        self.config = config

    def apply(self, input_path: Union[str, Path], output_path: Union[str, Path]) -> Path:
        """Apply watermark to PDF"""
        input_path = Path(input_path)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        doc = fitz.open(str(input_path))

        try:
            for page_num in range(len(doc)):
                if self._should_apply_to_page(page_num, len(doc)):
                    page = doc[page_num]
                    self._apply_watermark_to_page(page)

            doc.save(str(output_path))
            return output_path
        finally:
            doc.close()

    def _should_apply_to_page(self, page_num: int, total_pages: int) -> bool:
        """Check if watermark should be applied to this page"""
        config = self.config

        if config.page_range_type == PageRange.ALL:
            return True
        elif config.page_range_type == PageRange.FIRST:
            return page_num == 0
        elif config.page_range_type == PageRange.LAST:
            return page_num == total_pages - 1
        elif config.page_range_type == PageRange.ODD:
            return page_num % 2 == 0  # 0-indexed, so page 1 is even
        elif config.page_range_type == PageRange.EVEN:
            return page_num % 2 == 1
        elif config.page_range_type == PageRange.CUSTOM:
            return (page_num + 1) in config.custom_pages  # Convert to 1-indexed
        return True

    def _apply_watermark_to_page(self, page: fitz.Page) -> None:
        """Apply watermark to a single page"""
        config = self.config

        if config.watermark_type == WatermarkType.TEXT:
            self._apply_text_watermark(page)
        elif config.watermark_type == WatermarkType.DIAGONAL:
            self._apply_diagonal_watermark(page)
        elif config.watermark_type == WatermarkType.IMAGE:
            self._apply_image_watermark(page)
        elif config.watermark_type == WatermarkType.TILED:
            self._apply_tiled_watermark(page)
        elif config.watermark_type == WatermarkType.GRADIENT:
            self._apply_gradient_watermark(page)

    def _apply_text_watermark(self, page: fitz.Page) -> None:
        """Apply centered text watermark"""
        config = self.config
        rect = page.rect

        # Calculate position
        x = rect.width * config.x
        y = rect.height * config.y

        # Insert text with rotation
        page.insert_text(
            (x, y),
            config.text,
            fontsize=config.font_size,
            fontname=config.font_name,
            color=(config.color[0] / 255, config.color[1] / 255, config.color[2] / 255),
            opacity=config.opacity,
            rotate=config.rotation,
        )

    def _apply_diagonal_watermark(self, page: fitz.Page) -> None:
        """Apply diagonal watermark across page"""
        config = self.config
        rect = page.rect

        # Calculate center
        cx = rect.width / 2
        cy = rect.height / 2

        # Create transparent overlay
        overlay = page.new_trx()

        # Insert text at center with rotation
        page.insert_text(
            (cx, cy),
            config.text,
            fontsize=config.font_size,
            fontname=config.font_name,
            color=(config.color[0] / 255, config.color[1] / 255, config.color[2] / 255),
            opacity=config.opacity,
            rotate=config.rotation,
        )

    def _apply_image_watermark(self, page: fitz.Page) -> None:
        """Apply image watermark"""
        config = self.config

        if not config.image_path:
            return

        rect = page.rect

        # Calculate position and size
        img_width = 200 * config.scale
        img_height = 100 * config.scale
        x = (rect.width - img_width) * config.x
        y = (rect.height - img_height) * config.y

        img_rect = fitz.Rect(x, y, x + img_width, y + img_height)

        # Insert image with opacity
        page.insert_image(img_rect, filename=config.image_path, opacity=config.opacity)

    def _apply_tiled_watermark(self, page: fitz.Page) -> None:
        """Apply tiled watermark pattern"""
        config = self.config
        rect = page.rect

        y = config.tile_spacing_y / 2
        while y < rect.height:
            x = config.tile_spacing_x / 2
            while x < rect.width:
                page.insert_text(
                    (x, y),
                    config.text,
                    fontsize=config.font_size * 0.7,  # Smaller for tiling
                    fontname=config.font_name,
                    color=(config.color[0] / 255, config.color[1] / 255, config.color[2] / 255),
                    opacity=config.opacity,
                    rotate=45,  # Always diagonal for tiling
                )
                x += config.tile_spacing_x
            y += config.tile_spacing_y

    def _apply_gradient_watermark(self, page: fitz.Page) -> None:
        """Apply gradient watermark"""
        # For gradient, we'll create multiple text instances with varying opacity
        config = self.config
        rect = page.rect

        # Simple gradient: multiple text with varying opacity
        steps = 5
        for i in range(steps):
            opacity = config.opacity * (1 - i / steps)
            offset = i * 20

            page.insert_text(
                (rect.width / 2, rect.height / 2 + offset),
                config.text,
                fontsize=config.font_size - i * 4,
                fontname=config.font_name,
                color=(config.color[0] / 255, config.color[1] / 255, config.color[2] / 255),
                opacity=opacity,
                rotate=config.rotation,
            )


def apply_watermark(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    watermark_type: WatermarkType = WatermarkType.DIAGONAL,
    text: str = "DRAFT",
    opacity: float = 0.3,
    color: Tuple[int, int, int] = (192, 192, 192),
    font_size: int = 48,
) -> Path:
    """Convenience function to apply watermark"""
    config = WatermarkConfig(
        watermark_type=watermark_type, text=text, opacity=opacity, color=color, font_size=font_size
    )
    applier = WatermarkApplier(config)
    return applier.apply(input_path, output_path)
