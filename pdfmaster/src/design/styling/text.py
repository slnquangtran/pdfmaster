"""
Text styling utilities for PDF design
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Union
import fitz


@dataclass
class FontConfig:
    """Font configuration"""

    name: str = "Helvetica"
    size: int = 12
    weight: str = "normal"  # normal, bold
    style: str = "normal"  # normal, italic, oblique

    @property
    def pdf_font_name(self) -> str:
        """Get PyMuPDF font name"""
        font = self.name
        if self.weight == "bold":
            font += "-Bold"
        if self.style in ("italic", "oblique"):
            font += "-Oblique"
        return font


# Standard PDF fonts
STANDARD_FONTS = {
    "Helvetica": {
        "normal": "Helvetica",
        "bold": "Helvetica-Bold",
        "italic": "Helvetica-Oblique",
        "bold_italic": "Helvetica-BoldOblique",
    },
    "Times": {
        "normal": "Times-Roman",
        "bold": "Times-Bold",
        "italic": "Times-Italic",
        "bold_italic": "Times-BoldItalic",
    },
    "Courier": {
        "normal": "Courier",
        "bold": "Courier-Bold",
        "italic": "Courier-Oblique",
        "bold_italic": "Courier-BoldOblique",
    },
    "Symbol": {"normal": "Symbol"},
    "ZapfDingbats": {"normal": "ZapfDingbats"},
}


class TextStyler:
    """Text styling utilities"""

    @staticmethod
    def get_font_names(font_family: str = "Helvetica") -> dict:
        """Get all font variants for a family"""
        return STANDARD_FONTS.get(font_family, STANDARD_FONTS["Helvetica"])

    @staticmethod
    def get_available_families() -> List[str]:
        """Get list of available font families"""
        return list(STANDARD_FONTS.keys())

    @staticmethod
    def calculate_text_width(text: str, font_size: int, font_name: str = "Helvetica") -> float:
        """Calculate approximate width of text"""
        # Rough estimation: average character width is about 0.5 * font_size
        return len(text) * font_size * 0.5

    @staticmethod
    def calculate_text_height(font_size: int, line_height: float = 1.2) -> float:
        """Calculate height of text line"""
        return font_size * line_height

    @staticmethod
    def wrap_text(text: str, max_width: float, font_size: int) -> List[str]:
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_width = len(word) * font_size * 0.5

            if current_width + word_width > max_width and current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width
            else:
                current_line.append(word)
                current_width += word_width + font_size * 0.25  # Space width

        if current_line:
            lines.append(" ".join(current_line))

        return lines

    @staticmethod
    def insert_styled_text(
        page: fitz.Page,
        text: str,
        x: float,
        y: float,
        font_name: str = "Helvetica",
        font_size: int = 12,
        color: Tuple[int, int, int] = (0, 0, 0),
        bold: bool = False,
        italic: bool = False,
    ) -> float:
        """Insert styled text and return new y position"""
        # Determine font variant
        if bold and italic:
            actual_font = f"{font_name}-BoldOblique"
        elif bold:
            actual_font = f"{font_name}-Bold"
        elif italic:
            actual_font = f"{font_name}-Oblique"
        else:
            actual_font = font_name

        # Convert color to 0-1 range
        color_01 = (color[0] / 255, color[1] / 255, color[2] / 255)

        # Insert text
        page.insert_text((x, y), text, fontsize=font_size, fontname=actual_font, color=color_01)

        # Return new y position
        return y - font_size * 1.2

    @staticmethod
    def insert_multiline_text(
        page: fitz.Page,
        text: str,
        x: float,
        y: float,
        max_width: float,
        font_name: str = "Helvetica",
        font_size: int = 12,
        color: Tuple[int, int, int] = (0, 0, 0),
        line_height: float = 1.2,
    ) -> float:
        """Insert multiline text with wrapping and return new y position"""
        lines = TextStyler.wrap_text(text, max_width, font_size)
        current_y = y

        for line in lines:
            current_y = TextStyler.insert_styled_text(
                page, line, x, current_y, font_name=font_name, font_size=font_size, color=color
            )
            current_y -= font_size * (line_height - 1)  # Additional spacing

        return current_y

    @staticmethod
    def insert_paragraph(
        page: fitz.Page,
        paragraphs: List[str],
        x: float,
        y: float,
        max_width: float,
        font_name: str = "Helvetica",
        font_size: int = 12,
        color: Tuple[int, int, int] = (0, 0, 0),
        line_height: float = 1.2,
        paragraph_spacing: float = 12,
    ) -> float:
        """Insert multiple paragraphs with proper spacing"""
        current_y = y

        for para in paragraphs:
            current_y = TextStyler.insert_multiline_text(
                page,
                para,
                x,
                current_y,
                max_width,
                font_name=font_name,
                font_size=font_size,
                color=color,
                line_height=line_height,
            )
            current_y -= paragraph_spacing

        return current_y


class TextStyleBuilder:
    """Builder pattern for text styles"""

    def __init__(self):
        self._font_name = "Helvetica"
        self._font_size = 12
        self._bold = False
        self._italic = False
        self._color = (0, 0, 0)

    def set_font(self, name: str) -> "TextStyleBuilder":
        self._font_name = name
        return self

    def set_size(self, size: int) -> "TextStyleBuilder":
        self._font_size = size
        return self

    def set_bold(self, bold: bool = True) -> "TextStyleBuilder":
        self._bold = bold
        return self

    def set_italic(self, italic: bool = True) -> "TextStyleBuilder":
        self._italic = italic
        return self

    def set_color(self, r: int, g: int, b: int) -> "TextStyleBuilder":
        self._color = (r, g, b)
        return self

    def build(self) -> dict:
        return {
            "font_name": self._font_name,
            "font_size": self._font_size,
            "bold": self._bold,
            "italic": self._italic,
            "color": self._color,
        }


# Preset styles
TITLE_STYLE = {"font_name": "Helvetica", "font_size": 24, "bold": True, "color": (0, 0, 0)}

HEADING1_STYLE = {"font_name": "Helvetica", "font_size": 18, "bold": True, "color": (33, 37, 41)}

HEADING2_STYLE = {"font_name": "Helvetica", "font_size": 16, "bold": True, "color": (33, 37, 41)}

HEADING3_STYLE = {"font_name": "Helvetica", "font_size": 14, "bold": True, "color": (33, 37, 41)}

BODY_STYLE = {"font_name": "Helvetica", "font_size": 12, "bold": False, "color": (33, 37, 41)}

CAPTION_STYLE = {
    "font_name": "Helvetica",
    "font_size": 10,
    "italic": True,
    "color": (108, 117, 125),
}

CODE_STYLE = {"font_name": "Courier", "font_size": 10, "bold": False, "color": (33, 37, 41)}
