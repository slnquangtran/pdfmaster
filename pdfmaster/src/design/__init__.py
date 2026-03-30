"""
PDF Design Module

Provides comprehensive PDF design capabilities including:
- Design elements (text, images, shapes)
- Page decorators (watermarks, stamps, headers, footers)
- Document structure (TOC, bookmarks)
- Annotations
"""

from pdfmaster.src.design.elements.base import DesignElement, Rectangle, TextStyle
from pdfmaster.src.design.elements.text import TextElement
from pdfmaster.src.design.elements.image import ImageElement
from pdfmaster.src.design.elements.shapes import ShapeElement, LineElement
from pdfmaster.src.design.decorators.watermark import WatermarkConfig, WatermarkApplier
from pdfmaster.src.design.decorators.stamp import StampConfig, StampApplier
from pdfmaster.src.design.decorators.page_numbers import PageNumberConfig, PageNumberApplier
from pdfmaster.src.design.decorators.header_footer import HeaderFooterConfig, HeaderFooterApplier
from pdfmaster.src.design.structure.toc import TOCConfig, TOCGenerator
from pdfmaster.src.design.structure.bookmark import BookmarkManager
from pdfmaster.src.design.styling.text import TextStyler
from pdfmaster.src.design.designer import DocumentDesigner

__all__ = [
    "DesignElement",
    "Rectangle",
    "TextStyle",
    "TextElement",
    "ImageElement",
    "ShapeElement",
    "LineElement",
    "WatermarkConfig",
    "WatermarkApplier",
    "StampConfig",
    "StampApplier",
    "PageNumberConfig",
    "PageNumberApplier",
    "HeaderFooterConfig",
    "HeaderFooterApplier",
    "TOCConfig",
    "TOCGenerator",
    "BookmarkManager",
    "TextStyler",
    "DocumentDesigner",
]
