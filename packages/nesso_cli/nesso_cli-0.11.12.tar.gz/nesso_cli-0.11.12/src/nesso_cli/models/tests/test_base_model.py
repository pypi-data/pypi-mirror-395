import copy
import shutil
from pathlib import Path

import nesso_cli.models.context as context
import pytest
from conftest import TestData
from nesso_cli.models.base_model import check_if_base_model_exists
from nesso_cli.models.common import check_if_relation_exists
from nesso_cli.models.config import config, yaml
from nesso_cli.models.main import app
from typer.testing import CliRunner

PROJECT_DIR = Path(__file__).parent.joinpath("dbt_projects", "postgres")
context.set("PROJECT_DIR", PROJECT_DIR)
BASE_MODELS_DIR_PATH = PROJECT_DIR / "models" / config.silver_schema
BASE_MODEL_NAME_WITHOUT_PREFIX = "test_table_account"
BASE_MODEL_NAME_PREFIXED = "int_test_table_account"

runner = CliRunner()


def test_check_if_base_model_exists(TEST_TABLE_CONTACT_BASE_MODEL):
    # Assumptions.
    assert not check_if_base_model_exists(TEST_TABLE_CONTACT_BASE_MODEL)

    # Create the base model.
    base_model_dir_path = BASE_MODELS_DIR_PATH / TEST_TABLE_CONTACT_BASE_MODEL
    base_model_dir_path.mkdir(parents=True, exist_ok=True)

    base_model_sql_path = base_model_dir_path / f"{TEST_TABLE_CONTACT_BASE_MODEL}.sql"
    base_model_sql_path.touch()

    base_model_yaml_path = base_model_dir_path / f"{TEST_TABLE_CONTACT_BASE_MODEL}.yml"
    base_model_yaml_path.touch()

    # Test.
    assert check_if_base_model_exists(TEST_TABLE_CONTACT_BASE_MODEL)

    # Cleanup.
    shutil.rmtree(base_model_dir_path, ignore_errors=True)


def test_base_model_rm(
    setup_base_model,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    assert setup_base_model.exists()

    runner.invoke(app, ["base_model", "rm", TEST_TABLE_ACCOUNT_BASE_MODEL])

    assert not setup_base_model.exists()


def test_base_model_rm_drop_relation(
    setup_base_model,
    TEST_SCHEMA,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    """Test removing a base model together with dropping its relation."""
    # Assumptions.
    assert setup_base_model.exists()

    # Remove the YAML & drop the relation.
    result = runner.invoke(
        app, ["base_model", "rm", TEST_TABLE_ACCOUNT_BASE_MODEL, "--relation"]
    )

    # Validate it worked.
    assert result.exit_code == 0
    assert not check_if_relation_exists(
        schema=TEST_SCHEMA, name=TEST_TABLE_ACCOUNT_BASE_MODEL
    )


@pytest.mark.parametrize(
    "base_model_name", [BASE_MODEL_NAME_WITHOUT_PREFIX, BASE_MODEL_NAME_PREFIXED]
)
def test_base_model_bootstrap(base_model_name):
    """
    Note that we specify intermediate schema prefix in the test config. Due to
    this, even when we pass `BASE_MODEL_NAME_WITHOUT_PREFIX` as the name of the model
    to `base_model bootstrap`, the directory and file name will be prefixed.
    """
    # Assumptions.
    assert not check_if_base_model_exists(base_model_name)

    base_model_dir_path = BASE_MODELS_DIR_PATH / BASE_MODEL_NAME_PREFIXED
    base_model_sql_path = base_model_dir_path / f"{BASE_MODEL_NAME_PREFIXED}.sql"

    result = runner.invoke(
        app,
        [
            "base_model",
            "bootstrap",
            base_model_name,
        ],
    )

    assert result.exit_code == 0
    assert base_model_sql_path.exists()

    # Cleanup.
    shutil.rmtree(base_model_dir_path, ignore_errors=True)


@pytest.mark.parametrize(
    "base_model_name", [BASE_MODEL_NAME_WITHOUT_PREFIX, BASE_MODEL_NAME_PREFIXED]
)
def test_base_model_bootstrap_custom_silver_schema(base_model_name):
    """
    Note that we specify intermediate schema prefix in the test config. Due to
    this, even though we pass `BASE_MODEL_NAME_WITHOUT_PREFIX` as the name of the model
    to `base_model bootstrap`, the directory and file name will be prefixed.
    """
    # Assumptions.
    assert not check_if_base_model_exists(base_model_name)

    custom_silver_schema = "custom_silver_schema"
    base_model_dir_path = (
        PROJECT_DIR / "models" / custom_silver_schema / BASE_MODEL_NAME_PREFIXED
    )
    base_model_sql_path = base_model_dir_path / f"{BASE_MODEL_NAME_PREFIXED}.sql"

    result = runner.invoke(
        app,
        [
            "base_model",
            "bootstrap",
            base_model_name,
            "--silver-schema",
            custom_silver_schema,
        ],
    )

    assert result.exit_code == 0
    assert base_model_sql_path.exists()

    # Cleanup.
    shutil.rmtree(base_model_dir_path, ignore_errors=True)


@pytest.mark.parametrize(
    "base_model_name", [BASE_MODEL_NAME_WITHOUT_PREFIX, BASE_MODEL_NAME_PREFIXED]
)
def test_base_model_bootstrap_yaml(
    base_model_name,
    setup_base_model,
):
    # Delete base model YAML file created by the `setup_base_model` fixture.
    setup_base_model.unlink()

    # Assumptions.
    assert not setup_base_model.exists()

    # Test.
    result = runner.invoke(
        app,
        [
            "base_model",
            "bootstrap-yaml",
            base_model_name,
        ],
    )

    with open(setup_base_model) as f:
        schema = yaml.load(f)

    assert result.exit_code == 0
    assert check_if_base_model_exists(BASE_MODEL_NAME_PREFIXED)

    assert schema == TestData.base_model_props_no_overrides

    with open(setup_base_model) as f:
        yaml_str = f.read()

    # Check that comments are included in the YAML file.
    assert "# tests:" in yaml_str


def test_base_model_bootstrap_yaml_no_prefix(
    setup_source,
    TEST_SOURCE,
    postgres_connection,
    TEST_SCHEMA,
    TEST_TABLE_ACCOUNT,
):
    # Assumptions.
    assert not check_if_base_model_exists(TEST_TABLE_ACCOUNT)

    # Create and materialize the base model.
    config.silver_schema_prefix = ""

    base_model_dir_path = BASE_MODELS_DIR_PATH / TEST_TABLE_ACCOUNT
    base_model_sql_path = base_model_dir_path / f"{TEST_TABLE_ACCOUNT}.sql"
    base_model_sql_path.parent.mkdir(parents=True, exist_ok=True)
    base_model_sql_path.touch()

    table_fqn = f"{TEST_SOURCE}.{TEST_TABLE_ACCOUNT}"
    view_fqn = f"{TEST_SCHEMA}.{TEST_TABLE_ACCOUNT}"
    postgres_connection.execute(f"CREATE SCHEMA IF NOT EXISTS {TEST_SCHEMA};")
    postgres_connection.execute(
        f"CREATE OR REPLACE VIEW {view_fqn} AS SELECT * FROM {table_fqn};"
    )

    base_model_yaml_path = base_model_dir_path / f"{TEST_TABLE_ACCOUNT}.yml"
    with open(base_model_sql_path, "w") as f:
        f.write(
            f"select * from {{{{ source('{TEST_SOURCE}', '{TEST_TABLE_ACCOUNT}') }}}}"
        )

    result = runner.invoke(
        app,
        [
            "base_model",
            "bootstrap-yaml",
            TEST_TABLE_ACCOUNT,
        ],
    )

    with open(base_model_yaml_path) as f:
        schema = yaml.load(f)

    # Manually adjust the name as the test base model has the default, prefixed name.
    expected_schema = copy.deepcopy(TestData.base_model_props_no_overrides)
    expected_schema["models"][0]["name"] = "test_table_account"

    config.silver_schema_prefix = "int"

    assert result.exit_code == 0
    assert check_if_base_model_exists(TEST_TABLE_ACCOUNT)
    assert schema == expected_schema

    with open(base_model_yaml_path) as f:
        yaml_str = f.read()

    # Check that comments are included in the YAML file.
    assert "# tests:" in yaml_str

    # Cleanup.
    postgres_connection.execute(f"DROP VIEW IF EXISTS {view_fqn};")
    shutil.rmtree(base_model_dir_path, ignore_errors=True)


def test_base_model_bootstrap_yaml_selected_columns(
    setup_source,
    postgres_connection,
    TEST_SCHEMA,
    TEST_SOURCE,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Assumptions.
    assert not check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    # Create and materialize the base model.
    base_model_dir_path = BASE_MODELS_DIR_PATH / TEST_TABLE_ACCOUNT_BASE_MODEL
    base_model_sql_path = base_model_dir_path / f"{TEST_TABLE_ACCOUNT_BASE_MODEL}.sql"
    base_model_sql_path.parent.mkdir(parents=True, exist_ok=True)
    base_model_sql_path.touch()

    table_fqn = f"{TEST_SOURCE}.{TEST_TABLE_ACCOUNT}"
    view_fqn = f"{TEST_SCHEMA}.{TEST_TABLE_ACCOUNT_BASE_MODEL}"
    postgres_connection.execute(f"CREATE SCHEMA IF NOT EXISTS {TEST_SCHEMA};")
    postgres_connection.execute(
        f"""CREATE OR REPLACE VIEW {view_fqn} AS
        SELECT id, name, 'test_value'::text AS test_column FROM {table_fqn};"""
    )
    with open(base_model_sql_path, "w") as f:
        f.write(
            f"""select id, name, 'test_value' AS test_column
from {{{{ source('{TEST_SOURCE}', '{TEST_TABLE_ACCOUNT}') }}}}"""
        )

    result = runner.invoke(
        app,
        [
            "base_model",
            "bootstrap-yaml",
            TEST_TABLE_ACCOUNT,
        ],
    )

    base_model_yaml_path = base_model_dir_path / f"{TEST_TABLE_ACCOUNT_BASE_MODEL}.yml"
    with open(base_model_yaml_path) as f:
        schema = yaml.load(f)

    # Manually apply changes to a copy of the test base model to reflect the custom
    # schema expected in this test case.
    expected_schema = copy.deepcopy(TestData.base_model_props_no_overrides)
    del expected_schema["models"][0]["columns"][2:]
    expected_schema["models"][0]["name"] = TEST_TABLE_ACCOUNT_BASE_MODEL
    expected_schema["models"][0]["columns"].append(
        {
            "name": "test_column",
            "data_type": "TEXT",
            "description": "",
            "quote": True,
            "tags": [],
        }
    )

    assert result.exit_code == 0
    assert check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)
    assert schema == expected_schema

    with open(base_model_yaml_path) as f:
        yaml_str = f.read()

    # Check that comments are included in the YAML file.
    assert "# tests:" in yaml_str

    # Cleanup.
    postgres_connection.execute(f"DROP VIEW IF EXISTS {view_fqn};")
    shutil.rmtree(base_model_dir_path, ignore_errors=True)


def test_base_model_bootstrap_yaml_provide_meta_as_options(
    setup_base_model,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Delete base model YAML file created by the `setup_base_model` fixture.
    setup_base_model.unlink()

    # Assumptions.
    assert not setup_base_model.exists()

    # Test.
    result = runner.invoke(
        app,
        [
            "base_model",
            "bootstrap-yaml",
            TEST_TABLE_ACCOUNT,
            "--domains",
            '["base_model_domain"]',
        ],
    )

    with open(setup_base_model) as f:
        schema = yaml.load(f)

    assert schema == TestData.base_model_props_without_tests
    assert result.exit_code == 0
    assert check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    with open(setup_base_model) as f:
        yaml_str = f.read()

    # Check that comments are included in the YAML file.
    assert "# tests:" in yaml_str


@pytest.mark.parametrize(
    "base_model_name", [BASE_MODEL_NAME_WITHOUT_PREFIX, BASE_MODEL_NAME_PREFIXED]
)
@pytest.mark.parametrize(
    "setup_base_model",
    [
        (
            {
                "model_props": TestData.base_model_props,
                "silver_schema": "custom_silver_schema",
            }
        )
    ],
    indirect=True,
)
def test_base_model_bootstrap_yaml_custom_silver_schema(
    base_model_name,
    setup_base_model,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Delete base model YAML file created by the `setup_base_model` fixture.
    setup_base_model.unlink()

    # Assumptions.
    assert not setup_base_model.exists()

    # Test.
    result = runner.invoke(
        app,
        [
            "base_model",
            "bootstrap-yaml",
            base_model_name,
            "--silver-schema",
            "custom_silver_schema",
        ],
    )

    with open(setup_base_model) as f:
        schema = yaml.load(f)

    base_model_dir = (
        BASE_MODELS_DIR_PATH.parent
        / "custom_silver_schema"
        / TEST_TABLE_ACCOUNT_BASE_MODEL
    )

    assert result.exit_code == 0
    assert check_if_base_model_exists(
        TEST_TABLE_ACCOUNT_BASE_MODEL, base_model_dir=base_model_dir
    )
    assert schema == TestData.base_model_props_no_overrides

    with open(setup_base_model) as f:
        yaml_str = f.read()

    # Check that comments are included in the YAML file.
    assert "# tests:" in yaml_str
