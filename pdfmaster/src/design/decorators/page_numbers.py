"""
Page numbers decorator for PDF documents
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Union
from pathlib import Path
from enum import Enum
import fitz

from pdfmaster.src.core.editor import PDFEditor


class PageNumberFormat(Enum):
    """Page number formats"""

    NUMERIC = "numeric"  # 1, 2, 3
    ROMAN = "roman"  # I, II, III
    ALPHA = "alpha"  # A, B, C
    CUSTOM = "custom"  # Custom prefix/suffix


class PageNumberPosition(Enum):
    """Page number positions"""

    TOP_LEFT = "top-left"
    TOP_CENTER = "top-center"
    TOP_RIGHT = "top-right"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_CENTER = "bottom-center"
    BOTTOM_RIGHT = "bottom-right"


@dataclass
class PageNumberConfig:
    """Configuration for page numbers"""

    # Format
    number_format: PageNumberFormat = PageNumberFormat.NUMERIC

    # Custom format
    prefix: str = ""
    suffix: str = ""
    template: str = "{prefix}{number}{suffix}"  # e.g., "Page {number} of {total}"

    # Position
    position: PageNumberPosition = PageNumberPosition.BOTTOM_CENTER

    # Styling
    font_name: str = "Helvetica"
    font_size: int = 10
    color: Tuple[int, int, int] = (0, 0, 0)

    # Page range
    start_number: int = 1
    show_first_page: bool = True
    show_last_page: bool = True

    # Margins
    margin_x: float = 72  # Points
    margin_y: float = 36  # Points

    # Show total pages
    show_total: bool = False
    total_separator: str = " / "


class PageNumberApplier:
    """Apply page numbers to PDF documents"""

    def __init__(self, config: PageNumberConfig):
        self.config = config

    def apply(self, input_path: Union[str, Path], output_path: Union[str, Path]) -> Path:
        """Apply page numbers to PDF"""
        input_path = Path(input_path)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        doc = fitz.open(str(input_path))
        total_pages = len(doc)

        try:
            for page_num in range(total_pages):
                # Check if we should show page number
                if not self._should_show_page(page_num, total_pages):
                    continue

                page = doc[page_num]
                page_number = page_num + self.config.start_number
                self._apply_page_number(page, page_num, page_number, total_pages)

            doc.save(str(output_path))
            return output_path
        finally:
            doc.close()

    def _should_show_page(self, page_num: int, total_pages: int) -> bool:
        """Check if page number should be shown on this page"""
        if not self.config.show_first_page and page_num == 0:
            return False
        if not self.config.show_last_page and page_num == total_pages - 1:
            return False
        return True

    def _apply_page_number(
        self, page: fitz.Page, page_num: int, page_number: int, total_pages: int
    ) -> None:
        """Apply page number to a single page"""
        config = self.config
        rect = page.rect

        # Format the page number
        number_text = self._format_page_number(page_number, total_pages)

        # Calculate position
        x, y = self._calculate_position(rect, number_text)

        # Draw page number
        page.insert_text(
            (x, y),
            number_text,
            fontsize=config.font_size,
            fontname=config.font_name,
            color=(config.color[0] / 255, config.color[1] / 255, config.color[2] / 255),
        )

    def _format_page_number(self, page_number: int, total_pages: int) -> str:
        """Format page number according to configuration"""
        config = self.config

        # Convert number based on format
        if config.number_format == PageNumberFormat.NUMERIC:
            number_str = str(page_number)
        elif config.number_format == PageNumberFormat.ROMAN:
            number_str = self._to_roman(page_number)
        elif config.number_format == PageNumberFormat.ALPHA:
            number_str = self._to_alpha(page_number)
        else:
            number_str = str(page_number)

        # Build final string
        if config.show_total:
            total_str = (
                str(total_pages)
                if config.number_format == PageNumberFormat.NUMERIC
                else self._to_roman(total_pages)
            )
            return f"{config.prefix}{number_str}{config.total_separator}{total_str}{config.suffix}"
        else:
            return config.template.format(
                prefix=config.prefix,
                number=number_str,
                total=total_str if config.show_total else "",
                suffix=config.suffix,
            )

    def _calculate_position(self, rect: fitz.Rect, text: str) -> Tuple[float, float]:
        """Calculate text position based on configuration"""
        config = self.config

        # Estimate text width
        text_width = len(text) * config.font_size * 0.5

        # Get base position based on config
        if config.position == PageNumberPosition.TOP_LEFT:
            x = config.margin_x
            y = config.margin_y + config.font_size
        elif config.position == PageNumberPosition.TOP_CENTER:
            x = (rect.width - text_width) / 2
            y = config.margin_y + config.font_size
        elif config.position == PageNumberPosition.TOP_RIGHT:
            x = rect.width - config.margin_x - text_width
            y = config.margin_y + config.font_size
        elif config.position == PageNumberPosition.BOTTOM_LEFT:
            x = config.margin_x
            y = rect.height - config.margin_y
        elif config.position == PageNumberPosition.BOTTOM_CENTER:
            x = (rect.width - text_width) / 2
            y = rect.height - config.margin_y
        elif config.position == PageNumberPosition.BOTTOM_RIGHT:
            x = rect.width - config.margin_x - text_width
            y = rect.height - config.margin_y
        else:
            x = (rect.width - text_width) / 2
            y = rect.height - config.margin_y

        return x, y

    @staticmethod
    def _to_roman(num: int) -> str:
        """Convert number to Roman numerals"""
        val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]

        roman_num = ""
        i = 0
        while num > 0:
            for _ in range(num // val[i]):
                roman_num += syb[i]
                num -= val[i]
            i += 1
        return roman_num

    @staticmethod
    def _to_alpha(num: int) -> str:
        """Convert number to alphabetical (A, B, C, ..., Z, AA, AB, ...)"""
        result = ""
        while num > 0:
            num, remainder = divmod(num - 1, 26)
            result = chr(65 + remainder) + result
        return result


def apply_page_numbers(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    position: PageNumberPosition = PageNumberPosition.BOTTOM_CENTER,
    number_format: PageNumberFormat = PageNumberFormat.NUMERIC,
    font_size: int = 10,
    show_total: bool = False,
) -> Path:
    """Convenience function to apply page numbers"""
    config = PageNumberConfig(
        position=position, number_format=number_format, font_size=font_size, show_total=show_total
    )
    applier = PageNumberApplier(config)
    return applier.apply(input_path, output_path)


def apply_page_numbers_with_template(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    template: str = "Page {number} of {total}",
    position: PageNumberPosition = PageNumberPosition.BOTTOM_CENTER,
) -> Path:
    """Apply page numbers with custom template"""
    config = PageNumberConfig(position=position, template=template, show_total=True)
    applier = PageNumberApplier(config)
    return applier.apply(input_path, output_path)
