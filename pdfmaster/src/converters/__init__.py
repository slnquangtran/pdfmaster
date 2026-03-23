import logging
import subprocess
import sys
from pathlib import Path
from typing import Union

from pdfmaster.src.converters.base import BaseConverter

logger = logging.getLogger(__name__)


class DOCXConverter(BaseConverter):
    def convert(
        self, input_path: Union[str, Path], output_path: Union[str, Path]
    ) -> Path:
        input_path = self.validate_input(input_path)
        if isinstance(output_path, str):
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            from docx2pdf import convert

            convert(str(input_path), str(output_path))
            logger.info(f"Converted DOCX to PDF: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"DOCX conversion failed: {e}")
            if sys.platform == "win32":
                raise
            logger.warning("docx2pdf failed, trying LibreOffice fallback")
            return self._convert_with_libreoffice(input_path, output_path)

    def _convert_with_libreoffice(
        self, input_path: Path, output_path: Path
    ) -> Path:
        try:
            result = subprocess.run(
                [
                    "libreoffice",
                    "--headless",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    str(output_path.parent),
                    str(input_path),
                ],
                capture_output=True,
                timeout=60,
            )
            if result.returncode == 0:
                logger.info(f"Converted with LibreOffice: {output_path}")
                return output_path
            raise RuntimeError(f"LibreOffice conversion failed: {result.stderr}")
        except FileNotFoundError:
            raise RuntimeError(
                "Neither docx2pdf (requires MS Word) nor LibreOffice is available"
            )


class ImageConverter(BaseConverter):
    SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"}

    def convert(
        self, input_path: Union[str, Path], output_path: Union[str, Path]
    ) -> Path:
        input_path = self.validate_input(input_path)
        if isinstance(output_path, str):
            output_path = Path(output_path)

        ext = input_path.suffix.lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported image format: {ext}")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        from PIL import Image
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter

        img = Image.open(input_path)
        c = canvas.Canvas(str(output_path), pagesize=letter)
        width, height = letter

        img_width, img_height = img.size
        aspect = img_height / img_width

        draw_width = width - 100
        draw_height = draw_width * aspect

        if draw_height > height - 100:
            draw_height = height - 100
            draw_width = draw_height / aspect

        c.draw_image(
            str(input_path),
            50,
            height - 50 - draw_height,
            width=draw_width,
            height=draw_height,
        )
        c.save()

        logger.info(f"Converted image to PDF: {output_path}")
        return output_path


class TXTConverter(BaseConverter):
    def convert(
        self, input_path: Union[str, Path], output_path: Union[str, Path]
    ) -> Path:
        input_path = self.validate_input(input_path)
        if isinstance(output_path, str):
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()

        c = canvas.Canvas(str(output_path), pagesize=letter)
        width, height = letter

        y = height - 50
        margin = 50
        line_height = 14

        for line in content.split("\n"):
            if y < margin:
                c.showPage()
                y = height - margin

            if len(line) > 80:
                words = line.split()
                line = ""
                for word in words:
                    if len(line) + len(word) > 80:
                        c.drawString(margin, y, line)
                        y -= line_height
                        line = ""
                    line += word + " "
                if line:
                    c.drawString(margin, y, line.strip())
                    y -= line_height
            else:
                c.drawString(margin, y, line)
                y -= line_height

        c.save()
        logger.info(f"Converted TXT to PDF: {output_path}")
        return output_path


class HTMLConverter(BaseConverter):
    def convert(
        self, input_path: Union[str, Path], output_path: Union[str, Path]
    ) -> Path:
        input_path = self.validate_input(input_path)
        if isinstance(output_path, str):
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            from weasyprint import HTML

            HTML(filename=str(input_path)).write_pdf(str(output_path))
            logger.info(f"Converted HTML to PDF: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"HTML conversion failed: {e}")
            raise


class XLSXConverter(BaseConverter):
    def convert(
        self, input_path: Union[str, Path], output_path: Union[str, Path]
    ) -> Path:
        input_path = self.validate_input(input_path)
        if isinstance(output_path, str):
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            import subprocess

            result = subprocess.run(
                [
                    "libreoffice",
                    "--headless",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    str(output_path.parent),
                    str(input_path),
                ],
                capture_output=True,
                timeout=120,
            )
            if result.returncode == 0:
                logger.info(f"Converted XLSX to PDF: {output_path}")
                return output_path
            raise RuntimeError(f"LibreOffice conversion failed: {result.stderr}")

        except FileNotFoundError:
            raise RuntimeError("LibreOffice is required for XLSX conversion")


def convert_file(input_path: Union[str, Path], output_path: Union[str, Path]) -> Path:
    input_path = Path(input_path) if isinstance(input_path, str) else input_path
    output_path = Path(output_path) if isinstance(output_path, str) else output_path

    ext = input_path.suffix.lower()

    if ext in {".docx", ".doc"}:
        return DOCXConverter().convert(input_path, output_path)
    elif ext in {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"}:
        return ImageConverter().convert(input_path, output_path)
    elif ext == ".txt":
        return TXTConverter().convert(input_path, output_path)
    elif ext in {".html", ".htm"}:
        return HTMLConverter().convert(input_path, output_path)
    elif ext in {".xlsx", ".xls"}:
        return XLSXConverter().convert(input_path, output_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
