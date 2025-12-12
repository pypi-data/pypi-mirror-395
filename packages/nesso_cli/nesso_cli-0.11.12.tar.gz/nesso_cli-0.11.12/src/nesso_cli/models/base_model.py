import shutil
from pathlib import Path
from typing import Optional, Union

import typer
from rich import print
from rich.panel import Panel
from typing_extensions import Annotated

import nesso_cli.models.context as context
from nesso_cli.models.common import (
    call_shell,
    convert_list_of_options_to_dict,
    drop,
    get_local_schema,
    options,
)
from nesso_cli.models.config import config
from nesso_cli.models.resources import NessoDBTModel

app = typer.Typer()


def _get_default_base_dir_path(base_model_name: str) -> Path:
    dbt_project_dir = Path(context.get("PROJECT_DIR"))
    return dbt_project_dir / "models" / config.silver_schema / base_model_name


def check_if_base_model_exists(
    base_model_name: str,
    base_model_dir: Optional[Union[str, Path]] = None,
) -> bool:
    """Check whether a base model (ie. both SQL and YAML files) exists.

    Args:
        base_model_name (str): The name of the base model.
        base_model_dir (Optional[Union[str, Path]], optional): The path to the
            directory holding the base model. Defaults to None (default directory).

    Returns:
        bool: Whether the base model exists.
    """
    if base_model_dir is None:
        base_model_dir = _get_default_base_dir_path(base_model_name)

    # Enforce `pathlib.Path` type.
    base_model_dir = Path(base_model_dir)

    sql_path = base_model_dir / f"{base_model_name}.sql"
    yml_path = base_model_dir / f"{base_model_name}.yml"

    both_files_exist = sql_path.exists() and yml_path.exists()
    none_files_exist = not sql_path.exists() and not yml_path.exists()

    silver_schema = Path(base_model_dir).parent.stem
    fqn = f"[blue]{silver_schema}.{base_model_name}[/blue]"
    msg = f"""SQL or YML file for the base model {fqn} is missing.
Please remove the remaining file."""
    assert both_files_exist or none_files_exist, msg

    return sql_path.exists()


@app.command()
def rm(
    name: Annotated[
        str,
        typer.Argument(
            help="The name of the base model to remove.", show_default=False
        ),
    ],
    silver_schema: Annotated[
        str,
        typer.Option(
            "--silver-schema",
            "-s",
            help="The silver schema where the base model is located.",
        ),
    ] = config.silver_schema,
    relation: Annotated[
        Optional[bool],
        typer.Option(
            "--relation",
            "-r",
            help="Whether to remove the model's relation as well.",
            is_flag=True,
        ),
    ] = False,
    env: options.environment = config.default_env,
):
    """Remove a base model (YAML and optionally the relation)."""

    dbt_project_dir = Path(context.get("PROJECT_DIR"))
    base_model_dir = dbt_project_dir / "models" / silver_schema / name

    shutil.rmtree(base_model_dir, ignore_errors=True)

    if relation:
        if env == "prod":
            schema = silver_schema
        else:
            schema = get_local_schema(target=env)
        drop(name=name, schema=schema)


@app.command()
def bootstrap(
    base_model_name: Annotated[
        str, typer.Argument(help="The name of the base model.", show_default=False)
    ],
    silver_schema: Annotated[
        str,
        typer.Option(
            "--silver-schema",
            "-s",
            help="The silver schema to use for the base model.",
        ),
    ] = config.silver_schema,
):
    """Generate an empty [bright_black]{silver_schema}/{base_model_name}/{base_model_name}.sql[/] file.

    If silver schema prefix is not specified at the beginning of the model name, it
    will be added automatically.
    """  # noqa

    base_model_prefix = config.silver_schema_prefix
    if base_model_prefix and not base_model_prefix.endswith("_"):
        base_model_prefix = f"{base_model_prefix}_"

    if not base_model_name.startswith(base_model_prefix):
        base_model_name = f"{base_model_prefix}{base_model_name}"

    dbt_project_dir = Path(context.get("PROJECT_DIR"))

    base_dir = dbt_project_dir / "models" / silver_schema / base_model_name
    sql_path = base_dir / f"{base_model_name}.sql"

    if not base_dir.exists():
        base_dir.mkdir(parents=True, exist_ok=True)

    fqn = f"{silver_schema}.{base_model_name}"

    base_model_exists = check_if_base_model_exists(
        base_model_name, base_model_dir=base_dir
    )
    if base_model_exists:
        print(f"Base model {fqn} already exists. Skipping...")
        return

    sql_path_short = Path(
        "models",
        silver_schema,
        base_model_name,
        f"{base_model_name}.sql",
    )

    sql_path.touch(exist_ok=True)

    print(
        f"File [bright_black]{sql_path_short}[/bright_black] has been created [green]successfully[/green]."  # noqa
    )

    print("Base model bootstrapping is [green]complete[/green].")

    sql_path_clickable = dbt_project_dir.name / sql_path_short
    print(
        Panel(
            f"""Once you populate the base model file ([link={sql_path}]{sql_path_clickable}[/link]),
you can materialize it with [bright_black]nesso models run -s {base_model_name}[/bright_black], and then generate a YAML
template for it with [bright_black]nesso models base_model bootstrap-yaml {base_model_name}[/bright_black].""",  # noqa
            width=100,
        )
    )


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def bootstrap_yaml(
    ctx: typer.Context,
    base_model_name: Annotated[
        str, typer.Argument(help="The name of the base model.", show_default=False)
    ],
    silver_schema: Annotated[
        str,
        typer.Option(
            "--silver-schema",
            "-s",
            help="The silver schema to use for the base model.",
        ),
    ] = config.silver_schema,
    env: options.environment = config.default_env,
):
    """Bootstrap the YAML file for a base model.

    If `silver_schema_prefix` is not specified at the beginning of the base_model_name,
    it will be added automatically."""

    meta = convert_list_of_options_to_dict(ctx.args)
    dbt_model = NessoDBTModel(name=base_model_name, env=env, base=True, **meta)
    dbt_project_dir = Path(context.get("PROJECT_DIR"))

    base_dir = dbt_project_dir / "models" / silver_schema / dbt_model.name
    yaml_path = base_dir / f"{dbt_model.name}.yml"

    yaml_path_short = Path(
        "models",
        silver_schema,
        dbt_model.name,
        dbt_model.name + ".yml",
    )

    # Materialize the model.
    call_shell(f"dbt run --select {dbt_model.name}", print_logs=False)

    dbt_model.to_yaml(yaml_path)

    print(
        f"YAML template for base model {yaml_path_short} has been crated successfully."  # noqa
    )


if __name__ == "__main__":
    app()
