import os
from pathlib import Path
from pdfmaster.src.cli import main as cli_main
from pdfmaster.src.core.creator import PDFCreator
from click.testing import CliRunner


def _make_pdf(path: Path, title: str, text: str):
    creator = PDFCreator(title=title, author="UnitTest")
    creator.add_text(text, x=72, y=700, font_size=12)
    creator.save(str(path))


def test_merge_and_split_roundtrip(tmp_path: Path):  # type: ignore
    # Create two small PDFs
    p1 = tmp_path / "one.pdf"
    p2 = tmp_path / "two.pdf"
    _make_pdf(p1, "Doc1", "Hello from doc 1")
    _make_pdf(p2, "Doc2", "Hello from doc 2")

    runner = CliRunner()
    merged = tmp_path / "merged.pdf"
    r1 = runner.invoke(cli_main, ["merge", str(p1), str(p2), "-o", str(merged)])
    assert r1.exit_code == 0
    assert merged.exists()

    # Split the merged PDF into two pages
    split_dir = tmp_path / "split_out"
    r2 = runner.invoke(cli_main, ["split", str(merged), "--output-dir", str(split_dir), "--pages", "1-2"])
    assert r2.exit_code == 0
    # Expect two files
    f1 = split_dir / f"{merged.stem}_page_1.pdf"
    f2 = split_dir / f"{merged.stem}_page_2.pdf"
    assert f1.exists()
    assert f2.exists()
