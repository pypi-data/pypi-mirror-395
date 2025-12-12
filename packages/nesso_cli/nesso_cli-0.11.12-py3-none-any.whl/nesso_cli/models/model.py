from pathlib import Path
from typing import Optional

import typer
from rich import print
from rich.panel import Panel
from typing_extensions import Annotated

from nesso_cli.models import context
from nesso_cli.models.common import (
    call_shell,
    convert_list_of_options_to_dict,
    options,
)
from nesso_cli.models.config import config
from nesso_cli.models.resources import NessoDBTModel

app = typer.Typer()


def _get_model_dir(model_name: str) -> Path:
    """Retrieve the directory where a model (SQL file) is located.

    Args:
        model_name (str): The name of the model to retrieve.

    Raises:
        FileNotFoundError: If the specified model is not found.

    Returns:
        Path: The path to the model directory.
    """
    dbt_project_dir = Path(context.get("PROJECT_DIR"))
    models_path = dbt_project_dir.joinpath("models", config.gold_layer_name)
    for path in models_path.rglob(model_name):
        if path.is_dir():
            return path
    raise FileNotFoundError(f"Model '{model_name}' not found in directory tree.")


@app.command()
def bootstrap(
    model: Annotated[
        str, typer.Argument(help="The name of the model.", show_default=False)
    ],
    subdir: Annotated[
        Optional[str],
        typer.Option(
            "-s",
            "--subdir",
            help="Subdirectory inside the gold layer where the model should be located.",  # noqa
        ),
    ] = None,
):
    """Generate an empty models/<MODEL_NAME>/<MODEL_NAME>.sql file."""
    nesso_project_dir = Path(context.get("PROJECT_DIR"))
    project_dir = nesso_project_dir.joinpath(
        "models", config.gold_layer_name, subdir or ""
    )
    model_dir = project_dir.joinpath(model)

    if not model_dir.exists():
        model_dir.mkdir(parents=True, exist_ok=True)

    sql_path = model_dir.joinpath(f"{model}.sql")

    sql_path.touch(exist_ok=True)
    sql_path_short = Path(
        "models", config.gold_layer_name, subdir or "", model, f"{model}.sql"
    )
    print(
        f"File [bright_black]{sql_path_short}[/bright_black] has been created [green]successfully[/green]."  # noqa
    )

    print("Model bootstrapping is [green]complete[/green].")

    sql_path_clickable = nesso_project_dir.name / sql_path_short
    print(
        Panel(
            f"""Once you populate the model file ([link={sql_path}]{sql_path_clickable}[/link]),
you can materialize it with [bright_black]nesso models run -s {model}[/bright_black], and then generate a YAML
template for it with [bright_black]nesso models model bootstrap-yaml {model}[/bright_black].""",  # noqa
            width=100,
        )
    )


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def bootstrap_yaml(
    ctx: typer.Context,
    model: Annotated[
        str, typer.Argument(help="The name of the model.", show_default=False)
    ],
    env: options.environment = config.default_env,
):
    """Bootstrap the YAML file for a particular model."""

    model_dir = _get_model_dir(model_name=model)
    meta = convert_list_of_options_to_dict(ctx.args)

    dbt_model = NessoDBTModel(
        name=model,
        env=env,
        **meta,
    )

    print(f"Creating YAML for model [blue]{dbt_model.name}[/blue]...")
    yaml_path = model_dir.joinpath(f"{dbt_model.name}.yml")

    # Materialize the model.
    call_shell(f"dbt run --select {dbt_model.name}", print_logs=False)

    dbt_model.to_yaml(yaml_path)

    print(
        f"YAML template for model [blue]{dbt_model.name}[/] has been created [green]successfully[/]."  # noqa
    )


if __name__ == "__main__":
    app()
