from click.testing import CliRunner

def test_cli_smoke_import_and_help():
    # Import the CLI entrypoint and invoke help to ensure import paths work
    from pdfmaster.src.cli import main as cli_main

    runner = CliRunner()
    result = runner.invoke(cli_main, ["--help"])
    assert result.exit_code == 0
    assert "PDF Master" in (result.output or "") or "Usage" in (result.output or "")
