from typing import Optional

import typer
from rich import print
from typing_extensions import Annotated

from nesso_cli.models.base_model import _get_default_base_dir_path
from nesso_cli.models.common import options
from nesso_cli.models.config import config
from nesso_cli.models.model import _get_model_dir
from nesso_cli.models.models import DBTProperties
from nesso_cli.models.source import _get_default_schema_path

app = typer.Typer()


@app.command()
def source(
    table_name: Annotated[
        str, typer.Argument(help="The name of the table to update.", show_default=False)
    ],
    schema: Annotated[
        Optional[str],
        typer.Option(
            "--schema",
            "-s",
            help="The schema where the table is located.",
        ),
    ] = config.bronze_schema,
    env: options.environment = config.default_env,
):
    """Updates the source YAML file."""
    source_path = _get_default_schema_path(schema)

    source_properties = DBTProperties(file_path=source_path)

    source_diff, yaml_columns, db_columns = source_properties.coherence_scan(
        schema_name=schema,
        table_name=table_name,
        env=env,
    )
    if not source_diff:
        print(f"Source [blue]{schema}[/blue] is up to date.")
        return

    source_properties.synchronize_columns(
        diff=source_diff,
        yaml_columns=yaml_columns,
        db_columns=db_columns,
        table_name=table_name,
    )

    print(f"Source [blue]{schema}[/blue] has been updated successfully.")


@app.command(name="base_model")
def base_model(
    base_model: Annotated[
        str,
        typer.Argument(
            help="The name of the base_model to update.", show_default=False
        ),
    ],
    env: options.environment = config.default_env,
):
    """Updates the base model YAML file.

    If silver schema prefix is not specified at the beginning of the model name, it
    will be added automatically."""

    base_model_prefix = config.silver_schema_prefix
    if base_model_prefix and not base_model_prefix.endswith("_"):
        base_model_prefix = f"{base_model_prefix}_"

    if not base_model.startswith(base_model_prefix):
        base_model = f"{base_model_prefix}{base_model}"

    base_model_dir = _get_default_base_dir_path(base_model)
    yaml_file_path = base_model_dir / f"{base_model}.yml"

    base_model_properties = DBTProperties(file_path=yaml_file_path)

    base_model_diff, yaml_columns, db_columns = base_model_properties.coherence_scan(
        table_name=base_model,
        env=env,
    )

    if not base_model_diff:
        print(f"Base model [blue]{base_model}[/blue] is up to date.")
        return

    base_model_properties.synchronize_columns(
        diff=base_model_diff,
        yaml_columns=yaml_columns,
        db_columns=db_columns,
        table_name=base_model,
    )

    print(
        f"Base model [blue]{base_model}[/blue] has been updated [green]successfully[/]."
    )


@app.command()
def model(
    model: Annotated[
        str,
        typer.Argument(help="The name of the model to update.", show_default=False),
    ],
    env: options.environment = config.default_env,
):
    """Updates the model YAML file."""

    model_dir = _get_model_dir(model)
    yaml_file_path = model_dir / f"{model}.yml"

    model_properties = DBTProperties(file_path=yaml_file_path)

    model_diff, yaml_columns, db_columns = model_properties.coherence_scan(
        table_name=model,
        env=env,
    )
    if not model_diff:
        print(f"Model [blue]{model}[/blue] is up to date.")
        return

    model_properties.synchronize_columns(
        diff=model_diff,
        yaml_columns=yaml_columns,
        db_columns=db_columns,
        table_name=model,
    )

    print(f"Model [blue]{model}[/blue] has been updated [green]successfully[/].")


if __name__ == "__main__":
    app()
