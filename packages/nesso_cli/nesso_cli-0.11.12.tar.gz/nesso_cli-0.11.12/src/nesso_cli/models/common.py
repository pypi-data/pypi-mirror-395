import contextlib
import functools
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from subprocess import PIPE, STDOUT, Popen
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, Dict, Literal, Optional

import agate
import typer
from dbt.adapters.base.relation import BaseRelation
from loguru import logger
from typing_extensions import Annotated

import nesso_cli.models.context as context
from nesso_cli.models._vendored.dbt_core_interface import DbtProject
from nesso_cli.models.config import config, yaml

if TYPE_CHECKING:
    from nesso_cli.models.resources import NessoDBTModel


logger.remove(0)
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",  # noqa
)


def force(help="Whether to overwrite existing resource."):
    return Annotated[
        Optional[bool],
        typer.Option(
            "--force",
            "-f",
            help=help,
            is_flag=True,
        ),
    ]


options = SimpleNamespace(
    technical_owner=Annotated[
        Optional[str],
        typer.Option(
            "--technical-owner", "-t", help="The technical owner of this dataset."
        ),
    ],
    business_owner=Annotated[
        Optional[str],
        typer.Option(
            "--business-owner", "-b", help="The business owner of this dataset."
        ),
    ],
    domains=Annotated[
        Optional[list[str]],
        typer.Option("--domain", "-d", help="The domain(s) this dataset belongs to."),
    ],
    source_systems=Annotated[
        Optional[list[str]],
        typer.Option(
            "--source-system",
            "-ss",
            help="The source system(s) from which this data is coming.",
        ),
    ],
    environment=Annotated[
        str, typer.Option("--env", "-e", help="The environment to use.")
    ],
    project=Annotated[
        Optional[str],
        typer.Option(
            "--project",
            "-p",
            help="The name of the project to use.",
        ),
    ],
    force=force,
)


def call_shell(
    command: str,
    shell: str = "bash",
    print_logs: bool = True,
    args: list[str] | None = None,
) -> str:
    """Execute a shell command and streams the output in a pretty way."""

    if args:
        command += " " + " ".join(args)

    with tempfile.NamedTemporaryFile(prefix="nesso-") as tmp:
        tmp.write(command.encode())
        tmp.flush()
        with Popen([shell, tmp.name], stdout=PIPE, stderr=STDOUT) as sub_process:
            line = None
            lines = []
            for raw_line in iter(sub_process.stdout.readline, b""):
                line = raw_line.decode("utf-8").rstrip()

                lines.append(line)
                if print_logs:
                    logger.info(line)

            sub_process.wait()
            if sub_process.returncode:
                msg = f"Command failed with exit code {sub_process.returncode}"
                for line in lines:
                    logger.error(line)
                logger.error(msg)

                failed_command = ""
                with open(tmp.name) as f:
                    for line in f:
                        failed_command = failed_command + line

                raise subprocess.CalledProcessError(
                    sub_process.returncode, failed_command
                )
            else:
                # Due to some internal exception handling logic in Popen, we need to
                # make sure that the `output` variable is unassigned unless the function
                # executes successfully, otherwise the `output` variable will be
                # returned regardless whether an exception was raised or not.
                output = "\n".join(lines)

    return output


def get_current_dbt_project_path() -> Path:
    """Get the path to the current dbt project.

    Returns:
        Path: The path to the current dbt project.
    """
    cwd = os.getcwd()

    dbt_project_paths = []
    while cwd != os.path.dirname(cwd):
        dbt_project_paths = [path for path in Path(cwd).rglob("*dbt_project.yml")]
        if dbt_project_paths:
            break
        cwd = os.path.dirname(cwd)

    if not dbt_project_paths:
        raise ValueError("Could not locate dbt_project.yml.")

    # The first path on the list is the dbt project closest to our current working
    # directory.
    return Path(dbt_project_paths[0]).parent


def get_project_name(dbt_project_path: str | Path) -> str:
    """Retrieve the name of a dbt project given its path.

    Args:
        dbt_project_path (str | Path): The path to the dbt project.

    Returns:
        str: The name of the dbt project.
    """

    with open(Path(dbt_project_path) / "dbt_project.yml") as f:
        config = yaml.load(f)

    project_name = config.get("name")

    if project_name is None:
        raise ValueError(f"Could not locate project name in {dbt_project_path}.")

    return project_name


def run_in_dbt_project(func: callable, dbt_project_dir: Path | None = None) -> callable:
    """Execute a function in project's root directory.

    Args:
        func (callable): The function to decorate.
        dbt_project_dir (Path | None, optional): The dbt project directory
            to which to cd. Defaults to None.

    Raises:
        e: Exception raised by the decorated function.

    Returns:
        callable: The decorated function.
    """
    dbt_project_path = dbt_project_dir or get_current_dbt_project_path()

    def _decorate(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            if not dbt_project_path:
                return False

            original_directory = os.getcwd()
            os.chdir(dbt_project_path)
            """
            Ensure we go back to original dir
            even if the function throws an exception.
            """
            try:
                original_func_return_value = function(*args, **kwargs)
            except Exception as e:
                raise e
            finally:
                os.chdir(original_directory)
            return original_func_return_value

        return wrapper

    if func:
        return _decorate(func)

    return _decorate


def get_dbt_target(profiles_path: str | Path, project_name: str) -> str:
    """Retrieve the name of the default dbt target from specified profiles.yml file.

    Args:
        profiles_path (str | Path): The path to the dbt profiles.yml.
        project_name (str | Path): The name of the project for which to
            lookup the target.

    Raises:
        ValueError: If falling back to the default target, but it's not specified
        in the profiles file.

    Returns:
        str: The name of the default dbt target.
    """

    with open(profiles_path) as f:
        dbt_profiles = yaml.load(f)

    project_profile = dbt_profiles.get(project_name, {})
    target = project_profile.get("target")

    if target is None:
        raise ValueError(
            f"""Default target for project {project_name} could not be located
            in '{profiles_path}'"""
        )

    return target


def get_local_schema(
    profiles_path: str | Path | None = None,
    project_name: str | None = None,
    target: str | None = None,
) -> str:
    """Get the name of the local dbt schema from profiles.yml.

    Args:
        profiles_dir (str | Path): The path to the profiles.yml file.
        project_name (str): The name of the dbt project for which to get the schema.
        target (str, optional): The name of the dbt target for which to get the schema.
            By default, the default target specified in profiles.yml.

    Raises:
        ValueError: If the target is not specified and not present in the dbt profiles
            file.

    Returns:
        str: The name of the currently used dbt schema.
    """

    if target == "prod":
        raise ValueError("Production schema config is specified in dbt_project.yml.")

    if not profiles_path:
        profiles_path = get_current_dbt_profiles_dir() / "profiles.yml"

    if not project_name:
        project_path = get_current_dbt_project_path()
        project_name = get_project_name(project_path)

    with open(profiles_path) as f:
        dbt_profiles = yaml.load(f)

    project_profile = dbt_profiles.get(project_name, {})
    target = target or project_profile.get("target")

    if target is None:
        raise ValueError(
            f"""The target of project '{project_name}' was not found
            in '{profiles_path}'."""
        )

    schema = project_profile["outputs"][target].get("schema")

    if schema is None:
        raise ValueError(f"Could not locate current schema in {profiles_path}.")

    return schema


def snakecase(string: str) -> str:
    """Convert a string to snakecase.

    Args:
        string (str): The string to convert.

    Returns:
        str: The snakecased string.
    """
    return string.lower().replace("-", "_")


def get_current_dbt_profile() -> str | None:
    """Get the name of the currently used dbt profile.

    Returns:
        str | None: The name of the currently used dbt profile.
    """
    dbt_project_dir = get_current_dbt_project_path()
    if dbt_project_dir is not None:
        with open(dbt_project_dir.joinpath("dbt_project.yml")) as f:
            config = yaml.load(f)
        return config.get("profile")


def get_current_dbt_profiles_dir() -> Path:
    """Get the path to the currently used profiles.yml file.

    Order of checking:
        project directory -> environment -> ~/.dbt/profiles.yml.

    Returns:
        Path: The directory containing the currently used profiles.yml file.
    """
    current_profile_name = get_current_dbt_profile()
    current_project_dir = get_current_dbt_project_path()
    if current_project_dir:
        # Prioritize project-specific profiles.yml.
        current_project_profiles_yml_path = Path(current_project_dir) / "profiles.yml"
        if current_project_profiles_yml_path.exists():
            with open(current_project_profiles_yml_path) as f:
                profiles = yaml.load(f)
                if current_profile_name in profiles:
                    return current_project_profiles_yml_path.parent.resolve()

    # Next, check the environment.
    if "DBT_PROFILES_DIR" in os.environ:
        return Path(os.environ["DBT_PROFILES_DIR"]).resolve()

    # Otherwise, return dbt's default profiles.yml location.
    default_dbt_profiles_dir = Path.home() / ".dbt"
    return default_dbt_profiles_dir.resolve()


def check_if_relation_exists(
    name: str, schema: str, target: Optional[str] = None
) -> bool:
    """Check if a relation (table/view) exists in the database.

    NOTE: due to dbt's incorrect use of caching, we use the
    `list_relations_without_caching()` method instead of `relation_exists()`,
    as `relation_exists()` returns incorrect results in some cases.

    Args:
        name (str): The name of the relation.
        schema (str): The schema of the relation.
        target (Optional[str], optional): The name of the dbt target to use.
            Defaults to None.

    Returns:
        bool: Whether the relation exists.
    """

    dbt_project_obj = get_current_dbt_project_obj(target=target)
    # We need a schema relation object for list_relations_without_caching(),
    # but dbt doesn't provide a way of instantiating one.
    # As a workaround, we use BaseRelation to get a table relation object
    # and remove the table part to get the schema relation object.
    _ = BaseRelation.create(
        database=dbt_project_obj.adapter.config.credentials.database,
        schema=schema,
        identifier="abc",
    )
    schema_relation = _.without_identifier()
    with dbt_project_obj.adapter.connection_named("__nesso_models__"):
        relation_objects = dbt_project_obj.adapter.list_relations_without_caching(
            schema_relation
        )
        relations = [relation_object.identifier for relation_object in relation_objects]
        return name in relations


def execute_sql(
    sql: str,
    dbt_project: DbtProject | None = None,
    commit: bool = False,
    target: Optional[str] = None,
) -> agate.Table | None:
    """Execute SQL in the project's database.

    This adds the ability to execute DML queries on top of what's provided by
    dbt-core-interface. There's an issue to add this functionality there:
    https://github.com/z3z1ma/dbt-core-interface/issues/115.

    """
    dbt_project = dbt_project or get_current_dbt_project_obj(target=target)
    adapter = dbt_project.adapter

    if not commit:
        with adapter.connection_named("__nesso_models__"):
            return dbt_project.execute_code(sql).table

    with adapter.connection_named("__nesso_models__"):
        conn = adapter.connections.get_thread_connection()
        cursor = conn.handle.cursor()
        try:
            cursor.execute(sql)
            conn.handle.commit()
        except Exception:
            conn.transaction_open = False
        finally:
            return None


def get_current_dbt_project_obj(target: Optional[str] = None, recompile: bool = False):
    """Util to defer the instantiation of a "singleton" DbtProject."""
    current_project_path = get_current_dbt_project_path()
    current_profiles_path = get_current_dbt_profiles_dir()

    DBT_PROJECT = context.get("DBT_PROJECT")
    if not DBT_PROJECT or recompile:
        DBT_PROJECT = DbtProject(
            project_dir=str(current_project_path),
            profiles_dir=str(current_profiles_path),
            target=target,
        )
        context.set("DBT_PROJECT", DBT_PROJECT)
    return DBT_PROJECT


def get_db_table_columns(
    table_name: str,
    schema_name: Optional[str],
    env: Optional[str] = None,
) -> Dict[str, str]:
    """Retrieve information about the columns of a database table.

    Args:
        table_name (str): The name of the table.
        schema_name (Optional[str], optional): The name of the schema
            containing the table. Provide the name in the case of scanning source.
            Default to None.
        env (Optional[str], optional): The environment name.
            Defaults to None.

    Raises:
        ValueError: If the node for the specified table cannot be found.

    Returns:
        Dict[str, str]: A dictionary containing column names as keys
            and their data types as values.
    """
    dbt_project = get_current_dbt_project_obj(target=env, recompile=True)
    adapter = dbt_project.adapter

    if schema_name:
        node = dbt_project.get_source_node(
            target_source_name=schema_name, target_table_name=table_name
        )
    else:
        node = dbt_project.get_ref_node(target_model_name=table_name)

    if node is None:
        raise ValueError(f"Could not find node for table {table_name}")

    with adapter.connection_named("__nesso_models__"):
        # Assigning the first value in a tuple, which is a list of columns
        columns_list, *_ = dbt_project.get_columns_in_node(node)

    columns_dict = {}

    for column in columns_list:
        columns_dict.update({column.name: column.data_type.upper()})

    return columns_dict


def drop(
    name: str,
    schema: str,
    kind: Literal["view", "table"] = "view",
    cascade: bool = False,
) -> None:
    """Drop a relation from the project's database.

    Args:
        name (str): The name of the relation to drop.
        schema (str): The schema of the relation to drop.
        kind (Literal["view", "table"], optional): Relation kind. Defaults to "view".
        cascade (bool, optional): Whether to use CASCADE. Defaults to False.
    """
    logger.info(f"Dropping {kind} '{schema}.{name}'...")

    sql = f"DROP {kind.upper()} IF EXISTS {schema}.{name}"
    if cascade:
        sql += " CASCADE"

    execute_sql(sql, commit=True)

    logger.info(f"Successfully dropped {kind} '{schema}.{name}'.")


PROJECT_DIR = get_current_dbt_project_path()
wrapper_context_settings = {"allow_extra_args": True, "ignore_unknown_options": True}


def convert_list_of_options_to_dict(options: list[str]) -> dict[str, str]:
    """Convert a list of string-serialized CLI options to a dictionary.

    Note: does not handle flags.

    Args:
        options (list[str]): A list of options and their values.

    Returns:
        dict[str, str]: Option-value pairs extracted from the list.

    Raises:
        ValueError: If the arguments are not provided in the correct format. Each option
        should follow the pattern '--option value'.

    Example:
        >>> convert_list_of_options_to_dict(["--name", "John", "--age", "30"])
        {'name': 'John', 'age': '30'}
    """

    def validate(options: list[str]):
        # Each option must have a value, so the list will be of even length.
        is_valid = len(options) % 2 == 0

        # Check that each option is followed by a value.
        for i in range(0, len(options), 2):
            try:
                if not options[i].startswith("--") or options[i + 1].startswith("--"):
                    is_valid = False
            except IndexError:
                is_valid = False

        if not is_valid:
            msg = "Options should be specified in the format '--option value'."
            raise ValueError(msg)

    def deserialize(value):
        # Deserialize a value from string encoding.
        with contextlib.suppress(json.decoder.JSONDecodeError):
            # Decoding error happens if the value is actually a string.
            value = json.loads(value)
        return value

    validate(options)

    options_dict = {}
    for index, option_with_prefix in enumerate(options):
        if index % 2 == 0:
            option = option_with_prefix[2:]
            value = deserialize(options[index + 1])
            options_dict[option] = value
    return options_dict


def profile(
    model_name: str, base: bool = False, env: str | None = None
) -> dict[str, Any]:
    """Print basic information about the model's underlying relation."""
    from nesso_cli.models.resources import NessoDBTModel

    if env is None:
        env = config.default_env

    model = NessoDBTModel(name=model_name, base=base, env=env)

    fqn = f"{model.node.schema}.{model.node.identifier}"
    row_count_query = (
        f"select cast(count(*) as {{{{ dbt.type_numeric() }}}}) from {fqn}"
    )
    nrows_query_result = execute_sql(row_count_query, dbt_project=model.dbt_project)
    nrows = int(nrows_query_result.rows[0].values()[0])
    try:
        size = _get_model_size(model)
    except NotImplementedError:
        size = None
    size_pretty = str(size) + " MB" if size is not None else None
    return {"nrows": nrows, "size": size_pretty}


def _get_model_size(model: "NessoDBTModel") -> int:
    """Retrieve the size of the model in MB, rounded to the nearest integer."""

    materialization = model.node.get_materialization()

    if materialization == "view":
        return 0

    elif materialization != "table":
        return NotImplementedError

    adapter_type = model.dbt_project.adapter.type()
    schema = model.node.schema
    table = model.node.identifier

    if adapter_type == "postgres":
        query_template = "select pg_total_relation_size('{schema}.{table}')"
    elif adapter_type == "redshift":
        query_template = """
select size from svv_table_info
where schema = '{schema}' and "table" = '{table}'
"""
    elif adapter_type == "sqlserver":
        # SQLServer returns a non-machine-readable output so we need to do some
        # gymnastics to get the number.
        query_template = """
DECLARE @spaceUsed TABLE (
name varchar(255),
rows int,
reserved varchar(50),
data varchar(50),
index_size varchar(50),
unused varchar(50))

INSERT INTO @spaceUsed
exec sp_spaceused '{schema}.{table}'

SELECT cast(replace(reserved, ' kb', '') as int) / 1024 FROM @spaceUsed;
"""
    elif adapter_type == "duckdb":
        # It seems there is no way to retrieve table sizes in DuckDB.
        raise NotImplementedError
    elif adapter_type == "trino":
        query_template = (
            "EXPLAIN (TYPE IO, FORMAT JSON) select * from '{schema}.{table}'"
        )

    query_result = execute_sql(query_template.format(schema=schema, table=table))
    result_value = query_result.rows[0].values()[0]
    if adapter_type == "trino":
        size = result_value["estimate"]["outputSizeInBytes"] / 1024 / 1024
    else:
        size = result_value
    return size


def dict_diff(dict1: dict[Any, Any], dict2: dict[Any, Any]) -> dict[Any, Any]:
    """Find the differences between two dictionaries.

    Union a difference of two sets in order to get a diff of two dicts.

    Args:
        dict1 (dict[Any, Any]): The first dictionary.
        dict2 (dict[Any, Any]): The second dictionary.

    Returns:
        dict[Any, Any]: If the dictionaries are not equal, returns a dictionary
            containing the differing key-value pairs. If the dictionaries are equal,
            returns empty dictionary.
    """
    if dict1 != dict2 or dict2 != dict1:
        result = dict(dict1.items() - dict2.items())
        result2 = dict(dict2.items() - dict1.items())
        final_result = result | result2

        return final_result

    return {}
