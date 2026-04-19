import os
import tempfile
from pdfmaster.src.core.creator import PDFCreator
from pdfmaster.src.watermark import add_watermark


def test_watermark_basic_roundtrip():
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, "src.pdf")
        out_path = os.path.join(tmpdir, "watermarked.pdf")
        creator = PDFCreator(title="Test Watermark", author="UnitTest")
        creator.add_text("Watermark Test", x=72, y=700, font_size=12)
        creator.save(pdf_path)

        add_watermark(pdf_path, out_path, "CONFIDENTIAL")
        assert os.path.exists(out_path)
