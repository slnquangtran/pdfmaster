import os
import tempfile
from pdfmaster.src.core.creator import PDFCreator
from pdfmaster.src.extractors.text_extractor import TextExtractor


def test_text_extractor_basic_roundtrip():
    # Create a simple PDF with some text and ensure we can extract it back
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, "test_input.pdf")
        output_path = os.path.join(tmpdir, "extracted.txt")

        creator = PDFCreator(title="Test", author="UnitTest")
        creator.add_text("Hello, world!", x=72, y=700, font_size=12)
        creator.save(pdf_path)

        extractor = TextExtractor()
        text = extractor.extract(pdf_path)

        assert isinstance(text, str)
        assert "Hello" in text
