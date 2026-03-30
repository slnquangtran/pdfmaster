"""
Main Document Designer class - orchestrates all PDF design operations
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Union, Dict, Any
from pathlib import Path
import fitz

from pdfmaster.src.design.decorators.watermark import (
    WatermarkConfig,
    WatermarkApplier,
    WatermarkType,
    PageRange,
)
from pdfmaster.src.design.decorators.stamp import (
    StampConfig,
    StampApplier,
    StampCategory,
    StampShape,
)
from pdfmaster.src.design.decorators.page_numbers import (
    PageNumberConfig,
    PageNumberApplier,
    PageNumberFormat,
    PageNumberPosition,
)
from pdfmaster.src.design.decorators.header_footer import (
    HeaderFooterConfig,
    HeaderFooterApplier,
    HeaderConfig,
    FooterConfig,
)
from pdfmaster.src.design.structure.toc import TOCConfig, TOCGenerator
from pdfmaster.src.design.structure.bookmark import BookmarkManager
from pdfmaster.src.design.styling.text import TextStyler


@dataclass
class DesignResult:
    """Result of a design operation"""

    success: bool
    message: str
    output_path: Optional[Path] = None
    pages_processed: int = 0


class DocumentDesigner:
    """Main class for designing PDF documents"""

    def __init__(self, document_path: Optional[Union[str, Path]] = None):
        self.document_path: Optional[Path] = None
        self._doc: Optional[fitz.Document] = None

        if document_path:
            self.load(document_path)

    def load(self, path: Union[str, Path]) -> "DocumentDesigner":
        """Load existing PDF document"""
        self.document_path = Path(path)
        if not self.document_path.exists():
            raise FileNotFoundError(f"PDF not found: {path}")

        self._doc = fitz.open(str(self.document_path))
        return self

    def create(self, pagesize: str = "A4", pages: int = 1) -> "DocumentDesigner":
        """Create new blank document"""
        self._doc = fitz.open()

        # Get page dimensions
        paper_sizes = {
            "A4": (595, 842),
            "Letter": (612, 792),
            "Legal": (612, 1008),
            "A3": (842, 1191),
            "A5": (420, 595),
        }

        width, height = paper_sizes.get(pagesize, (595, 842))

        for _ in range(pages):
            self._doc.new_page(width=width, height=height)

        return self

    def save(self, output_path: Union[str, Path]) -> Path:
        """Save document to file"""
        if not self._doc:
            raise RuntimeError("No document loaded or created")

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        self._doc.save(str(output_path))
        return output_path

    def close(self):
        """Close the document"""
        if self._doc:
            self._doc.close()
            self._doc = None

    @property
    def page_count(self) -> int:
        """Get number of pages"""
        return len(self._doc) if self._doc else 0

    @property
    def document(self) -> Optional[fitz.Document]:
        """Get underlying PyMuPDF document"""
        return self._doc

    # =========================================================================
    # Watermark Operations
    # =========================================================================

    def add_watermark(
        self,
        text: str = "DRAFT",
        watermark_type: WatermarkType = WatermarkType.DIAGONAL,
        opacity: float = 0.3,
        color: Tuple[int, int, int] = (192, 192, 192),
        font_size: int = 48,
        rotation: float = 45,
        pages: Union[str, List[int]] = "all",
    ) -> DesignResult:
        """Add watermark to document"""
        if not self._doc:
            return DesignResult(False, "No document loaded")

        try:
            # Determine page range
            if isinstance(pages, str):
                page_range_type = PageRange.ALL
                custom_pages = []
            else:
                page_range_type = PageRange.CUSTOM
                custom_pages = pages

            config = WatermarkConfig(
                watermark_type=watermark_type,
                text=text,
                opacity=opacity,
                color=color,
                font_size=font_size,
                rotation=rotation,
                page_range_type=page_range_type,
                custom_pages=custom_pages,
            )

            applier = WatermarkApplier(config)

            # Apply to in-memory document
            for page_num in range(len(self._doc)):
                if applier._should_apply_to_page(page_num, len(self._doc)):
                    page = self._doc[page_num]
                    applier._apply_watermark_to_page(page)

            return DesignResult(True, f"Watermark '{text}' applied", pages_processed=len(self._doc))
        except Exception as e:
            return DesignResult(False, f"Failed to apply watermark: {str(e)}")

    def add_image_watermark(
        self,
        image_path: Union[str, Path],
        opacity: float = 0.3,
        scale: float = 1.0,
        position: Tuple[float, float] = (0.5, 0.5),
    ) -> DesignResult:
        """Add image watermark to document"""
        if not self._doc:
            return DesignResult(False, "No document loaded")

        try:
            config = WatermarkConfig(
                watermark_type=WatermarkType.IMAGE,
                image_path=str(image_path),
                opacity=opacity,
                scale=scale,
                x=position[0],
                y=position[1],
            )

            applier = WatermarkApplier(config)

            for page_num in range(len(self._doc)):
                page = self._doc[page_num]
                applier._apply_image_watermark(page)

            return DesignResult(True, "Image watermark applied", pages_processed=len(self._doc))
        except Exception as e:
            return DesignResult(False, f"Failed to apply image watermark: {str(e)}")

    # =========================================================================
    # Stamp Operations
    # =========================================================================

    def add_stamp(
        self,
        stamp_name: str = "APPROVED",
        category: StampCategory = StampCategory.APPROVAL,
        shape: StampShape = StampShape.RECTANGLE,
        position: Tuple[float, float] = (0.75, 0.8),
        rotation: float = -15,
        pages: Optional[List[int]] = None,
    ) -> DesignResult:
        """Add stamp to document"""
        if not self._doc:
            return DesignResult(False, "No document loaded")

        try:
            config = StampConfig(
                stamp_name=stamp_name,
                category=category,
                shape=shape,
                x=position[0],
                y=position[1],
                rotation=rotation,
                pages=pages or list(range(1, len(self._doc) + 1)),
            )

            applier = StampApplier(config)

            for page_num in range(len(self._doc)):
                if (page_num + 1) in config.pages:
                    page = self._doc[page_num]
                    applier._apply_stamp_to_page(page)

            return DesignResult(
                True, f"Stamp '{stamp_name}' applied", pages_processed=len(config.pages)
            )
        except Exception as e:
            return DesignResult(False, f"Failed to apply stamp: {str(e)}")

    def add_custom_stamp(
        self,
        text: str,
        border_color: Tuple[int, int, int] = (0, 128, 0),
        fill_color: Tuple[int, int, int] = (255, 255, 255),
        position: Tuple[float, float] = (0.75, 0.8),
        size: Tuple[float, float] = (150, 60),
        pages: Optional[List[int]] = None,
    ) -> DesignResult:
        """Add custom text stamp to document"""
        if not self._doc:
            return DesignResult(False, "No document loaded")

        try:
            config = StampConfig(
                category=StampCategory.CUSTOM,
                custom_text=text,
                border_color=border_color,
                fill_color=fill_color,
                x=position[0],
                y=position[1],
                width=size[0],
                height=size[1],
                pages=pages or list(range(1, len(self._doc) + 1)),
            )

            applier = StampApplier(config)

            for page_num in range(len(self._doc)):
                if (page_num + 1) in config.pages:
                    page = self._doc[page_num]
                    applier._apply_stamp_to_page(page)

            return DesignResult(
                True, f"Custom stamp '{text}' applied", pages_processed=len(config.pages)
            )
        except Exception as e:
            return DesignResult(False, f"Failed to apply stamp: {str(e)}")

    # =========================================================================
    # Page Number Operations
    # =========================================================================

    def add_page_numbers(
        self,
        position: PageNumberPosition = PageNumberPosition.BOTTOM_CENTER,
        number_format: PageNumberFormat = PageNumberFormat.NUMERIC,
        font_size: int = 10,
        color: Tuple[int, int, int] = (0, 0, 0),
        show_total: bool = False,
        start_number: int = 1,
    ) -> DesignResult:
        """Add page numbers to document"""
        if not self._doc:
            return DesignResult(False, "No document loaded")

        try:
            config = PageNumberConfig(
                position=position,
                number_format=number_format,
                font_size=font_size,
                color=color,
                show_total=show_total,
                start_number=start_number,
            )

            applier = PageNumberApplier(config)

            for page_num in range(len(self._doc)):
                page_number = page_num + start_number
                applier._apply_page_number(page, page_num, page_number, len(self._doc))

            return DesignResult(True, "Page numbers added", pages_processed=len(self._doc))
        except Exception as e:
            return DesignResult(False, f"Failed to add page numbers: {str(e)}")

    def add_custom_page_numbers(
        self,
        template: str = "Page {number} of {total}",
        position: PageNumberPosition = PageNumberPosition.BOTTOM_CENTER,
        font_size: int = 10,
        color: Tuple[int, int, int] = (0, 0, 0),
    ) -> DesignResult:
        """Add custom formatted page numbers"""
        if not self._doc:
            return DesignResult(False, "No document loaded")

        try:
            config = PageNumberConfig(
                position=position,
                template=template,
                font_size=font_size,
                color=color,
                show_total=True,
            )

            applier = PageNumberApplier(config)

            for page_num in range(len(self._doc)):
                page_number = page_num + 1
                applier._apply_page_number(page, page_num, page_number, len(self._doc))

            return DesignResult(
                True, f"Custom page numbers added: {template}", pages_processed=len(self._doc)
            )
        except Exception as e:
            return DesignResult(False, f"Failed to add page numbers: {str(e)}")

    # =========================================================================
    # Header/Footer Operations
    # =========================================================================

    def add_header_footer(
        self,
        header_title: str = "",
        footer_text: str = "",
        show_date: bool = True,
        show_line: bool = True,
    ) -> DesignResult:
        """Add header and footer to document"""
        if not self._doc:
            return DesignResult(False, "No document loaded")

        try:
            header_config = HeaderConfig(
                title=header_title,
                show_title=bool(header_title),
                show_date=show_date,
                show_line=show_line,
            )

            footer_config = FooterConfig(center_text=footer_text, show_line=show_line)

            config = HeaderFooterConfig(
                header=header_config,
                footer=footer_config,
                apply_to_first_page=False,  # Don't apply to cover page
            )

            applier = HeaderFooterApplier(config)

            for page_num in range(len(self._doc)):
                if page_num > 0:  # Skip first page
                    page = self._doc[page_num]
                    applier._apply_header(page, header_config, page_num, len(self._doc))
                    applier._apply_footer(page, footer_config, page_num, len(self._doc))

            return DesignResult(True, "Header and footer added", pages_processed=len(self._doc) - 1)
        except Exception as e:
            return DesignResult(False, f"Failed to add header/footer: {str(e)}")

    def add_header_with_logo(
        self, logo_path: Union[str, Path], title: str = "", show_date: bool = True
    ) -> DesignResult:
        """Add header with logo to document"""
        if not self._doc:
            return DesignResult(False, "No document loaded")

        try:
            header_config = HeaderConfig(
                show_logo=True,
                logo_path=str(logo_path),
                title=title,
                show_title=bool(title),
                show_date=show_date,
            )

            for page_num in range(len(self._doc)):
                if page_num > 0:  # Skip first page
                    page = self._doc[page_num]
                    applier = HeaderFooterApplier(HeaderFooterConfig(header=header_config))
                    applier._apply_header(page, header_config, page_num, len(self._doc))

            return DesignResult(True, "Header with logo added", pages_processed=len(self._doc) - 1)
        except Exception as e:
            return DesignResult(False, f"Failed to add header: {str(e)}")

    # =========================================================================
    # Table of Contents Operations
    # =========================================================================

    def generate_toc(
        self, title: str = "Table of Contents", insert_toc_page: bool = True, max_depth: int = 3
    ) -> DesignResult:
        """Generate table of contents from document headings"""
        if not self._doc:
            return DesignResult(False, "No document loaded")

        try:
            # Get existing TOC/bookmarks from document
            existing_toc = self._doc.get_toc()

            config = TOCConfig(title=title, insert_toc_page=insert_toc_page, max_depth=max_depth)

            generator = TOCGenerator(config)

            # Add entries from existing TOC
            for item in existing_toc:
                level, title_text, page_num = item[0], item[1], item[2]
                generator.add_entry(level, title_text, page_num)

            # Generate and save to temp file, then reload
            import tempfile

            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp_path = tmp.name

            generator.save(self._doc, tmp_path)

            # Reload the document
            self._doc.close()
            self._doc = fitz.open(tmp_path)
            Path(tmp_path).unlink()

            return DesignResult(True, "Table of contents generated", pages_processed=1)
        except Exception as e:
            return DesignResult(False, f"Failed to generate TOC: {str(e)}")

    # =========================================================================
    # Bookmark Operations
    # =========================================================================

    def add_bookmarks(self, entries: List[Tuple[str, int]]) -> DesignResult:
        """Add bookmarks to document"""
        if not self._doc:
            return DesignResult(False, "No document loaded")

        try:
            manager = BookmarkManager()

            for title, page in entries:
                manager.add_chapter(title, page)

            manager.save_to_document(self._doc)

            return DesignResult(
                True, f"Added {len(entries)} bookmarks", pages_processed=len(entries)
            )
        except Exception as e:
            return DesignResult(False, f"Failed to add bookmarks: {str(e)}")

    def import_bookmarks(self) -> DesignResult:
        """Import and recreate existing bookmarks"""
        if not self._doc:
            return DesignResult(False, "No document loaded")

        try:
            manager = BookmarkManager()
            manager.load_from_document(self._doc)

            # Clear and re-add
            self._doc.set_toc([])
            manager.save_to_document(self._doc)

            return DesignResult(True, f"Imported {len(manager)} bookmarks")
        except Exception as e:
            return DesignResult(False, f"Failed to import bookmarks: {str(e)}")

    # =========================================================================
    # Utility Operations
    # =========================================================================

    def get_page_info(self, page_num: int = 0) -> Dict[str, Any]:
        """Get information about a page"""
        if not self._doc or page_num >= len(self._doc):
            return {}

        page = self._doc[page_num]
        return {
            "page_number": page_num + 1,
            "width": page.rect.width,
            "height": page.rect.height,
            "rotation": page.rotation,
            "text": page.get_text()[:500],  # First 500 chars
        }

    def get_document_info(self) -> Dict[str, Any]:
        """Get document information"""
        if not self._doc:
            return {}

        return {
            "page_count": len(self._doc),
            "metadata": self._doc.metadata,
            "is_encrypted": self._doc.is_encrypted,
            "is_pdf": self._doc.is_pdf,
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
