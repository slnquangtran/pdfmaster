import os
from pathlib import Path
from pdfmaster.src.core.creator import PDFCreator
from click.testing import CliRunner
import pytest

def _make_pdf(tmp_dir, name="edge_case.pdf", text="Edge Case"):
    p = Path(tmp_dir) / name
    creator = PDFCreator(title="Edge", author="Tester")
    creator.add_text(text, x=72, y=700, font_size=12)
    creator.save(str(p))
    return p

def _make_multi_page_pdf(tmp_dir, name="multi_page.pdf"):
    p = Path(tmp_dir) / name
    from pdfmaster.src.core.creator import PDFCreator
    creator = PDFCreator(title="MultiPage", author="Tester")
    creator.add_text("Page 1", x=72, y=700, font_size=12)
    creator.new_page()
    creator.add_text("Page 2", x=72, y=700, font_size=12)
    creator.new_page()
    creator.add_text("Page 3", x=72, y=700, font_size=12)
    creator.save(str(p))
    return p


def test_merge_no_inputs_error():
    runner = CliRunner()
    from pdfmaster.src.cli import main as cli_main
    result = runner.invoke(cli_main, ["merge", "-o", "out.pdf"])
    assert result.exit_code != 0
    assert "No input PDFs provided" in (result.output or "")


def test_split_nonexistent_input_error():
    runner = CliRunner()
    from pdfmaster.src.cli import main as cli_main
    result = runner.invoke(cli_main, ["split", "nonexistent.pdf", "-o", "outdir"])
    assert result is not None
    assert result.exit_code != 0


def test_preview_text_cli(tmp_path):
    pdf = _make_pdf(tmp_path, name="preview.pdf", text="Preview test content")
    runner = CliRunner()
    from pdfmaster.src.cli import main as cli_main
    result = runner.invoke(cli_main, ["preview-text", str(pdf), "--chars", "20"])
    assert result.exit_code == 0
    assert isinstance(result.output, str)
    assert len(result.output.strip()) <= 20


def test_export_page_image_cli(tmp_path):
    pdf = _make_pdf(tmp_path, name="page_export.pdf", text="Page export test")
    out_dir = tmp_path / "images"
    runner = CliRunner()
    from pdfmaster.src.cli import main as cli_main
    result = runner.invoke(cli_main, ["export-page-image", str(pdf), "--output-dir", str(out_dir), "--page", "1"])
    assert result.exit_code == 0
    assert (out_dir / f"{Path(pdf).stem}_page_1.png").exists()


def test_watermark_cli(tmp_path):
    pdf = _make_pdf(tmp_path, name="watermark.pdf", text="Watermark test")
    out = tmp_path / "watermarked.pdf"
    runner = CliRunner()
    from pdfmaster.src.cli import main as cli_main
    result = runner.invoke(cli_main, ["watermark", str(pdf), str(out), "--text", "CONFIDENTIAL"])
    assert result.exit_code == 0
    assert out.exists()
def test_export_all_pages_image_cli(tmp_path):
    # Create a 3-page PDF
    pdf = _make_multi_page_pdf(tmp_path, name="multi_page.pdf")
    out_dir = tmp_path / "all_pages_images"
    runner = CliRunner()
    from pdfmaster.src.cli import main as cli_main
    result = runner.invoke(cli_main, ["export-all-pages-image", str(pdf), "-o", str(out_dir)])
    assert result.exit_code == 0
    pngs = [f for f in os.listdir(out_dir) if f.endswith('.png')]
    assert len(pngs) == 3
