from typer.testing import CliRunner

from nesso_cli.models.main import app

runner = CliRunner()


def test_metadata():
    result = runner.invoke(
        app,
        ["metadata", "generate"],
    )
    assert result.exit_code == 0
