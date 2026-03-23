import logging
from pathlib import Path
from typing import Optional, List, Tuple, Union

import fitz

logger = logging.getLogger(__name__)


class PDFEditor:
    def __init__(self, input_path: Union[str, Path]):
        if isinstance(input_path, str):
            input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"PDF file not found: {input_path}")

        self.input_path = input_path
        self._document: Optional[fitz.Document] = None
        self._pages: List[dict] = []

    def open(self) -> "PDFEditor":
        self._document = fitz.open(str(self.input_path))
        for page_num in range(len(self._document)):
            page = self._document[page_num]
            self._pages.append(
                {
                    "page_num": page_num,
                    "width": page.rect.width,
                    "height": page.rect.height,
                    "text": page.get_text(),
                }
            )
        logger.info(f"Opened PDF: {self.input_path} ({len(self._pages)} pages)")
        return self

    def get_page_text(self, page_num: int = 0) -> str:
        if self._document is None:
            raise RuntimeError("PDF not opened. Call open() first.")
        return self._document[page_num].get_text()

    def get_all_text(self) -> str:
        if self._document is None:
            raise RuntimeError("PDF not opened. Call open() first.")
        text = ""
        for page in self._document:
            text += page.get_text()
        return text

    def replace_text(
        self,
        old_text: str,
        new_text: str,
        page_num: Optional[int] = None,
    ) -> int:
        if self._document is None:
            raise RuntimeError("PDF not opened. Call open() first.")

        replacements = 0
        pages = (
            [self._document[page_num]] if page_num is not None else self._document
        )

        for page in pages:
            text_instances = page.search_for(old_text)
            for inst in text_instances:
                page.draw_rect(inst, color=(1, 1, 1), fill=(1, 1, 1))
                page.insert_text(
                    inst.tl,
                    new_text,
                    fontsize=12,
                    color=(0, 0, 0),
                )
                replacements += 1

        logger.info(f"Replaced {replacements} instances of text")
        return replacements

    def add_text(
        self,
        text: str,
        x: float = 72,
        y: float = 720,
        page_num: int = 0,
        font_size: float = 12,
    ) -> "PDFEditor":
        if self._document is None:
            raise RuntimeError("PDF not opened. Call open() first.")

        if page_num >= len(self._document):
            raise ValueError(f"Page {page_num} does not exist")

        page = self._document[page_num]
        page.insert_text((x, y), text, fontsize=font_size, color=(0, 0, 0))
        return self

    def add_image(
        self,
        image_path: Union[str, Path],
        x: float = 72,
        y: float = 400,
        width: Optional[float] = None,
        height: Optional[float] = None,
        page_num: int = 0,
    ) -> "PDFEditor":
        if self._document is None:
            raise RuntimeError("PDF not opened. Call open() first.")

        if not Path(image_path).exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        page = self._document[page_num]
        page.insert_image(fitz.Rect(x, y, x + (width or 200), y + (height or 200)), filename=str(image_path))
        return self

    def add_page(self, after_page: Optional[int] = None) -> int:
        if self._document is None:
            raise RuntimeError("PDF not opened. Call open() first.")

        new_page_num = self._document.new_page(
            width=612, height=792
        )
        logger.info(f"Added new page at position {new_page_num}")
        return new_page_num

    def delete_page(self, page_num: int) -> "PDFEditor":
        if self._document is None:
            raise RuntimeError("PDF not opened. Call open() first.")

        if page_num >= len(self._document):
            raise ValueError(f"Page {page_num} does not exist")

        self._document.delete_page(page_num)
        logger.info(f"Deleted page {page_num}")
        return self

    def save(self, output_path: Union[str, Path]) -> Path:
        if self._document is None:
            raise RuntimeError("PDF not opened. Call open() first.")

        if isinstance(output_path, str):
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        self._document.save(str(output_path))
        logger.info(f"Saved PDF: {output_path}")
        return output_path

    def close(self):
        if self._document is not None:
            self._document.close()
            self._document = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def page_count(self) -> int:
        if self._document is None:
            return 0
        return len(self._document)

    @property
    def is_encrypted(self) -> bool:
        if self._document is None:
            return False
        return self._document.is_encrypted
