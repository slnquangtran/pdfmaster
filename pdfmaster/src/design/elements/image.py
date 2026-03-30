"""
Image element for PDF design
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple, Union
from pathlib import Path
import fitz

from pdfmaster.src.design.elements.base import DesignElement, Rectangle


@dataclass
class ImageElement(DesignElement):
    """Image element for PDF design"""

    type: str = "image"

    # Image source
    source: Optional[str] = None  # File path

    # Sizing
    maintain_aspect: bool = True

    # Appearance
    border_width: float = 0
    border_color: Tuple[int, int, int] = (0, 0, 0)
    corner_radius: float = 0

    # Grayscale
    grayscale: bool = False

    def render(self, page: fitz.Page) -> None:
        """Render image to PDF page"""
        if not self.visible or not self.source:
            return

        try:
            # Calculate image rectangle
            rect = self.bounds.to_fitz_rect()

            # Insert image
            page.insert_image(rect, filename=self.source, rotate=self.rotation)

            # Draw border if specified
            if self.border_width > 0:
                page.draw_rect(
                    rect,
                    color=(
                        self.border_color[0] / 255,
                        self.border_color[1] / 255,
                        self.border_color[2] / 255,
                    ),
                    width=self.border_width,
                )

        except Exception as e:
            print(f"Error rendering image: {e}")

    def get_bounds(self) -> Rectangle:
        """Get image bounds"""
        return self.bounds

    def set_source(self, path: Union[str, Path]) -> "ImageElement":
        """Set image source path"""
        self.source = str(path)
        return self

    def fit_to_bounds(self, width: float, height: float) -> "ImageElement":
        """Set bounds to fit image"""
        self.bounds = Rectangle(self.bounds.x, self.bounds.y, width, height)
        return self


@dataclass
class ImageConfig:
    """Configuration for image insertion"""

    source: str
    x: float = 72
    y: float = 72
    width: Optional[float] = None
    height: Optional[float] = None
    maintain_aspect: bool = True
    opacity: float = 1.0
    rotation: float = 0
    border_width: float = 0
    border_color: Tuple[int, int, int] = (0, 0, 0)
