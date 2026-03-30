"""
Text element for PDF design
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple, List
import fitz

from pdfmaster.src.design.elements.base import DesignElement, Rectangle, TextStyle


@dataclass
class TextElement(DesignElement):
    """Text element for PDF design"""

    type: str = "text"

    # Content
    content: str = ""

    # Styling
    style: TextStyle = field(default_factory=TextStyle)

    # Multi-line support
    auto_wrap: bool = True
    max_width: Optional[float] = None

    def render(self, page: fitz.Page) -> None:
        """Render text to PDF page"""
        if not self.visible or not self.content:
            return

        # Insert text
        page.insert_text(
            (self.bounds.x, self.bounds.y + self.bounds.height),
            self.content,
            fontsize=self.style.font_size,
            fontname=self.style.font,
            color=(
                self.style.font_color[0] / 255,
                self.style.font_color[1] / 255,
                self.style.font_color[2] / 255,
            ),
            rotate=self.rotation,
        )

    def get_bounds(self) -> Rectangle:
        """Calculate bounds based on content"""
        # Estimate width based on character count
        char_width = self.style.font_size * 0.5
        width = len(self.content) * char_width
        height = self.style.font_size * self.style.line_height

        if self.max_width and width > self.max_width:
            width = self.max_width
            lines = int(len(self.content) * char_width / self.max_width) + 1
            height = lines * height

        return Rectangle(self.bounds.x, self.bounds.y, width, height)

    def set_text(self, text: str) -> "TextElement":
        """Set text content"""
        self.content = text
        return self

    def set_font(self, font_name: str, size: int = 12) -> "TextElement":
        """Set font properties"""
        self.style.font_name = font_name
        self.style.font_size = size
        return self

    def set_color(self, color: Tuple[int, int, int]) -> "TextElement":
        """Set text color"""
        self.style.font_color = color
        return self


@dataclass
class RichTextElement(DesignElement):
    """Rich text element with multiple styled segments"""

    type: str = "rich_text"

    # Text segments with individual styles
    segments: List[Tuple[str, TextStyle]] = field(default_factory=list)

    # Default style for segments without explicit style
    default_style: TextStyle = field(default_factory=TextStyle)

    auto_wrap: bool = True

    def add_segment(self, text: str, style: Optional[TextStyle] = None) -> "RichTextElement":
        """Add a text segment"""
        self.segments.append((text, style or self.default_style))
        return self

    def add_text(self, text: str) -> "RichTextElement":
        """Add plain text segment"""
        self.segments.append((text, self.default_style))
        return self

    def add_bold(self, text: str) -> "RichTextElement":
        """Add bold text"""
        style = TextStyle(
            font_name=self.default_style.font_name,
            font_size=self.default_style.font_size,
            font_weight="bold",
            font_color=self.default_style.font_color,
        )
        self.segments.append((text, style))
        return self

    def add_italic(self, text: str) -> "RichTextElement":
        """Add italic text"""
        style = TextStyle(
            font_name=self.default_style.font_name,
            font_size=self.default_style.font_size,
            font_style="italic",
            font_color=self.default_style.font_color,
        )
        self.segments.append((text, style))
        return self

    def add_colored(self, text: str, color: Tuple[int, int, int]) -> "RichTextElement":
        """Add colored text"""
        style = TextStyle(
            font_name=self.default_style.font_name,
            font_size=self.default_style.font_size,
            font_color=color,
        )
        self.segments.append((text, style))
        return self

    def render(self, page: fitz.Page) -> None:
        """Render rich text to PDF page"""
        if not self.visible or not self.segments:
            return

        x = self.bounds.x
        y = self.bounds.y + self.bounds.height

        for text, style in self.segments:
            page.insert_text(
                (x, y),
                text,
                fontsize=style.font_size,
                fontname=style.font,
                color=(
                    style.font_color[0] / 255,
                    style.font_color[1] / 255,
                    style.font_color[2] / 255,
                ),
            )
            # Move x position for next segment
            x += len(text) * style.font_size * 0.5

    def get_bounds(self) -> Rectangle:
        """Calculate bounds based on segments"""
        total_width = 0
        max_height = 0

        for text, style in self.segments:
            total_width += len(text) * style.font_size * 0.5
            height = style.font_size * style.line_height
            max_height = max(max_height, height)

        return Rectangle(self.bounds.x, self.bounds.y, total_width, max_height)
