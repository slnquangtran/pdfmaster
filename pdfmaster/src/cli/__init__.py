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
