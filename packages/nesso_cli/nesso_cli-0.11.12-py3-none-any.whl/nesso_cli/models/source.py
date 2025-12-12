import json
from pathlib import Path
from textwrap import indent
from typing import Optional, Union

import typer
from rich import print
from rich.panel import Panel
from rich.prompt import Prompt
from typing_extensions import Annotated

import nesso_cli.models.context as context
from nesso_cli.models.base_model import rm as base_model_rm
from nesso_cli.models.common import (
    call_shell,
    check_if_relation_exists,
    options,
    wrapper_context_settings,
)
from nesso_cli.models.config import config, yaml

app = typer.Typer()


class SourceTableExistsError(Exception):
    pass


def _get_default_schema_path(source: str) -> Path:
    dbt_project_dir = Path(context.get("PROJECT_DIR"))
    schema_file_name = source + ".yml"
    return dbt_project_dir / "models" / "sources" / source / schema_file_name


def check_if_source_exists(
    source: str, schema_path: Optional[Union[str, Path]] = None
) -> bool:
    if schema_path is None:
        schema_path = _get_default_schema_path(source)

    # Enforce `pathlib.Path` type.
    schema_path = Path(schema_path)
    return schema_path.exists()


def check_if_source_table_exists(
    source: str, table_name: str, schema_path: Optional[Union[str, Path]] = None
) -> bool:
    if schema_path is None:
        schema_path = _get_default_schema_path(source)

    if check_if_source_exists(source, schema_path=schema_path):
        representations = [
            f"- name: {table_name}\n",
            f'- name: "{table_name}"\n',
            f"- name: '{table_name}'\n",
        ]

        with open(schema_path, "r") as f:
            for line in f:
                for representation in representations:
                    if representation in line:
                        return True
    return False


def _create_table_docs(
    base_dir: Path,
    schema: str,
    table: str,
    no_profile: bool,
    target: Optional[str] = None,
    non_interactive: Optional[bool] = False,
) -> None:
    """Create documentation for a database table.

    Args:
        base_dir (Path): The base directory for storing the documentation.
        schema (str): The schema of the database table.
        table (str): The name of the database table.
        no_profile (bool): If True, creates a description template for the table.
            If False, profiles the source table.
        target (Optional[str], optional): The name of the dbt target to use.
            Defaults to None.
        non_interactive (Optional[str], optional): Whether to execute the function
            without interactive prompts. Defaults to False.
    """

    docs_path = base_dir.joinpath("docs", f"{table}.md")
    docs_path_trimmed = docs_path.relative_to(
        docs_path.parent.parent.parent.parent.parent
    )
    docs_path_fmt = f"[bright_black]{docs_path_trimmed}[/bright_black]"
    fqn_fmt = f"[white]{schema}.{table}[/white]"

    docs_path.parent.mkdir(exist_ok=True, parents=True)

    if no_profile:
        print(f"Creating description template for model [blue]{fqn_fmt}[/blue]...")
        args = {"schema": schema, "relation_name": table}
        command = f"dbt -q run-operation create_description_markdown --args '{args}'"
        if target:
            command += f" --target {target}"
        content = call_shell(
            command,
            print_logs=False,
        )
        success_msg = f"Description template successfully written to {docs_path_fmt}."
    else:
        print(f"Profiling source table {fqn_fmt}...")
        args = {"schema": schema, "relation_name": table}
        command = f"dbt -q run-operation print_profile_docs --args '{args}'"
        if target:
            command += f" --target {target}"

        content = call_shell(command)
        success_msg = f"Profile successfully written to {docs_path_fmt}."

    with open(docs_path, "w") as file:
        file.write(content)

    print(success_msg)

    if not non_interactive:
        print(
            Panel(
                f"""Before continuing, please open [link={docs_path}]{table}.md[/link]
    and add your description in the [blue]📝 Details[/blue] section.""",
                title="ATTENTION",
                width=100,
            )
        )
        Prompt.ask("Press [green]ENTER[/green] to continue")


@app.command()
def create(
    ctx: typer.Context,
    source: Annotated[
        str, typer.Argument(help="The name of the source schema.", show_default=False)
    ],
    schema_path: Annotated[
        Optional[str],
        typer.Option(
            "--schema-path",
            help="""The path to the source YAML.
        Defaults to `{PROJECT_DIR}/models/sources/{source}.yml`.""",
        ),
    ] = None,
    case_sensitive_cols: Annotated[
        Optional[bool],
        typer.Option(
            "--case-sensitive-cols",
            "-c",
            help="Whether the column names of the source are case-sensitive.",
            is_flag=True,
        ),
    ] = True,
    no_profile: Annotated[
        Optional[bool],
        typer.Option(
            "--no-profile",
            "-np",
            help="Whether to skip table profiling.",
            is_flag=True,
        ),
    ] = True,
    env: options.environment = config.default_env,
    project: options.project = context.get("PROJECT_NAME"),
    force: options.force("Overwrite the existing source.") = False,
):
    """Add a new source schema with all existing tables in it."""

    dbt_project_dir = Path(context.get("PROJECT_DIR"))

    if not project:
        project = dbt_project_dir.name

    base_dir = dbt_project_dir / "models" / "sources" / source

    if not schema_path:
        schema_path: Path = base_dir / f"{source}.yml"

    if not base_dir.exists():
        base_dir.mkdir(parents=True, exist_ok=True)

    source_exists = check_if_source_exists(source, schema_path=schema_path)
    if source_exists:
        if force:
            operation = "overwriting"
        else:
            print(f"Source [blue]{source}[/blue] [b]already exists[/b]. Skipping...")
            return False
    else:
        operation = "creating"

    print(f"[white]{operation.title()} source[/white] [blue]{source}[/blue]...")

    args = {"schema_name": source, "print_result": True}
    get_existing_tables_cmd = (
        f"dbt -q run-operation get_tables_in_schema --args '{args}' --target {env}"
    )

    existing_tables_str = call_shell(get_existing_tables_cmd, print_logs=False).strip()
    if not existing_tables_str:
        raise ValueError(f"Schema '{source}' is empty.")
    existing_tables = existing_tables_str.split(",")

    for table in existing_tables:
        _create_table_docs(
            base_dir=base_dir,
            schema=source,
            table=table,
            no_profile=no_profile,  # type: ignore
            target=env,
        )

    # Generate the YAML file.
    args = {"schema_name": source, "case_sensitive_cols": case_sensitive_cols}
    generate_yaml_text_command = (
        f"""dbt -q run-operation generate_source --args '{args}' --target {env}"""
    )

    source_str = call_shell(generate_yaml_text_command, print_logs=False)

    with open(schema_path, "w") as f:
        f.write(source_str)

    # Print success message.
    operation_past_tenses = {"overwriting": "overwritten", "creating": "created"}
    operation_past_tense = operation_past_tenses[operation]
    print(f"Source [blue]{source}[/blue] has been {operation_past_tense} successfully.")

    return True


@app.command()
def add(
    ctx: typer.Context,
    table_name: Annotated[
        str, typer.Argument(help="The name of the table to add.", show_default=False)
    ],
    case_sensitive_cols: Annotated[
        Optional[bool],
        typer.Option(
            "--case-sensitive-cols",
            "-c",
            help="Whether the column names are case-sensitive.",
        ),
    ] = True,
    no_profile: Annotated[
        Optional[bool],
        typer.Option(
            "--no-profile",
            "-np",
            help="Whether to document data profiling information.",
            is_flag=True,
        ),
    ] = True,
    project: options.project = context.get("PROJECT_NAME"),
    env: options.environment = config.default_env,
    non_interactive: Annotated[
        Optional[bool],
        typer.Option(
            "--non-interactive",
            "-ni",
            help="Whether to execute the command without interactive prompts.",
            is_flag=True,
        ),
    ] = False,
) -> bool:
    """Add a new table to a source schema and materializes it as a base model."""

    dbt_project_dir = Path(context.get("PROJECT_DIR"))
    project = project or dbt_project_dir.name
    source = config.bronze_schema

    base_dir = dbt_project_dir.joinpath("models", "sources", source)

    if not base_dir.exists():
        base_dir.mkdir(parents=True, exist_ok=True)

    schema_path = _get_default_schema_path(source)
    fqn = f"{source}.{table_name}"
    fqn_fmt = f"[white]{source}.{table_name}[/white]"

    yaml_exists = check_if_source_table_exists(source=source, table_name=table_name)
    if yaml_exists:
        print(f"Source table '{fqn}' already exists. Skipping...")
        return False

    table_exists = check_if_relation_exists(name=table_name, schema=source, target=env)
    if not table_exists:
        raise ValueError(f"Table '{fqn}' does not exist.")

    # Generate docs.
    _create_table_docs(
        base_dir=base_dir,
        schema=source,
        table=table_name,
        no_profile=no_profile,
        target=env,
        non_interactive=non_interactive,
    )

    # Generate source YAML and append it to the sources schema.
    args = json.dumps(
        {
            "schema_name": source,
            "table_names": [table_name],
            "case_sensitive_cols": case_sensitive_cols,
        }
    )
    generate_source_text_command = (
        f"""dbt -q run-operation generate_source --args '{args}' --target {env}"""
    )

    source_str = call_shell(generate_source_text_command, print_logs=False)

    # Special case when adding the first table.
    has_tables = False
    with open(schema_path, "r") as file:
        for line_number, line in enumerate(file):
            if "tables" in line:
                has_tables = True
                break
            elif line_number > 100:
                # The "tables" key is at the top of the props file, so need to scan the
                # entire file (it could have millions of rows).
                break
    if not has_tables:
        source_str = "\n" + indent("tables:", " " * 4) + source_str

    with open(schema_path, "a") as file:
        file.write(source_str)

    print(f"Source table {fqn_fmt} has been added successfully.")

    schema_path_trimmed = schema_path.relative_to(
        schema_path.parent.parent.parent.parent
    )

    if not non_interactive:
        print(
            Panel(
                f"""Before continuing, please provide the source table's metadata in [link={schema_path}]{schema_path_trimmed}[/link]
    (owners, tests, etc.).""",  # noqa
                title="ATTENTION",
                width=120,
            )
        )

        Prompt.ask("Press [green]ENTER[/green] to continue")

    return True


@app.command(context_settings=wrapper_context_settings)
def freshness(
    ctx: typer.Context,
    select: Annotated[
        Optional[str], typer.Option("--select", "-s", help="The source(s) to select.")
    ] = None,
    env: options.environment = config.default_env,
):
    """Validate the freshness of source table(s)."""
    args = []
    if select:
        if "." not in select:
            # Table name has to be fully qualified.
            select = f"{config.bronze_schema}.{select}"
        if "source:" not in select:
            select = f"source:{select}"
        args.extend(["-s", select])
    if ctx.args:
        args.extend(ctx.args)

    result = call_shell(f"dbt source freshness -t {env}", args=args, print_logs=True)
    return result


@app.command()
def rm(
    table_name: Annotated[
        str, typer.Argument(help="The name of the table to add.", show_default=False)
    ],
    remove_base_model: Annotated[
        Optional[bool],
        typer.Option(
            "--remove-base-model",
            "-b",
            help="Whether to remove the corresponding base model.",
            is_flag=True,
        ),
    ] = False,
    env: options.environment = config.default_env,
) -> bool:
    """Remove a source table from the schema YAML."""

    dbt_project_dir = Path(context.get("PROJECT_DIR"))
    source = config.bronze_schema
    base_dir = dbt_project_dir.joinpath("models", "sources", source)
    schema_path = _get_default_schema_path(source)

    # Remove the description Markdown.
    description_markdown = base_dir / f"{table_name}.md"
    description_markdown.unlink(missing_ok=True)

    # Remove the definition from source schema YAML.
    with open(schema_path, "r") as file:
        cfg = yaml.load(file)

    try:
        source_cfg = [s for s in cfg["sources"] if s["name"] == source][0]
    except IndexError:
        raise ValueError(f"Source table {table_name} not found in {schema_path}.")

    source_cfg["tables"] = [t for t in source_cfg["tables"] if t["name"] != table_name]

    with open(schema_path, "w") as file:
        yaml.dump(cfg, file)

    # Remove the base model.
    if remove_base_model:
        base_model_name = config.silver_schema_prefix + "_" + table_name
        base_model_rm(name=base_model_name, relation=True, env=env)

    return True


if __name__ == "__main__":
    app()
