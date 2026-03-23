import logging
from pathlib import Path
from typing import Union, List, Optional

import fitz

logger = logging.getLogger(__name__)


class TextExtractor:
    def __init__(self, preserve_formatting: bool = True):
        self.preserve_formatting = preserve_formatting

    def extract(self, input_path: Union[str, Path]) -> str:
        if isinstance(input_path, str):
            input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"PDF file not found: {input_path}")

        doc = fitz.open(str(input_path))
        
        if doc.is_encrypted:
            doc.close()
            raise ValueError("PDF is encrypted")

        text_parts = []

        for page_num in range(len(doc)):
            page = doc[page_num]

            if self.preserve_formatting:
                text = self._extract_with_formatting(page)
            else:
                text = page.get_text()

            if text.strip():
                text_parts.append(f"--- Page {page_num + 1} ---\n{text}")

        doc.close()

        result = "\n\n".join(text_parts)
        logger.info(f"Extracted text from {len(doc)} pages")
        return result

    def _extract_with_formatting(self, page: fitz.Page) -> str:
        blocks = page.get_text("dict")["blocks"]
        text_lines = []

        for block in blocks:
            if block["type"] == 0:
                block_text = ""
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text = span.get("text", "")
                        block_text += text
                    block_text += "\n"
                if block_text.strip():
                    text_lines.append(block_text.strip())

        return "\n\n".join(text_lines)

    def extract_page(self, input_path: Union[str, Path], page_num: int) -> str:
        if isinstance(input_path, str):
            input_path = Path(input_path)

        doc = fitz.open(str(input_path))
        
        if page_num >= len(doc):
            doc.close()
            raise ValueError(f"Page {page_num} does not exist")

        page = doc[page_num]
        text = page.get_text()
        doc.close()

        return text

    def extract_to_file(
        self, input_path: Union[str, Path], output_path: Union[str, Path]
    ):
        text = self.extract(input_path)
        
        if isinstance(output_path, str):
            output_path = Path(output_path)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        
        logger.info(f"Saved extracted text to {output_path}")
        return output_path
