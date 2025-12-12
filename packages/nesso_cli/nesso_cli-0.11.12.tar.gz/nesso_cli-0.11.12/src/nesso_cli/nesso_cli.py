from importlib.metadata import version
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

import nesso_cli.jobs as jobs
import nesso_cli.models as models

app = typer.Typer(rich_markup_mode="rich")
app.add_typer(models.main.app, name="models", short_help="Manage data models.")
app.add_typer(jobs.main.app, name="jobs", short_help="Manage ELT jobs.")


def cli():
    """For python script installation purposes (flit)"""
    app()


def version_callback(value: bool):
    if value:
        cli_name = Path(__file__).stem
        print(f"{cli_name} {version(cli_name)}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option("--version", "-v", callback=version_callback, is_eager=True),
    ] = None,
):
    return


if __name__ == "__main__":
    app()
