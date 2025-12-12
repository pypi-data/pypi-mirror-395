#!/usr/bin/env python
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer
from rich import print
from typing_extensions import Annotated

import nesso_cli.models.base_model as base_model
import nesso_cli.models.init as init
import nesso_cli.models.metadata as metadata
import nesso_cli.models.model as model
import nesso_cli.models.seed as seed
import nesso_cli.models.source as source
import nesso_cli.models.update as update
from nesso_cli.models import context
from nesso_cli.models.common import call_shell, options, wrapper_context_settings
from nesso_cli.models.config import config

app = typer.Typer()

app.add_typer(source.app, name="source", short_help="Manage sources.")
app.add_typer(base_model.app, name="base_model", short_help="Manage base models.")
app.add_typer(model.app, name="model", short_help="Manage models.")
app.add_typer(seed.app, name="seed", short_help="Manage seeds.")
app.add_typer(metadata.app, name="metadata", short_help="Manage model metadata.")
app.add_typer(
    update.app,
    name="update",
    short_help="Update YAMLs with latest information from the database.",
)
app.add_typer(
    init.app, name="init", short_help="Initialize a new nesso project or user."
)

PRIVATE_USER_FIELDS = ("password", "token")
USER_CREDENTIAL_FIELDS = ("user", *PRIVATE_USER_FIELDS)
USER_FIELDS = (*USER_CREDENTIAL_FIELDS, "schema")
TEMPLATES_DIR = Path(__file__).parent.resolve() / "templates"


######################################################################################
# DBT wrappers.                                                                      #
# Note we include `--select` option explicitly in order to display its help message. #
######################################################################################


@app.command(context_settings=wrapper_context_settings)
def debug(
    ctx: typer.Context,
    env: options.environment = config.default_env,
):
    """Validate project configuration and database connectivity."""
    call_shell(f"dbt debug -t {env}", args=ctx.args, print_logs=True)


@app.command(context_settings=wrapper_context_settings)
def test(
    ctx: typer.Context,
    select: Annotated[
        Optional[str], typer.Option("--select", "-s", help="The model(s) to select.")
    ] = None,
    env: options.environment = config.default_env,
):
    """Run tests."""
    args = []
    if select:
        args.extend(["-s", select])
    if ctx.args:
        args.extend(ctx.args)
    try:
        call_shell(f"dbt test -t {env}", args=args, print_logs=True)
    except subprocess.CalledProcessError:
        print("`dbt test` command failed")
        sys.exit(1)


@app.command(context_settings=wrapper_context_settings)
def run(
    ctx: typer.Context,
    select: Annotated[
        Optional[str], typer.Option("--select", "-s", help="The model(s) to select.")
    ] = None,
    env: options.environment = config.default_env,
):
    """Run model(s)."""
    args = []
    if select:
        args.extend(["-s", select])
    if ctx.args:
        args.extend(ctx.args)
    call_shell(f"dbt run -t {env}", args=args, print_logs=True)


@app.command()
def setup():
    """Setup the project. Also useful for creating a fresh environment.

    Clean up the folders specified in `dbt_project.yml` and pull project dependencies
    specified in `packages.yml`.
    """
    call_shell("dbt clean && dbt deps", print_logs=True)
    # Fix dbt utils bug.
    # See https://github.com/dbt-labs/dbt-utils/issues/627.
    dbt_project_dir = Path(context.get("PROJECT_DIR"))
    shutil.rmtree(
        dbt_project_dir.joinpath(
            "dbt_packages",
            "dbt_utils",
            "tests",
        ),
        ignore_errors=True,
    )


if __name__ == "__main__":
    app()
