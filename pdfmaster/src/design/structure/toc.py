"""
Table of contents (TOC) generator for PDF documents
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Union, Dict
from pathlib import Path
import fitz


@dataclass
class TOCEntry:
    """Single TOC entry"""

    level: int  # 1 = chapter, 2 = section, etc.
    title: str
    page_number: int
    children: List["TOCEntry"] = field(default_factory=list)
    color: Optional[Tuple[int, int, int]] = None


@dataclass
class TOCStyle:
    """Style for a TOC level"""

    font_name: str = "Helvetica"
    font_size: int = 12
    color: Tuple[int, int, int] = (0, 0, 0)
    indent: float = 20
    bold: bool = False


@dataclass
class TOCConfig:
    """Configuration for table of contents"""

    # Title
    title: str = "Table of Contents"
    title_font_size: int = 18
    title_font_name: str = "Helvetica-Bold"

    # Styling
    default_style: TOCStyle = field(default_factory=TOCStyle)
    level_styles: Dict[int, TOCStyle] = field(default_factory=dict)

    # Layout
    indent_per_level: float = 20
    line_spacing: float = 1.5
    show_dots: bool = True
    dot_character: str = "."

    # Page settings
    insert_toc_page: bool = True
    toc_page_position: int = 0  # 0 = first page
    max_depth: int = 3

    # Auto-generation
    auto_generate_from_headings: bool = True


class TOCGenerator:
    """Generate table of contents for PDF documents"""

    def __init__(self, config: Optional[TOCConfig] = None):
        self.config = config or TOCConfig()
        self.entries: List[TOCEntry] = []

    def add_entry(self, level: int, title: str, page_number: int) -> TOCGenerator:
        """Add a TOC entry"""
        entry = TOCEntry(level=level, title=title, page_number=page_number)
        self.entries.append(entry)
        return self

    def add_entries_from_bookmarks(self, doc: fitz.Document) -> TOCGenerator:
        """Generate TOC entries from document bookmarks/outline"""
        toc = doc.get_toc()

        for item in toc:
            level, title, page_num = item[0], item[1], item[2]
            self.add_entry(level, title, page_num)

        return self

    def generate(self, input_path: Union[str, Path], output_path: Union[str, Path]) -> Path:
        """Generate TOC and insert into PDF"""
        input_path = Path(input_path)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        doc = fitz.open(str(input_path))

        try:
            # Create TOC page
            if self.config.insert_toc_page:
                toc_page = doc.new_page(width=doc[0].rect.width, height=doc[0].rect.height)

                # Move TOC page to desired position
                if self.config.toc_page_position > 0:
                    doc.move_page(len(doc) - 1, self.config.toc_page_position)

                # Render TOC on page
                self._render_toc_page(toc_page, doc)

            # Add bookmarks
            self._add_bookmarks(doc)

            doc.save(str(output_path))
            return output_path
        finally:
            doc.close()

    def _render_toc_page(self, page: fitz.Page, doc: fitz.Document) -> None:
        """Render TOC content on page"""
        config = self.config
        rect = page.rect

        # Draw title
        y = rect.height - 100
        page.insert_text(
            (72, y),
            config.title,
            fontsize=config.title_font_size,
            fontname=config.title_font_name,
            color=(0, 0, 0),
        )

        # Draw separator line
        y += 10
        page.draw_line((72, y), (rect.width - 72, y), color=(0, 0, 0), width=1)

        # Draw entries
        y += 30

        for entry in self.entries:
            if entry.level > config.max_depth:
                continue

            # Get style for this level
            style = config.level_styles.get(entry.level, config.default_style)

            # Calculate indent
            indent = (entry.level - 1) * config.indent_per_level
            x = 72 + indent

            # Get font name
            font_name = style.font_name
            if entry.level == 1:
                font_name = "Helvetica-Bold"
            elif entry.level == 2:
                font_name = "Helvetica"

            # Draw entry text
            page.insert_text(
                (x, y),
                entry.title,
                fontsize=style.font_size,
                fontname=font_name,
                color=(style.color[0] / 255, style.color[1] / 255, style.color[2] / 255),
            )

            # Draw page number with dot leaders
            if config.show_dots:
                page_number_text = str(entry.page_number)
                page_number_width = len(page_number_text) * style.font_size * 0.5
                entry_width = len(entry.title) * style.font_size * 0.5

                # Calculate dot area
                dot_start_x = x + entry_width + 10
                dot_end_x = rect.width - 72 - page_number_width - 10

                # Draw dots
                if dot_end_x > dot_start_x:
                    dot_spacing = style.font_size * 0.5
                    dot_x = dot_start_x
                    while dot_x < dot_end_x:
                        page.insert_text((dot_x, y), ".", fontsize=style.font_size * 0.5)
                        dot_x += dot_spacing

            # Draw page number
            page_number_text = str(entry.page_number)
            page_number_width = len(page_number_text) * style.font_size * 0.5
            page.insert_text(
                (rect.width - 72 - page_number_width, y),
                page_number_text,
                fontsize=style.font_size,
                fontname=font_name,
                color=(style.color[0] / 255, style.color[1] / 255, style.color[2] / 255),
            )

            # Move to next line
            y += style.font_size * config.line_spacing

            # Check if we need a new page
            if y > rect.height - 72:
                # Add new TOC page
                page = doc.new_page(width=rect.width, height=rect.height)
                y = 100

    def _add_bookmarks(self, doc: fitz.Document) -> None:
        """Add bookmarks to document based on TOC entries"""
        for entry in self.entries:
            if entry.level > self.config.max_depth:
                continue

            # PyMuPDF bookmark format: [level, title, page_number]
            doc.set_toc([[entry.level, entry.title, entry.page_number]])


def generate_toc(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    entries: Optional[List[Tuple[int, str, int]]] = None,
    title: str = "Table of Contents",
    from_bookmarks: bool = True,
) -> Path:
    """Convenience function to generate TOC"""
    config = TOCConfig(title=title)
    generator = TOCGenerator(config)

    if entries:
        for level, title, page in entries:
            generator.add_entry(level, title, page)

    if from_bookmarks:
        doc = fitz.open(str(input_path))
        try:
            generator.add_entries_from_bookmarks(doc)
        finally:
            doc.close()

    return generator.generate(input_path, output_path)
