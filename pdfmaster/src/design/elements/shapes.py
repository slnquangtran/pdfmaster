"""
Shape elements for PDF design
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple, List
from enum import Enum
import fitz

from pdfmaster.src.design.elements.base import DesignElement, Rectangle, FillStyle, StrokeStyle


class ShapeType(Enum):
    """Types of shapes"""

    RECTANGLE = "rectangle"
    ROUNDED_RECTANGLE = "rounded_rectangle"
    OVAL = "oval"
    CIRCLE = "circle"
    TRIANGLE = "triangle"
    STAR = "star"
    ARROW = "arrow"
    CALLOUT = "callout"
    CLOUD = "cloud"


@dataclass
class ShapeElement(DesignElement):
    """Shape element for PDF design"""

    type: str = "shape"

    # Shape type
    shape_type: ShapeType = ShapeType.RECTANGLE

    # Styling
    fill: FillStyle = field(default_factory=FillStyle)
    stroke: StrokeStyle = field(default_factory=StrokeStyle)

    # Special properties
    corner_radius: float = 0

    def render(self, page: fitz.Page) -> None:
        """Render shape to PDF page"""
        if not self.visible:
            return

        rect = self.bounds.to_fitz_rect()

        if self.shape_type == ShapeType.RECTANGLE:
            self._draw_rectangle(page, rect)
        elif self.shape_type == ShapeType.ROUNDED_RECTANGLE:
            self._draw_rounded_rectangle(page, rect)
        elif self.shape_type in (ShapeType.OVAL, ShapeType.CIRCLE):
            self._draw_oval(page, rect)
        elif self.shape_type == ShapeType.TRIANGLE:
            self._draw_triangle(page, rect)
        elif self.shape_type == ShapeType.STAR:
            self._draw_star(page, rect)
        elif self.shape_type == ShapeType.ARROW:
            self._draw_arrow(page, rect)

    def _draw_rectangle(self, page: fitz.Page, rect: fitz.Rect) -> None:
        """Draw rectangle"""
        page.draw_rect(
            rect,
            color=self._get_stroke_color(),
            fill=self._get_fill_color(),
            width=self.stroke.width,
            dash=self.stroke.get_dash(),
        )

    def _draw_rounded_rectangle(self, page: fitz.Page, rect: fitz.Rect) -> None:
        """Draw rounded rectangle"""
        # PyMuPDF doesn't have native rounded rectangles, use smooth polygon
        r = min(self.corner_radius, rect.width / 4, rect.height / 4)

        points = [
            (rect.x0 + r, rect.y0),
            (rect.x1 - r, rect.y0),
            (rect.x1, rect.y0),
            (rect.x1, rect.y0 + r),
            (rect.x1, rect.y1 - r),
            (rect.x1, rect.y1),
            (rect.x1 - r, rect.y1),
            (rect.x0 + r, rect.y1),
            (rect.x0, rect.y1),
            (rect.x0, rect.y1 - r),
            (rect.x0, rect.y0 + r),
            (rect.x0, rect.y0),
        ]

        page.draw_polyline(
            points,
            color=self._get_stroke_color(),
            fill=self._get_fill_color(),
            width=self.stroke.width,
        )

    def _draw_oval(self, page: fitz.Page, rect: fitz.Rect) -> None:
        """Draw oval/ellipse"""
        page.draw_oval(
            rect,
            color=self._get_stroke_color(),
            fill=self._get_fill_color(),
            width=self.stroke.width,
        )

    def _draw_triangle(self, page: fitz.Page, rect: fitz.Rect) -> None:
        """Draw triangle"""
        points = [
            (rect.x0 + rect.width / 2, rect.y0),  # Top center
            (rect.x1, rect.y1),  # Bottom right
            (rect.x0, rect.y1),  # Bottom left
        ]
        page.draw_polyline(
            points,
            color=self._get_stroke_color(),
            fill=self._get_fill_color(),
            width=self.stroke.width,
        )

    def _draw_star(self, page: fitz.Page, rect: fitz.Rect) -> None:
        """Draw star"""
        import math

        cx = rect.x0 + rect.width / 2
        cy = rect.y0 + rect.height / 2
        outer_r = min(rect.width, rect.height) / 2
        inner_r = outer_r * 0.4

        points = []
        for i in range(10):
            angle = math.pi / 2 + i * math.pi / 5
            r = outer_r if i % 2 == 0 else inner_r
            x = cx + r * math.cos(angle)
            y = cy - r * math.sin(angle)
            points.append((x, y))

        page.draw_polyline(
            points,
            color=self._get_stroke_color(),
            fill=self._get_fill_color(),
            width=self.stroke.width,
        )

    def _draw_arrow(self, page: fitz.Page, rect: fitz.Rect) -> None:
        """Draw arrow"""
        # Draw line
        page.draw_line(
            (rect.x0, rect.y0 + rect.height / 2),
            (rect.x1, rect.y0 + rect.height / 2),
            color=self._get_stroke_color(),
            width=self.stroke.width,
        )
        # Draw arrowhead
        arrow_size = min(rect.height, rect.width * 0.3)
        points = [
            (rect.x1, rect.y0 + rect.height / 2),
            (rect.x1 - arrow_size, rect.y0),
            (rect.x1 - arrow_size, rect.y1),
        ]
        page.draw_polyline(
            points, color=self._get_stroke_color(), fill=self._get_stroke_color(), width=1
        )

    def _get_stroke_color(self) -> Optional[Tuple[float, float, float]]:
        """Get stroke color as 0-1 tuple"""
        if self.stroke.width > 0:
            return (
                self.stroke.color[0] / 255,
                self.stroke.color[1] / 255,
                self.stroke.color[2] / 255,
            )
        return None

    def _get_fill_color(self) -> Optional[Tuple[float, float, float]]:
        """Get fill color as 0-1 tuple"""
        if self.fill.color:
            return (self.fill.color[0] / 255, self.fill.color[1] / 255, self.fill.color[2] / 255)
        return None

    def set_fill(self, color: Tuple[int, int, int], opacity: float = 1.0) -> "ShapeElement":
        """Set fill color"""
        self.fill = FillStyle(color=color, opacity=opacity)
        return self

    def set_stroke(self, color: Tuple[int, int, int], width: float = 1.0) -> "ShapeElement":
        """Set stroke style"""
        self.stroke = StrokeStyle(color=color, width=width)
        return self


@dataclass
class LineElement(DesignElement):
    """Line element for PDF design"""

    type: str = "line"

    # Line endpoints
    x2: float = 100
    y2: float = 0

    # Styling
    stroke: StrokeStyle = field(default_factory=StrokeStyle)

    # Arrow
    start_arrow: bool = False
    end_arrow: bool = False
    arrow_size: float = 10

    def render(self, page: fitz.Page) -> None:
        """Render line to PDF page"""
        if not self.visible:
            return

        color = (self.stroke.color[0] / 255, self.stroke.color[1] / 255, self.stroke.color[2] / 255)

        # Draw line
        page.draw_line(
            (self.bounds.x, self.bounds.y),
            (self.x2, self.y2),
            color=color,
            width=self.stroke.width,
            dash=self.stroke.get_dash(),
        )

        # Draw arrows if needed
        if self.start_arrow:
            self._draw_arrow(page, self.bounds.x, self.bounds.y, self.x2, self.y2, True)
        if self.end_arrow:
            self._draw_arrow(page, self.x2, self.y2, self.bounds.x, self.bounds.y, True)

    def _draw_arrow(
        self, page: fitz.Page, x1: float, y1: float, x2: float, y2: float, at_start: bool
    ) -> None:
        """Draw arrowhead"""
        import math

        angle = math.atan2(y2 - y1, x2 - x1)
        if at_start:
            angle += math.pi

        arrow_angle = math.pi / 6  # 30 degrees
        size = self.arrow_size

        color = (self.stroke.color[0] / 255, self.stroke.color[1] / 255, self.stroke.color[2] / 255)

        # Arrow points
        ax = x1 + size * math.cos(angle + math.pi - arrow_angle)
        ay = y1 + size * math.sin(angle + math.pi - arrow_angle)
        bx = x1 + size * math.cos(angle + math.pi + arrow_angle)
        by = y1 + size * math.sin(angle + math.pi + arrow_angle)

        page.draw_polygon([(x1, y1), (ax, ay), (bx, by)], color=color, fill=color)

    def get_bounds(self) -> Rectangle:
        """Get line bounds"""
        x = min(self.bounds.x, self.x2)
        y = min(self.bounds.y, self.y2)
        width = abs(self.x2 - self.bounds.x)
        height = abs(self.y2 - self.bounds.y)
        return Rectangle(x, y, width, height)

    def set_endpoints(self, x1: float, y1: float, x2: float, y2: float) -> "LineElement":
        """Set line endpoints"""
        self.bounds = Rectangle(x1, y1, 0, 0)
        self.x2 = x2
        self.y2 = y2
        return self
