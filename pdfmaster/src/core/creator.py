import logging
from pathlib import Path
from typing import Optional, List, Tuple, Union

from reportlab.lib.pagesizes import A4, letter, legal
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors

logger = logging.getLogger(__name__)

PAGE_SIZES = {
    "A4": A4,
    "Letter": letter,
    "Legal": legal,
}


class PDFCreator:
    def __init__(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        page_size: str = "A4",
    ):
        self.title = title
        self.author = author
        self.page_size = page_size
        self._pages: List[dict] = []
        self._current_page: Optional[dict] = None
        self._canvas: Optional[canvas.Canvas] = None
        self._output_path: Optional[Path] = None

    def new_page(self):
        if self._current_page is not None:
            self._pages.append(self._current_page)
        self._current_page = {"elements": []}
        return self

    def add_text(
        self,
        text: str,
        x: float = 72,
        y: float = 720,
        font_size: float = 12,
        font_name: str = "Helvetica",
        font_color: Tuple[int, int, int] = (0, 0, 0),
    ):
        if self._current_page is None:
            self.new_page()
        self._current_page["elements"].append(
            {
                "type": "text",
                "text": text,
                "x": x,
                "y": y,
                "font_size": font_size,
                "font_name": font_name,
                "font_color": font_color,
            }
        )
        return self

    def add_image(
        self,
        image_path: Union[str, Path],
        x: float = 72,
        y: float = 400,
        width: Optional[float] = None,
        height: Optional[float] = None,
    ):
        if self._current_page is None:
            self.new_page()
        self._current_page["elements"].append(
            {
                "type": "image",
                "path": image_path,
                "x": x,
                "y": y,
                "width": width,
                "height": height,
            }
        )
        return self

    def add_shape(
        self,
        shape_type: str,
        x: float,
        y: float,
        width: float,
        height: float,
        fill_color: Optional[Tuple[int, int, int]] = None,
        stroke_color: Optional[Tuple[int, int, int]] = (0, 0, 0),
        stroke_width: float = 1,
    ):
        if self._current_page is None:
            self.new_page()
        self._current_page["elements"].append(
            {
                "type": "shape",
                "shape_type": shape_type,
                "x": x,
                "y": y,
                "width": width,
                "height": height,
                "fill_color": fill_color,
                "stroke_color": stroke_color,
                "stroke_width": stroke_width,
            }
        )
        return self

    def save(self, output_path: Union[str, Path]):
        if isinstance(output_path, str):
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        if self._current_page is not None:
            self._pages.append(self._current_page)

        if not self._pages:
            self.new_page()

        c = canvas.Canvas(str(output_path), pagesize=PAGE_SIZES[self.page_size])
        self._canvas = c

        if self.title:
            c.setTitle(self.title)
        if self.author:
            c.setAuthor(self.author)

        page_width, page_height = PAGE_SIZES[self.page_size]

        for page in self._pages:
            for elem in page.get("elements", []):
                if elem["type"] == "text":
                    c.setFont(elem["font_name"], elem["font_size"])
                    r, g, b = elem["font_color"]
                    c.setFillColor(colors.Color(r / 255, g / 255, b / 255))
                    c.drawString(elem["x"], elem["y"], elem["text"])

                elif elem["type"] == "image":
                    from reportlab.lib.utils import ImageReader

                    img = ImageReader(str(elem["path"]))
                    img_width, img_height = img.getSize()
                    width = elem.get("width") or (img_width / 2)
                    height = elem.get("height") or (img_height / 2)
                    c.drawImage(img, elem["x"], elem["y"], width=width, height=height)

                elif elem["type"] == "shape":
                    r, g, b = elem["stroke_color"]
                    c.setStrokeColor(colors.Color(r / 255, g / 255, b / 255))
                    c.setLineWidth(elem["stroke_width"])

                    if elem.get("fill_color"):
                        r, g, b = elem["fill_color"]
                        c.setFillColor(colors.Color(r / 255, g / 255, b / 255))

                    shape_type = elem["shape_type"]
                    x, y, w, h = elem["x"], elem["y"], elem["width"], elem["height"]

                    if shape_type == "rectangle":
                        if elem.get("fill_color"):
                            c.rect(x, y, w, h, stroke=1, fill=1)
                        else:
                            c.rect(x, y, w, h, stroke=1, fill=0)

                    elif shape_type == "line":
                        c.line(x, y, x + w, y + h)

                    elif shape_type == "circle":
                        c.circle(x, y, w / 2, stroke=1, fill=0)

            c.showPage()

        c.save()
        self._output_path = output_path
        logger.info(f"PDF created: {output_path}")
        return output_path
