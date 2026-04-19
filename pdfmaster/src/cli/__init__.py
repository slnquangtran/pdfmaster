import click
from pdfmaster.src.utils import setup_logging

logger = setup_logging()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """PDF Master Suite - Comprehensive PDF tools for creation, editing, and conversion."""
    pass


@main.command()
@click.option("--output", "-o", required=True, help="Output PDF file path")
@click.option("--title", help="Document title")
@click.option("--author", help="Document author")
@click.option(
    "--page-size",
    default="A4",
    type=click.Choice(["A4", "Letter", "Legal"]),
    help="Page size",
)
def create(output: str, title: str, author: str, page_size: str):
    """Create a new PDF document."""
    from pdfmaster.src.core.creator import PDFCreator

    try:
        creator = PDFCreator(title=title, author=author, page_size=page_size)
        creator.save(output)
        click.echo(f"Created PDF: {output}")
    except Exception as e:
        logger.error(f"Failed to create PDF: {e}")
        raise click.ClickException(str(e))


@main.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
def convert(input: str, output: str):
    """Convert a file to PDF format."""
    from pdfmaster.src.converters import convert_file

    try:
        convert_file(input, output)
        click.echo(f"Converted: {input} -> {output}")
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        raise click.ClickException(str(e))

@main.command()
@click.argument("inputs", nargs=-1, type=click.Path(exists=True))
@click.option("--output", "-o", required=True, help="Output PDF path")
def merge(inputs: tuple, output: str):
    """Merge multiple PDFs into a single PDF."""
    from pdfmaster.src.extractors.table_extractor import TableExtractor  # noqa: F401
    import fitz
    if not inputs:
        raise click.ClickException("No input PDFs provided to merge")
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dst = fitz.open()
    for p in inputs:
        src = fitz.open(str(p))
        dst.insert_pdf(src)
        src.close()
    dst.save(str(output_path))
    dst.close()
    click.echo(f"Merged PDFs -> {output_path}")

@main.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("--output-dir", "-o", required=True, help="Output directory for split pages")
@click.option("--pages", default=None, help="Page ranges to split (e.g., 1-3,5,7-9)")
def split(input: str, output_dir: str, pages: str):
    """Split a PDF into individual pages (or specified pages)."""
    import fitz
    from pathlib import Path
    input_path = Path(input)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(input_path))

    # Parse page ranges if provided
    page_numbers = None
    if pages:
        page_numbers = []
        for part in pages.split(','):
            part = part.strip()
            if not part:
                continue
            if '-' in part:
                start, end = part.split('-')
                try:
                    s = int(start)
                    e = int(end)
                except ValueError:
                    continue
                page_numbers.extend(list(range(s, e + 1)))
            else:
                try:
                    page_numbers.append(int(part))
                except ValueError:
                    continue
        page_numbers = sorted(set(page_numbers))

    base = input_path.stem
    for idx in range(doc.page_count):
        if page_numbers is not None and (idx + 1) not in page_numbers:
            continue
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=idx, to_page=idx)
        out_path = out_dir / f"{base}_page_{idx+1}.pdf"
        new_doc.save(str(out_path))
        new_doc.close()
    doc.close()
    click.echo(f"Split complete to {out_dir}")

@main.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("--output-dir", "-o", required=True, help="Output directory for table CSVs")
def extract_table(input: str, output_dir: str):
    """Extract tables from a PDF to CSV files.
    Writes one CSV per table per page as: <output_dir>/table_page{page}_idx{idx}.csv
    """
    from pdfmaster.src.extractors.table_extractor import TableExtractor
    from pathlib import Path
    import pandas as pd

    te = TableExtractor()
    results = te.extract(input)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for t in results:
        df = t.get("dataframe")
        if df is None:
            continue
        out_file = out_dir / f"table_page{t['page']}_idx{t['table_index']}.csv"
        df.to_csv(out_file, index=False)
        click.echo(f"Wrote table to {out_file}")

@main.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("--output-dir", "-o", required=True, help="Output directory for image exports")
@click.option("--page", type=int, default=1, help="Page number to export as image (1-based)")
def export_page_image(input: str, output_dir: str, page: int):
    """Export a single PDF page to an image (PNG)."""
    import fitz
    from pathlib import Path
    input_path = Path(input)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(input_path))
    if page < 1 or page > doc.page_count:
        doc.close()
        raise click.ClickException(f"Invalid page number: {page}")
    p = doc[page - 1]
    pix = p.get_pixmap()
    out_file = out_dir / f"{input_path.stem}_page_{page}.png"
    pix.save(str(out_file))
    doc.close()
    click.echo(f"Exported page {page} to {out_file}")


@main.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("--output", "-o", required=True, help="Output directory for all page images")
def export_all_pages_image(input: str, output: str):
    """Export all PDF pages to separate PNG images."""
    import fitz
    from pathlib import Path
    input_path = Path(input)
    out_dir = Path(output)
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(input_path))
    total = doc.page_count
    stem = input_path.stem
    for i in range(total):
        page = doc[i]
        pix = page.get_pixmap()
        out_file = out_dir / f"{stem}_page_{i+1}.png"
        pix.save(str(out_file))
    doc.close()
    click.echo(f"Exported {total} pages to {out_dir}")

@main.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--text", default="Draft", help="Watermark text to apply")
def watermark(input: str, output: str, text: str):
    """Apply a text watermark across all pages of a PDF."""
    from pdfmaster.src.watermark import add_watermark
    add_watermark(input, output, text)
    click.echo(f"Watermark applied to: {output}")

@main.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option(
    "--encoding", default="utf-8", help="Text encoding (default: utf-8)"
)
def extract_text(input: str, output: str, encoding: str):
    """Extract text content from PDF."""
    from pdfmaster.src.extractors.text_extractor import TextExtractor

    try:
        extractor = TextExtractor()
        text = extractor.extract(input)
        with open(output, "w", encoding=encoding) as f:
            f.write(text)
        click.echo(f"Extracted text to: {output}")
    except Exception as e:
        logger.error(f"Text extraction failed: {e}")
        raise click.ClickException(str(e))

@main.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("--chars", default=500, help="Number of characters to preview from extracted text")
def preview_text(input: str, chars: int):
    """Preview first N characters of extracted text from a PDF."""
    from pdfmaster.src.extractors.text_extractor import TextExtractor
    extractor = TextExtractor()
    text = extractor.extract(input)
    preview = text[: max(0, chars)]
    click.echo(preview)

@main.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("--output", "-o", required=True, help="Output SQL file path")
@click.option("--table-name", help="Name for generated table")
def extract_schema(input: str, output: str, table_name: str):
    """Extract table data and generate SQL schema from PDF."""
    from pdfmaster.src.extractors.schema_generator import SchemaGenerator

    try:
        generator = SchemaGenerator()
        schema = generator.extract(input, table_name=table_name)
        with open(output, "w") as f:
            f.write(schema)
        click.echo(f"Generated SQL schema: {output}")
    except Exception as e:
        logger.error(f"Schema extraction failed: {e}")
        raise click.ClickException(str(e))


@main.command()
@click.option("--input-dir", "-i", required=True, help="Input directory")
@click.option("--output-dir", "-o", required=True, help="Output directory")
@click.option("--pattern", default="*.*", help="File pattern")
def batch_convert(input_dir: str, output_dir: str, pattern: str):
    """Convert multiple files to PDF."""
    from pdfmaster.src.converters.batch import batch_convert_directory

    try:
        results = batch_convert_directory(input_dir, output_dir, pattern)
        click.echo(f"Converted {results['success']} of {results['total']} files")
        if results["failed"] > 0:
            click.echo(f"Failed: {results['failed']}")
    except Exception as e:
        logger.error(f"Batch conversion failed: {e}")
        raise click.ClickException(str(e))


if __name__ == "__main__":
    main()
