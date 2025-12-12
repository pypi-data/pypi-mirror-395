from importlib import metadata
import json
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Annotated, Any

import click
from jinja2 import Environment, FileSystemLoader
from rich import print
from rich.prompt import IntPrompt, Prompt
import typer

from nesso_cli.models.common import call_shell, wrapper_context_settings
from nesso_cli.models.config import config, yaml
from nesso_cli.models.models import NessoDBTConfig, dbt_config_map


app = typer.Typer()


TEMPLATES_DIR = Path(__file__).parent.resolve() / "templates"
JINJA_ENVIRONMENT = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
PRIVATE_USER_FIELDS = ("password", "token")
USER_CREDENTIAL_FIELDS = ("user", *PRIVATE_USER_FIELDS)
USER_FIELDS = (*USER_CREDENTIAL_FIELDS, "schema")

TEMPLATE_FILES_TO_COPY = [".gitignore", ".vscode"]
TEMPLATE_FILES_TO_RENDER = [
    "config.yml",
    "dbt_project.yml",
    "README.md",
    "requirements.txt",
    "packages.yml",
    "prepare.sh",
    "{{ bronze_schema }}.yml",
    "CONTRIBUTING.md",
]


def render_string(template_string: str, **kwargs) -> str:
    """Render a string from a Jinja template.

    Args:
        template_string (str): The template string.
        kwargs: dict[str, Any]: Values to be passed to the template file (useful to
            execute the function non-interactively).

    Returns:
        str: The rendered string.

    """
    template = JINJA_ENVIRONMENT.from_string(template_string)
    return template.render(**kwargs)


def render_jinja_template_file(
    template_path: str | Path,
    output_dir_path: str | Path | None = None,
    stream_output: bool = False,
    **kwargs,
) -> str | None:
    """Create a project file from a Jinja template.

    Args:
        template_path (str): The path to the template file, relative to the `templates/`
            directory.
        output_dir_path (str, optional): The path to the output directory.
            The file name is taken from `template_path` or a rendered Jinja (eg. if
            template file name is `{{ project_name }}.yml`, this function will expect a
            keyword argument named `project_name` to be provided. Then, the output file
            name will be resolved using this input. For example, if
            `project_name=my_project` is passed, the resulting file name would be
            `my_project.yml`).
            Ignored if `stream_output` is True.
        stream_output (bool, optional): Whether to return the output as a string.

    """
    template = JINJA_ENVIRONMENT.get_template(str(template_path))
    content = template.render(**kwargs)

    if stream_output:
        return content

    template_file_name = Path(template_path).name

    # Handle a templated file name, eg. '{{ project_name }}.yml'.
    if "{{" in template_file_name and "}}" in template_file_name:
        target_file_name = render_string(template_string=template_file_name, **kwargs)
    else:
        target_file_name = template_file_name

    target_file_path = Path(output_dir_path or "") / target_file_name

    # Ensure that the output directory exists.
    target_file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(target_file_path, "w") as f:
        f.write(content)

    return None


def create_profiles_yml_template(
    db_type: str, project_name: str, profiles_path: str | Path | None = None, **kwargs
) -> None:
    """Create a `profiles.yml.example` file with example config.

    Args:
        db_type (str): The type of the database for which this profile is created.
            The list of supported databases is currently in `_get_db_type_from_user()`.
        project_name (str): The name of the project for which this profile is
            created.
        profiles_path (str | Path, optional): The path to the generated file. Defaults
            to "profiles.yml.example".
        kwargs: dict[str, Any]: Values to be passed to the template file (useful to
            execute the function non-interactively).

    """
    if profiles_path is None:
        profiles_path = f"{project_name}/profiles.yml.example"

    path = Path(profiles_path)

    if path.exists():
        path_trimmed = path.relative_to(path.parent.parent)
        print(f"File '{path_trimmed}' already exists. Overwriting...")

    model = NessoDBTConfig(db_type=db_type, project_name=project_name).dict(  # type: ignore[attr-defined]
        by_alias=True
    )
    profile_name = list(model.keys())[0]
    profile = model[profile_name]
    target = profile["target"]
    config = profile["outputs"][target]

    advanced_config_fields = ["threads", "retries", "login_timeout", "query_timeout"]

    for field in config:
        # Only prompt for values not provided in kwargs.
        if field not in kwargs:
            # Skip irrelevant fields.
            if field not in ("type", *USER_FIELDS, *advanced_config_fields):
                default = config[field]
                if isinstance(default, int):
                    value = IntPrompt.ask(
                        f"Please provide the value for '{field}'", default=default
                    )
                else:
                    value = Prompt.ask(
                        f"Please provide the value for '{field}'", default=default
                    )  # type: ignore
            else:
                continue
        else:
            value = kwargs[field]

        config[field] = value

    print("Generating a template `profiles.yml` file...")

    with open(path, "w") as f:
        yaml.dump(model, f)

    print("`profiles.yml.example` file was created [green]successfully[/]...")


def create_directory_structure(
    project_dir: Path,
    bronze_schema: str,
    silver_schema: str,
    gold_layer_name: str,
) -> tuple[Path, Path, Path, Path]:
    """Create initial project directory structure.

    Args:
        project_dir (Path): The root directory of the project.
        bronze_schema (str): The name of the bronze schema.
        silver_schema (str): The name of the silver schema.
        gold_layer_name (str): The name of the gold layer.

    Returns:
        tuple[Path, Path, Path]: Paths to the created directories (bronze schema,
            silver schema, gold layer, and nesso config dir).

    """
    bronze_schema_dir = project_dir / "models" / "sources" / bronze_schema
    bronze_schema_dir.mkdir(parents=True, exist_ok=True)
    silver_schema_dir = project_dir / "models" / silver_schema
    silver_schema_dir.mkdir(parents=True, exist_ok=True)
    gold_layer_dir = project_dir / "models" / gold_layer_name
    gold_layer_dir.mkdir(parents=True, exist_ok=True)

    nesso_config_dir = project_dir / ".nesso"
    nesso_config_dir.mkdir(parents=True, exist_ok=True)

    return bronze_schema_dir, silver_schema_dir, gold_layer_dir, nesso_config_dir


def render_project_files(
    project_name: str,
    data_architecture: str,
    db_type: str,
    bronze_schema: str,
    silver_schema: str,
    silver_schema_prefix: str,
    gold_layer_name: str,
    macros_path: str,
    default_env: str,
    nesso_cli_version: str,
    luma: bool,
    snakecase_columns: bool,
) -> None:
    """Render project files from Jinja templates.

    Note we could just use **kwargs here, but we kept the explicit list of params to
    make it clear which project variables are used.

    Args:
        project_name (str): The name of the project.
        data_architecture (str): The data architecture to use.
        db_type (str): The database type that the project will connect to.
        bronze_schema (str): The schema where raw data is ingested ("input schema").
        silver_schema (str): The intermediate schema between raw data and user-facing
            models.
        silver_schema_prefix (str): The prefix to use for models in the silver schema.
        gold_layer_name (str): The name of the gold layer.
        macros_path (str): The path to the nesso macros directory.
        default_env (str): The default environment to use.
        nesso_cli_version (str): The version of nesso CLI used by the project.
        luma (bool): Whether to enable Luma Data Catalog integration.
        snakecase_columns (bool): Whether to standardize column names to snakecase.

    """
    project_variables = {
        "project_name": project_name,
        "data_architecture": data_architecture,
        "db_type": db_type,
        "bronze_schema": bronze_schema,
        "silver_schema": silver_schema,
        "silver_schema_prefix": silver_schema_prefix,
        "gold_layer_name": gold_layer_name,
        "macros_path": macros_path,
        "default_env": default_env,
        "nesso_cli_version": nesso_cli_version,
        "luma": luma,
        "snakecase_columns": snakecase_columns,
    }
    project_dir = Path(project_name)

    for file in TEMPLATE_FILES_TO_RENDER:
        if file == "config.yml":
            output_dir_path = project_dir / ".nesso"
        elif file == "{{ bronze_schema }}.yml":
            output_dir_path = project_dir / "models" / "sources" / bronze_schema
        else:
            output_dir_path = project_dir
        render_jinja_template_file(
            template_path=file,
            output_dir_path=output_dir_path,
            **project_variables,  # type: ignore
        )


@app.command()
def project(
    project_name: Annotated[
        str, typer.Option("--project-name", "-p", prompt="Project name")
    ] = config.project_name,
    db_type: Annotated[
        str,
        typer.Option(
            "--database-type",
            "-t",
            prompt="Database type",
            click_type=click.Choice(list(dbt_config_map.keys())),
        ),
    ] = config.database_type,
    db_kwargs: Annotated[
        str | None,
        typer.Option(
            "--db-kwargs", "-k", help="The parameters to pass to the database config"
        ),
    ] = None,
    data_architecture: Annotated[
        str,
        typer.Option(
            "--data-architecture",
            "-d",
            click_type=click.Choice(["marts", "medallion"]),
        ),
    ] = config.data_architecture,
    bronze_schema: Annotated[
        str,
        typer.Option("--bronze-schema", "-b", prompt="Bronze layer schema"),
    ] = config.bronze_schema,
    silver_schema: Annotated[
        str,
        typer.Option("--silver-schema", "-s", prompt="Silver layer schema"),
    ] = config.silver_schema,
    silver_schema_prefix: Annotated[
        str,
        typer.Option("--silver-schema-prefix", "-sp", prompt="Silver schema prefix"),
    ] = config.silver_schema_prefix,
    gold_layer_name: Annotated[
        str, typer.Option("--gold-layer-name", "-g", prompt="Gold layer")
    ] = config.gold_layer_name,
    luma: Annotated[
        bool,
        typer.Option(
            "--luma", "-l", prompt="Enable Luma Data Catalog integration?", is_flag=True
        ),
    ] = config.luma["enabled"],
    snakecase_columns: Annotated[
        bool,
        typer.Option(
            "--snakecase_columns",
            "-sc",
            prompt="Whether to standardize column names to snakecase",
            is_flag=True,
        ),
    ] = config.snakecase_columns,
    no_install_dependencies: Annotated[
        bool,
        typer.Option(
            "--no-install-dependencies",
            is_flag=True,
        ),
    ] = False,
):
    """Initialize a new nesso-models project :rocket:.

    -----------------------------------------

    Create a new project directory with the following structure:

    <project_name>
    ├── .gitignore  # Git config file.
    |── .luma  # (optional) Luma Data Catalog config file.
    ├── .nesso
    │   └── config.yml  # Project config file.
    ├── dbt_project.yml  # Project config file.
    ├── models
    │   ├── <silver_schema>  # Silver schema models.
    │   ├── <gold_layer>  # Gold layer models.
    │   └── sources
    │       └── <bronze_schema>  # Bronze tables.
    │           └── <bronze_schema>.yml  # Bronze table metadata.
    ├── packages.yml  # Internal project dependencies.
    ├── prepare.sh  # A helper installation script.
    ├── profiles.yml.example  # Example dbt profiles.yml.
    ├── README.md  # Template project README.
    └── requirements.txt  # nesso-cli version used by the project.

    Args:
        project_name (Annotated[str, typer.Option], optional): The name of the project.
        db_type (Annotated[str, typer.Option], optional): The database type that
            the project will connect to.
        db_kwargs (Annotated[str, typer.Option], optional): JSON-encoded parameters to
            pass to the database config. For example, `'{"host": "localhost"}'`.
        data_architecture (Annotated[str, typer.Option], optional): The data
            architecture to use.
        bronze_schema (Annotated[str, typer.Option], optional): The schema where
            raw data is ingested ("input schema").
        silver_schema (Annotated[str, typer.Option], optional): The intermediate
            schema between raw data and user-facing models.
        silver_schema_prefix (Annotated[str, typer.Option], optional): The prefix to use
            for models in the silver schema.
        gold_layer_name (Annotated[str, typer.Option], optional): The name of the gold
            layer.
        luma (Annotated[bool, typer.Option], optional): Whether to enable Luma Data
            Catalog integration.
        snakecase_columns (Annotated[bool, typer.Option], optional): Whether to
            standardize column names to snakecase.
        no_install_dependencies (Annotated[bool, typer.Option], optional): Whether to
            skip installing project dependencies.

    """
    # There is no good way to provide empty input in Typer, so we have to handle
    # various options.
    empty_values = ("None", "null", "none", '""', "''")
    if not silver_schema_prefix or silver_schema_prefix in empty_values:
        silver_schema_prefix = ""

    project_dir = Path(project_name)

    if db_type not in dbt_config_map:
        raise NotImplementedError(f"Unsupported database type: '{db_type}'.")

    if project_dir.is_dir():
        print(f"Project `{project_name}` already exists. Type `Ctrl+C` to abort.")

    # Create directory structure
    create_directory_structure(
        project_dir=project_dir,
        bronze_schema=bronze_schema,
        silver_schema=silver_schema,
        gold_layer_name=gold_layer_name,
    )

    # Copy hardcoded template files to project directory.
    for path in TEMPLATE_FILES_TO_COPY:
        source_path = TEMPLATES_DIR / path
        destination_path = project_dir / path

        if source_path.is_dir():
            destination_path.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
        else:
            shutil.copy(source_path, destination_path)

    render_project_files(
        project_name=project_name,
        data_architecture=data_architecture,
        db_type=db_type,
        bronze_schema=bronze_schema,
        silver_schema=silver_schema,
        silver_schema_prefix=silver_schema_prefix,
        gold_layer_name=gold_layer_name,
        macros_path=config.macros_path,
        default_env=config.default_env,
        nesso_cli_version="v" + metadata.version("nesso_cli"),
        luma=luma,
        snakecase_columns=snakecase_columns,
    )

    # Create `profiles.yml` template file based on database type.
    if db_kwargs:
        create_profiles_yml_template(
            db_type=db_type, project_name=project_name, **json.loads(db_kwargs)
        )
    else:
        create_profiles_yml_template(db_type=db_type, project_name=project_name)

    if no_install_dependencies:
        result = ""
    else:
        result = call_shell(f"cd {project_name} && dbt deps", print_logs=False)

    if "ERROR" not in result:
        print("Project initialized [green]successfully[/].")


#################
### user init ###
#################
def _generate_user_profile(
    template_profiles_yml_path: str | Path = "profiles.yml.example",
    **kwargs,
) -> dict[str, Any]:
    # Check if the command is being ran from within a nesso project.
    if not Path(template_profiles_yml_path).exists():
        msg = f"""profiles.yml.example file not found. Please ensure you are running the
command from inside a nesso project and try again.

Provided path: {template_profiles_yml_path}
"""
        raise FileNotFoundError(msg)

    # Extract user config from the nested profiles.yml structure.
    with open(template_profiles_yml_path) as file:
        profiles_template = yaml.load(file)
    project_name = list(profiles_template.keys())[0]
    profile = profiles_template[project_name]
    target = profile["target"]
    config = profile["outputs"][target]

    # Get user credentials.
    for key in config:
        if key not in kwargs:
            if key in USER_CREDENTIAL_FIELDS:
                password = True if key in PRIVATE_USER_FIELDS else False
                value = Prompt.ask(
                    f"Please provide your {key}",
                    default=config[key],
                    password=password,
                )
            else:
                continue
        else:
            value = kwargs[key]

        config[key] = value

    # Get user schema.
    username = config.get("user")
    if username:
        # Normalize the username.
        username.replace(".", "_").split("@")[0]

    if "schema" not in kwargs:
        if username:
            default_schema = f"dbt_{username}"
        else:
            default_schema = "dbt"
        schema = Prompt.ask("Please provide your schema", default=default_schema)
    else:
        schema = kwargs["schema"]
    config["schema"] = schema
    profiles_complete = {project_name: {"target": target, "outputs": {target: config}}}
    return profiles_complete


def _run_dbt_cmd(
    command: str, pre_msg: str | None = None, post_msg: str | None = None
) -> None:
    """Run a dbt command."""
    try:
        if pre_msg:
            print(pre_msg)
        call_shell(f"dbt {command}", print_logs=False)
        if post_msg:
            print(post_msg)
    except subprocess.CalledProcessError:
        print(f"Error running `dbt {command}`.")
        print("For more information, please see the command output above.")
        sys.exit(1)


@app.command(context_settings=wrapper_context_settings)
def user(
    ctx: typer.Context,
    profiles_path: Annotated[
        str, typer.Option("--profiles-path", "-p")
    ] = "~/.dbt/profiles.yml",
    no_install_dependencies: Annotated[
        bool,
        typer.Option(
            "--no-install-dependencies",
            is_flag=True,
        ),
    ] = False,
    no_generate_profiles: Annotated[
        bool,
        typer.Option(
            "--no-generate-profiles",
            is_flag=True,
        ),
    ] = False,
) -> None:
    """Create a user config and install any necessary packages.

    kwargs (dict): Keyword arguments to pass to `_generate_user_profile()`.
    """

    def process_arg(arg: tuple[str, str]) -> tuple[str, str]:
        k, v = arg

        # Convert CLI format to Python convention (eg. --my-param -> my_param).
        k = k.lstrip("-").replace("-", "_")

        # Resolve any paths to allow providing relative paths and expansions (~/).
        v = str(Path(v).expanduser().resolve()) if "path" in k else v

        return k, v

    if not no_generate_profiles:
        # Construct kwargs from a list of args in the format
        # ["--param1", "value1", ...].
        kwargs = {
            process_arg(arg)[0]: process_arg(arg)[1]
            for arg in zip(ctx.args[::2], ctx.args[1::2], strict=False)
        }

        profile = _generate_user_profile(**kwargs)

        profiles_path = str(Path(profiles_path).expanduser().resolve())

        if Path(profiles_path).exists():
            with open(profiles_path) as file:
                profiles = yaml.load(file)
            profiles.update(profile)
        else:
            profiles = profile

        profile_name = list(profile.keys())[0]
        print(
            f"Creating user profile '{profile_name}' in [bright_black]{profiles_path}[/]..."
        )

        # Ensure that the output directory exists.
        Path(profiles_path).parent.mkdir(parents=True, exist_ok=True)

        with open(profiles_path, "w") as file:
            yaml.dump(profiles, file)
        print("User profile has been created [green]successfully[/].")

    _run_dbt_cmd(
        "debug",
        pre_msg="Validating user configuration...",
        post_msg="Configuration has been validated [green]successfully[/].",
    )
    if not no_install_dependencies:
        _run_dbt_cmd(
            "deps",
            pre_msg="Installing project dependencies...",
            post_msg="Packages have been installed [green]successfully[/].",
        )
        _run_dbt_cmd(
            "seed",
            pre_msg="Loading seed data...",
            post_msg="Seed data has been loaded [green]successfully[/].",
        )

    # Fix dbt utils bug.
    # See https://github.com/dbt-labs/dbt-utils/issues/627.
    shutil.rmtree(
        Path(
            "dbt_packages",
            "dbt_utils",
            "tests",
        ),
        ignore_errors=True,
    )

    print("[green]All set![/]")


if __name__ == "__main__":
    app()
