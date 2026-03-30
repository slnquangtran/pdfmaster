"""
Stamp decorator for PDF documents
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Union
from pathlib import Path
from enum import Enum
import fitz

from pdfmaster.src.core.editor import PDFEditor


class StampCategory(Enum):
    """Stamp categories"""

    APPROVAL = "approval"
    STATUS = "status"
    CUSTOM = "custom"
    SPECIAL = "special"


class StampShape(Enum):
    """Stamp shapes"""

    RECTANGLE = "rectangle"
    OVAL = "oval"
    CIRCLE = "circle"


# Predefined stamps
APPROVAL_STAMPS = {
    "APPROVED": {"color": (0, 128, 0), "text": "APPROVED"},
    "REJECTED": {"color": (200, 0, 0), "text": "REJECTED"},
    "PENDING": {"color": (255, 165, 0), "text": "PENDING"},
    "REVISED": {"color": (0, 0, 200), "text": "REVISED"},
    "DRAFT": {"color": (128, 128, 128), "text": "DRAFT"},
    "FINAL": {"color": (0, 100, 0), "text": "FINAL"},
}

STATUS_STAMPS = {
    "CONFIDENTIAL": {"color": (200, 0, 0), "text": "CONFIDENTIAL"},
    "INTERNAL ONLY": {"color": (0, 0, 200), "text": "INTERNAL ONLY"},
    "COPY": {"color": (128, 128, 128), "text": "COPY"},
    "SAMPLE": {"color": (0, 128, 128), "text": "SAMPLE"},
    "VOID": {"color": (200, 0, 0), "text": "VOID"},
    "ORIGINAL": {"color": (0, 100, 0), "text": "ORIGINAL"},
}


@dataclass
class StampConfig:
    """Configuration for stamp"""

    # Stamp content
    category: StampCategory = StampCategory.APPROVAL
    stamp_name: str = "APPROVED"
    custom_text: Optional[str] = None

    # Shape
    shape: StampShape = StampShape.RECTANGLE

    # Colors
    border_color: Tuple[int, int, int] = (0, 128, 0)
    fill_color: Tuple[int, int, int] = (255, 255, 255)
    text_color: Optional[Tuple[int, int, int]] = None  # Default: same as border

    # Size
    width: float = 150
    height: float = 60
    border_width: float = 3

    # Position (0.0 to 1.0 as percentage of page)
    x: float = 0.75
    y: float = 0.8

    # Rotation (degrees)
    rotation: float = 0

    # Opacity
    opacity: float = 0.9

    # Page numbers (1-indexed)
    pages: List[int] = field(default_factory=lambda: [1])


class StampApplier:
    """Apply stamps to PDF documents"""

    def __init__(self, config: StampConfig):
        self.config = config
        self._load_stamp_properties()

    def _load_stamp_properties(self) -> None:
        """Load stamp properties from predefined stamps"""
        config = self.config

        if config.category == StampCategory.APPROVAL:
            stamp_data = APPROVAL_STAMPS.get(config.stamp_name)
        elif config.category == StampCategory.STATUS:
            stamp_data = STATUS_STAMPS.get(config.stamp_name)
        else:
            stamp_data = None

        if stamp_data:
            config.border_color = stamp_data["color"]
            if not config.custom_text:
                config.custom_text = stamp_data["text"]
            if not config.text_color:
                config.text_color = stamp_data["color"]

    def apply(self, input_path: Union[str, Path], output_path: Union[str, Path]) -> Path:
        """Apply stamp to PDF"""
        input_path = Path(input_path)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        doc = fitz.open(str(input_path))

        try:
            for page_num in range(len(doc)):
                # Convert to 1-indexed for comparison
                if (page_num + 1) in self.config.pages or not self.config.pages:
                    page = doc[page_num]
                    self._apply_stamp_to_page(page)

            doc.save(str(output_path))
            return output_path
        finally:
            doc.close()

    def _apply_stamp_to_page(self, page: fitz.Page) -> None:
        """Apply stamp to a single page"""
        config = self.config
        rect = page.rect

        # Calculate position
        x = rect.width * config.x
        y = rect.height * config.y

        # Create stamp rectangle (centered on position)
        stamp_rect = fitz.Rect(
            x - config.width / 2, y - config.height / 2, x + config.width / 2, y + config.height / 2
        )

        # Get text
        text = config.custom_text or config.stamp_name

        # Set colors
        border_color = (
            config.border_color[0] / 255,
            config.border_color[1] / 255,
            config.border_color[2] / 255,
        )

        fill_color = (
            config.fill_color[0] / 255,
            config.fill_color[1] / 255,
            config.fill_color[2] / 255,
        )

        text_color = config.text_color or config.border_color
        text_color = (text_color[0] / 255, text_color[1] / 255, text_color[2] / 255)

        # Draw shape based on type
        if config.shape == StampShape.RECTANGLE:
            page.draw_rect(
                stamp_rect,
                color=border_color,
                fill=fill_color,
                width=config.border_width,
                opacity=config.opacity,
            )
        elif config.shape == StampShape.OVAL:
            page.draw_oval(
                stamp_rect,
                color=border_color,
                fill=fill_color,
                width=config.border_width,
                opacity=config.opacity,
            )
        elif config.shape == StampShape.CIRCLE:
            # Make it a square for circle
            size = min(config.width, config.height)
            circle_rect = fitz.Rect(x - size / 2, y - size / 2, x + size / 2, y + size / 2)
            page.draw_oval(
                circle_rect,
                color=border_color,
                fill=fill_color,
                width=config.border_width,
                opacity=config.opacity,
            )

        # Calculate font size based on text length and stamp width
        font_size = min(config.height * 0.5, config.width / len(text) * 1.5)

        # Calculate text position (centered)
        text_width = len(text) * font_size * 0.5
        text_x = x - text_width / 2
        text_y = y + font_size / 3

        # Draw text
        page.insert_text(
            (text_x, text_y),
            text,
            fontsize=font_size,
            fontname="Helvetica-Bold",
            color=text_color,
            opacity=config.opacity,
            rotate=config.rotation,
        )


def apply_stamp(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    stamp_name: str = "APPROVED",
    category: StampCategory = StampCategory.APPROVAL,
    x: float = 0.75,
    y: float = 0.8,
    rotation: float = -15,
    pages: Optional[List[int]] = None,
) -> Path:
    """Convenience function to apply stamp"""
    config = StampConfig(
        stamp_name=stamp_name, category=category, x=x, y=y, rotation=rotation, pages=pages or [1]
    )
    applier = StampApplier(config)
    return applier.apply(input_path, output_path)


def apply_approved_stamp(
    input_path: Union[str, Path], output_path: Union[str, Path], pages: Optional[List[int]] = None
) -> Path:
    """Apply APPROVED stamp"""
    return apply_stamp(input_path, output_path, "APPROVED", pages=pages)


def apply_confidential_stamp(
    input_path: Union[str, Path], output_path: Union[str, Path], pages: Optional[List[int]] = None
) -> Path:
    """Apply CONFIDENTIAL stamp"""
    return apply_stamp(
        input_path, output_path, "CONFIDENTIAL", category=StampCategory.STATUS, pages=pages
    )
