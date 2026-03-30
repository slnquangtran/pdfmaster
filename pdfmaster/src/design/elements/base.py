"""
Base design element classes for PDF design
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Tuple, List
import uuid
import fitz


@dataclass
class Rectangle:
    """Represents a rectangular area"""

    x: float
    y: float
    width: float
    height: float

    @property
    def x1(self) -> float:
        return self.x

    @property
    def y1(self) -> float:
        return self.y

    @property
    def x2(self) -> float:
        return self.x + self.width

    @property
    def y2(self) -> float:
        return self.y + self.height

    def to_fitz_rect(self) -> fitz.Rect:
        """Convert to PyMuPDF Rect"""
        return fitz.Rect(self.x, self.y, self.x2, self.y2)

    def contains_point(self, px: float, py: float) -> bool:
        """Check if point is inside rectangle"""
        return self.x1 <= px <= self.x2 and self.y1 <= py <= self.y2

    def expand(self, margin: float) -> "Rectangle":
        """Create expanded rectangle with margin"""
        return Rectangle(
            self.x - margin, self.y - margin, self.width + 2 * margin, self.height + 2 * margin
        )


@dataclass
class TextStyle:
    """Text styling properties"""

    font_name: str = "Helvetica"
    font_size: int = 12
    font_weight: str = "normal"  # normal, bold
    font_style: str = "normal"  # normal, italic, oblique
    font_color: Tuple[int, int, int] = (0, 0, 0)
    line_height: float = 1.2
    alignment: str = "left"  # left, center, right, justify
    letter_spacing: float = 0
    background_color: Optional[Tuple[int, int, int]] = None

    @property
    def font(self) -> str:
        """Get full font name for PyMuPDF"""
        font = self.font_name
        if self.font_weight == "bold":
            font += "-Bold"
        if self.font_style == "italic":
            font += "-Oblique"
        elif self.font_style == "oblique":
            font += "-Oblique"
        return font


@dataclass
class StrokeStyle:
    """Stroke/line styling properties"""

    color: Tuple[int, int, int] = (0, 0, 0)
    width: float = 1.0
    style: str = "solid"  # solid, dashed, dotted
    dash_pattern: Optional[List[float]] = None

    def get_dash(self) -> Optional[List[float]]:
        """Get dash pattern for PyMuPDF"""
        if self.style == "dashed":
            return [6, 3]
        elif self.style == "dotted":
            return [2, 2]
        return self.dash_pattern


@dataclass
class DesignElement(ABC):
    """Base class for all design elements"""

    # Identity
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = "Element"
    type: str = "base"

    # Position and size
    bounds: Rectangle = field(default_factory=lambda: Rectangle(0, 0, 100, 50))

    # Appearance
    rotation: float = 0
    opacity: float = 1.0

    # Layer and state
    layer: int = 0
    locked: bool = False
    visible: bool = True
    selected: bool = False

    @abstractmethod
    def render(self, page: fitz.Page) -> None:
        """Render element to PDF page"""
        pass

    @abstractmethod
    def get_bounds(self) -> Rectangle:
        """Get element bounding box"""
        return self.bounds

    def contains_point(self, x: float, y: float) -> bool:
        """Check if point is within element"""
        return self.bounds.contains_point(x, y)

    def move(self, dx: float, dy: float) -> None:
        """Move element by delta"""
        self.bounds = Rectangle(
            self.bounds.x + dx, self.bounds.y + dy, self.bounds.width, self.bounds.height
        )

    def resize(self, width: float, height: float) -> None:
        """Resize element"""
        self.bounds = Rectangle(self.bounds.x, self.bounds.y, width, height)


@dataclass
class FillStyle:
    """Fill styling properties"""

    color: Optional[Tuple[int, int, int]] = None
    opacity: float = 1.0

    def get_fitz_color(self) -> Optional[Tuple[float, float, float]]:
        """Get color as 0-1 tuple for PyMuPDF"""
        if self.color:
            return (self.color[0] / 255, self.color[1] / 255, self.color[2] / 255)
        return None
