import os
import shutil
from pathlib import Path

import agate
import nesso_cli.models.context as context
import pytest
from conftest import TestData, test_tables_nrows
from nesso_cli.models.common import (
    call_shell,
    check_if_relation_exists,
    convert_list_of_options_to_dict,
    dict_diff,
    drop,
    execute_sql,
    get_current_dbt_profile,
    get_current_dbt_profiles_dir,
    get_current_dbt_project_obj,
    get_db_table_columns,
    get_dbt_target,
    get_local_schema,
    get_project_name,
    profile,
    run_in_dbt_project,
)
from nesso_cli.models.config import config, yaml

PROJECT_NAME = "postgres"
PROJECT_DIR = Path(__file__).parent.joinpath("dbt_projects", PROJECT_NAME)
context.set("PROJECT_DIR", PROJECT_DIR)


@pytest.fixture(scope="function")
def FAKE_DBT_PROFILES_DIR():
    profiles_dir = "/tmp/fake_project"

    shutil.rmtree(profiles_dir, ignore_errors=True)
    Path(profiles_dir).mkdir(parents=True, exist_ok=True)

    yield Path(profiles_dir)

    shutil.rmtree(profiles_dir, ignore_errors=True)


@pytest.fixture(scope="function")
def FAKE_DBT_PROFILES_PATH(FAKE_DBT_PROFILES_DIR):
    profiles_dir = FAKE_DBT_PROFILES_DIR.joinpath("profiles.yml")
    profiles_dir.unlink(missing_ok=True)

    yield profiles_dir

    profiles_dir.unlink(missing_ok=True)


def test_call_shell():
    command = "/usr/bin/ls"
    result = call_shell(command)
    files = result.split("\n")
    assert "dbt_project.yml" in files


def test_call_shell_with_args():
    command = "/usr/bin/ls"
    args = ["-a"]
    result = call_shell(command, args=args)
    files = result.split("\n")
    assert ".nesso" in files


def test_run_in_dbt_project():
    @run_in_dbt_project
    def check_if_in_dbt_project():
        cwd = os.getcwd()
        return str(cwd) == str(PROJECT_DIR)

    decorator_works = check_if_in_dbt_project()
    assert decorator_works


def test_get_current_dbt_project():
    postgres_project_dir = (
        Path(__file__).parent.absolute().joinpath("dbt_projects", "postgres")
    )
    project = get_project_name(postgres_project_dir)

    assert project == "postgres"


def test_get_dbt_target(FAKE_DBT_PROFILES_DIR, FAKE_DBT_PROFILES_PATH):
    test_target = "test_target"
    fake_profiles = {PROJECT_NAME: {"target": test_target, "outputs": {}}}
    with open(FAKE_DBT_PROFILES_PATH, "w") as f:
        yaml.dump(fake_profiles, f)

    target = get_dbt_target(
        profiles_path=FAKE_DBT_PROFILES_PATH, project_name=PROJECT_NAME
    )
    assert target == test_target


def test_get_local_schema(FAKE_DBT_PROFILES_DIR, FAKE_DBT_PROFILES_PATH):
    test_target = "test_target"
    test_schema = "test_schema"
    fake_profiles = {
        PROJECT_NAME: {
            "target": test_target,
            "outputs": {test_target: {"schema": test_schema}},
        }
    }
    with open(FAKE_DBT_PROFILES_PATH, "w") as f:
        yaml.dump(fake_profiles, f)

    schema = get_local_schema(
        profiles_path=FAKE_DBT_PROFILES_PATH, project_name=PROJECT_NAME
    )
    assert schema == test_schema

    # Ensure 'prod' target is not supported.
    with pytest.raises(ValueError):
        get_local_schema(
            profiles_path=FAKE_DBT_PROFILES_PATH,
            project_name=PROJECT_NAME,
            target="prod",
        )


def test_get_current_dbt_profile():
    # Setup.
    working_dir = os.getcwd()

    postgres_project_dir = (
        Path(__file__).parent.absolute().joinpath("dbt_projects", "postgres")
    )
    trino_project_dir = (
        Path(__file__).parent.absolute().joinpath("dbt_projects", "trino")
    )

    # Test.
    os.chdir(postgres_project_dir)
    profile = get_current_dbt_profile()
    assert profile == "postgres"

    os.chdir(trino_project_dir)
    profile = get_current_dbt_profile()
    assert profile == "trino"

    # Cleanup.
    os.chdir(working_dir)


def test_get_current_dbt_profiles_dir():
    working_dir = os.getcwd()

    postgres_project_dir = (
        Path(__file__).parent.absolute().joinpath("dbt_projects", "postgres")
    )
    os.chdir(postgres_project_dir)

    profiles_dir = get_current_dbt_profiles_dir()

    assert profiles_dir == postgres_project_dir

    # Cleanup.
    os.chdir(working_dir)


def test_get_db_table_columns(setup_source, TEST_SOURCE, TEST_TABLE_ACCOUNT):
    # Setup.
    working_dir = os.getcwd()

    postgres_project_dir = (
        Path(__file__).parent.absolute().joinpath("dbt_projects", "postgres")
    )
    os.chdir(postgres_project_dir)

    # Test.
    data = get_db_table_columns(table_name=TEST_TABLE_ACCOUNT, schema_name=TEST_SOURCE)
    assert data == {
        "id": "BIGINT",
        "name": "TEXT",
        "email": "TEXT",
        "mobile": "TEXT",
        "country": "TEXT",
        "_viadot_downloaded_at_utc": "TIMESTAMP WITHOUT TIME ZONE",
    }

    # Cleanup.
    os.chdir(working_dir)


def test_get_current_dbt_project_obj():
    # Setup.
    working_dir = os.getcwd()

    postgres_project_dir = (
        Path(__file__).parent.absolute().joinpath("dbt_projects", "postgres")
    )
    os.chdir(postgres_project_dir)

    # Test.
    project = get_current_dbt_project_obj()
    assert project.config.project_name == "postgres"

    # Cleanup.
    os.chdir(working_dir)


def test_check_if_relation_exists(postgres_connection):
    seed = "countries_example"
    schema = config.bronze_schema

    # Assumptions.
    assert not check_if_relation_exists(schema=schema, name=seed)

    # Create table.
    call_shell(f"dbt seed -s {seed} -t prod")

    # Validate.
    assert check_if_relation_exists(schema=schema, name=seed)

    # Cleanup.
    postgres_connection.execute(f"DROP TABLE IF EXISTS {schema}.{seed};")


def test_execute_sql_fetches_data(TEST_TABLE_CONTACT):
    # Assumptions.
    schema = config.bronze_schema
    assert check_if_relation_exists(schema=schema, name=TEST_TABLE_CONTACT)

    # Test.
    sql = f"SELECT * FROM {schema}.{TEST_TABLE_CONTACT};"
    table = execute_sql(sql)
    assert isinstance(table, agate.Table)
    assert len(table.rows) == 100


def test_drop(postgres_connection):
    # Set up.
    table_schema = config.bronze_schema
    table_name = "test_table"
    table_fqn = f"{table_schema}.{table_name}"
    view_schema = config.silver_schema
    view_name = "test_view"
    view_fqn = f"{view_schema}.{view_name}"

    postgres_connection.execute(f"CREATE TABLE IF NOT EXISTS {table_fqn} (id int);")
    postgres_connection.execute(f"CREATE SCHEMA IF NOT EXISTS {view_schema};")
    postgres_connection.execute(
        f"CREATE OR REPLACE VIEW {view_fqn} AS SELECT * FROM {table_fqn};"
    )

    # Assumptions.
    assert check_if_relation_exists(schema=table_schema, name=table_name)
    assert check_if_relation_exists(schema=view_schema, name=view_name)

    # Test.
    drop(name=view_name, schema=view_schema, kind="view")
    assert not check_if_relation_exists(schema=view_schema, name=view_name)

    drop(name=table_name, schema=table_schema, kind="table")
    assert not check_if_relation_exists(schema=table_schema, name=table_name)

    # Cleanup.
    postgres_connection.execute(f"DROP TABLE IF EXISTS {table_fqn};")
    postgres_connection.execute(f"DROP VIEW IF EXISTS {view_fqn};")
    postgres_connection.execute(f"DROP SCHEMA IF EXISTS {view_schema} CASCADE;")


@pytest.mark.parametrize(
    "options, expected_dict",
    [
        (["--key1", "val1", "--key2", "val2"], {"key1": "val1", "key2": "val2"}),
        (["--key1", "value-2", "--key2", "val2"], {"key1": "value-2", "key2": "val2"}),
        ([], {}),
    ],
)
def test_convert_list_of_options_to_dict(options, expected_dict):
    data = convert_list_of_options_to_dict(options)
    assert data == expected_dict


@pytest.mark.parametrize(
    "options",
    [
        ["--key1", "val1", "--key2"],
        ["key1", "val1", "--key2"],
        ["--key1", "val1", "--key2", "--value2"],
        ["key1", "--val1", "key2", "--value2"],
    ],
)
def test_convert_list_of_options_to_dict_handles_incorrect_input(options):
    with pytest.raises(ValueError):
        convert_list_of_options_to_dict(options)


def test_profile(setup_model):
    info = profile(TestData.model.name)
    assert info["nrows"] == test_tables_nrows
    assert info["size"] == "0 MB"


def test_dict_diff_equal():
    """Verify that dict_diff() returns correct diff for equal dictionaries."""
    dict1 = {"a": 1, "b": 2, "c": 3}
    dict2 = dict1
    diff = dict_diff(dict1, dict2)
    assert diff == {}


def test_dict_diff_different():
    """Verify that dict_diff() returns correct diff for different dictionaries."""
    dict1 = {"a": 1, "b": 2, "c": 3}
    dict2 = {"a": 1, "b": 2, "c": 4}
    diff = dict_diff(dict1, dict2)
    assert diff == {"c": 4}
