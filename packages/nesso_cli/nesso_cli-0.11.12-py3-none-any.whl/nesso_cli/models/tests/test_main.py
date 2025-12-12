from pathlib import Path

from typer.testing import CliRunner

from nesso_cli.models.main import app

runner = CliRunner()

PROJECT_DIR = Path(__file__).parent.joinpath("dbt_projects", "postgres")


def test_test(setup_model, MODEL):
    result = runner.invoke(
        app,
        ["test", "-s", MODEL, "-e", "prod"],
    )
    assert result.exit_code == 0


def test_debug():
    result = runner.invoke(
        app,
        ["debug"],
    )
    assert result.exit_code == 0


def test_run(setup_model, MODEL):
    result = runner.invoke(
        app,
        ["run", "-s", MODEL, "-t", "prod"],
    )
    assert result.exit_code == 0


def test_setup():
    dbt_erroring_dir_path = PROJECT_DIR.joinpath(
        "dbt_packages",
        "dbt_utils",
        "tests",
    )

    result = runner.invoke(
        app,
        ["setup"],
    )

    assert result.exit_code == 0
    assert not dbt_erroring_dir_path.exists()
