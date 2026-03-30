"""
Header and footer decorator for PDF documents
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Union
from pathlib import Path
from datetime import datetime
import fitz

from pdfmaster.src.core.editor import PDFEditor


@dataclass
class HeaderConfig:
    """Configuration for header"""

    # Content
    show_title: bool = True
    title: str = ""
    show_author: bool = False
    author: str = ""
    show_date: bool = False
    date_format: str = "%Y-%m-%d"
    show_logo: bool = False
    logo_path: Optional[str] = None
    logo_width: float = 50
    logo_height: float = 25

    # Styling
    font_name: str = "Helvetica"
    font_size: int = 10
    color: Tuple[int, int, int] = (0, 0, 0)

    # Layout
    height: float = 40  # Points
    show_line: bool = True
    line_color: Tuple[int, int, int] = (0, 0, 0)
    line_width: float = 0.5

    # Margins
    margin_left: float = 72
    margin_right: float = 72
    padding_top: float = 10


@dataclass
class FooterConfig:
    """Configuration for footer"""

    # Content
    show_author: bool = False
    author: str = ""
    show_date: bool = False
    date_format: str = "%Y-%m-%d"
    show_copyright: bool = True
    copyright_text: str = "© {year} {author}"

    # Custom text
    left_text: str = ""
    center_text: str = ""
    right_text: str = ""

    # Styling
    font_name: str = "Helvetica"
    font_size: int = 9
    color: Tuple[int, int, int] = (128, 128, 128)

    # Layout
    height: float = 30  # Points
    show_line: bool = True
    line_color: Tuple[int, int, int] = (192, 192, 192)
    line_width: float = 0.5

    # Margins
    margin_left: float = 72
    margin_right: float = 72
    padding_bottom: float = 10


@dataclass
class HeaderFooterConfig:
    """Combined header and footer configuration"""

    header: HeaderConfig = field(default_factory=HeaderConfig)
    footer: FooterConfig = field(default_factory=FooterConfig)

    # Page range
    apply_to_first_page: bool = False  # Often want blank first page
    apply_to_last_page: bool = True

    # Different odd/even
    odd_even_different: bool = False
    odd_header: Optional[HeaderConfig] = None
    even_header: Optional[HeaderConfig] = None


class HeaderFooterApplier:
    """Apply headers and footers to PDF documents"""

    def __init__(self, config: HeaderFooterConfig):
        self.config = config

    def apply(self, input_path: Union[str, Path], output_path: Union[str, Path]) -> Path:
        """Apply headers and footers to PDF"""
        input_path = Path(input_path)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        doc = fitz.open(str(input_path))
        total_pages = len(doc)

        try:
            for page_num in range(total_pages):
                # Check if we should apply to this page
                if not self._should_apply_to_page(page_num, total_pages):
                    continue

                page = doc[page_num]

                # Determine which config to use (odd/even)
                header_config = self._get_header_config(page_num)

                # Apply header
                self._apply_header(page, header_config, page_num, total_pages)

                # Apply footer
                self._apply_footer(page, self.config.footer, page_num, total_pages)

            doc.save(str(output_path))
            return output_path
        finally:
            doc.close()

    def _should_apply_to_page(self, page_num: int, total_pages: int) -> bool:
        """Check if header/footer should be applied to this page"""
        if not self.config.apply_to_first_page and page_num == 0:
            return False
        if not self.config.apply_to_last_page and page_num == total_pages - 1:
            return False
        return True

    def _get_header_config(self, page_num: int) -> HeaderConfig:
        """Get appropriate header config for page"""
        if self.config.odd_even_different:
            if page_num % 2 == 0:  # Odd page (1-indexed)
                return self.config.odd_header or self.config.header
            else:  # Even page
                return self.config.even_header or self.config.header
        return self.config.header

    def _apply_header(
        self, page: fitz.Page, config: HeaderConfig, page_num: int, total_pages: int
    ) -> None:
        """Apply header to a page"""
        rect = page.rect
        y = rect.height - config.padding_top

        # Draw line if enabled
        if config.show_line:
            line_y = y - config.height + 5
            page.draw_line(
                (config.margin_left, line_y),
                (rect.width - config.margin_right, line_y),
                color=(
                    config.line_color[0] / 255,
                    config.line_color[1] / 255,
                    config.line_color[2] / 255,
                ),
                width=config.line_width,
            )

        # Draw logo if enabled
        x_pos = config.margin_left
        if config.show_logo and config.logo_path:
            try:
                logo_rect = fitz.Rect(
                    x_pos, y - config.logo_height - 5, x_pos + config.logo_width, y - 5
                )
                page.insert_image(logo_rect, filename=config.logo_path)
                x_pos += config.logo_width + 10
            except:
                pass

        # Draw title
        if config.show_title and config.title:
            page.insert_text(
                (x_pos, y - config.height / 2 + 4),
                config.title,
                fontsize=config.font_size,
                fontname=config.font_name,
                color=(config.color[0] / 255, config.color[1] / 255, config.color[2] / 255),
            )

        # Draw date (right aligned)
        if config.show_date:
            date_text = datetime.now().strftime(config.date_format)
            date_width = len(date_text) * config.font_size * 0.5
            page.insert_text(
                (rect.width - config.margin_right - date_width, y - config.height / 2 + 4),
                date_text,
                fontsize=config.font_size,
                fontname=config.font_name,
                color=(config.color[0] / 255, config.color[1] / 255, config.color[2] / 255),
            )

    def _apply_footer(
        self, page: fitz.Page, config: FooterConfig, page_num: int, total_pages: int
    ) -> None:
        """Apply footer to a page"""
        rect = page.rect
        y = config.padding_bottom + 10

        # Draw line if enabled
        if config.show_line:
            line_y = y + config.height - 10
            page.draw_line(
                (config.margin_left, line_y),
                (rect.width - config.margin_right, line_y),
                color=(
                    config.line_color[0] / 255,
                    config.line_color[1] / 255,
                    config.line_color[2] / 255,
                ),
                width=config.line_width,
            )

        color = (config.color[0] / 255, config.color[1] / 255, config.color[2] / 255)

        # Draw left text
        if config.left_text:
            page.insert_text(
                (config.margin_left, y),
                config.left_text,
                fontsize=config.font_size,
                fontname=config.font_name,
                color=color,
            )

        # Draw center text
        if config.center_text:
            center_width = len(config.center_text) * config.font_size * 0.5
            page.insert_text(
                ((rect.width - center_width) / 2, y),
                config.center_text,
                fontsize=config.font_size,
                fontname=config.font_name,
                color=color,
            )

        # Draw right text
        if config.right_text:
            right_width = len(config.right_text) * config.font_size * 0.5
            page.insert_text(
                (rect.width - config.margin_right - right_width, y),
                config.right_text,
                fontsize=config.font_size,
                fontname=config.font_name,
                color=color,
            )

        # Draw copyright
        if config.show_copyright:
            copyright_text = config.copyright_text.format(
                year=datetime.now().year, author=config.author
            )
            copyright_width = len(copyright_text) * config.font_size * 0.5
            page.insert_text(
                ((rect.width - copyright_width) / 2, y - 15),
                copyright_text,
                fontsize=config.font_size - 1,
                fontname=config.font_name,
                color=color,
            )


def apply_header_footer(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    title: str = "",
    author: str = "",
    copyright_text: str = "",
) -> Path:
    """Convenience function to apply header and footer"""
    header_config = HeaderConfig(title=title, show_title=bool(title), show_date=True)

    footer_config = FooterConfig(
        author=author,
        show_author=bool(author),
        show_copyright=bool(copyright_text),
        copyright_text=copyright_text if copyright_text else "© {year}",
    )

    config = HeaderFooterConfig(header=header_config, footer=footer_config)

    applier = HeaderFooterApplier(config)
    return applier.apply(input_path, output_path)


def apply_header_with_logo(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    logo_path: str,
    title: str = "",
    company: str = "",
) -> Path:
    """Apply header with company logo"""
    header_config = HeaderConfig(
        show_logo=True, logo_path=logo_path, title=company or title, show_title=True
    )

    config = HeaderFooterConfig(header=header_config)
    applier = HeaderFooterApplier(config)
    return applier.apply(input_path, output_path)
