from click.testing import CliRunner

def test_cli_smoke_import_and_help():
    # Import the CLI entrypoint and invoke help to ensure import paths work
    from pdfmaster.src.cli import main as cli_main

    runner = CliRunner()
    result = runner.invoke(cli_main, ["--help"])
    assert result.exit_code == 0
    assert "PDF Master" in (result.output or "") or "Usage" in (result.output or "")

def test_cli_commands_exist():
    # Ensure the expected subcommands exist on the CLI group
    from pdfmaster.src.cli import main as cli_main
    commands = getattr(cli_main, 'commands', {})
    for name in ["create", "convert", "extract-text", "extract-schema", "batch-convert"]:
        assert name in commands or name.replace('-', '_') in commands
