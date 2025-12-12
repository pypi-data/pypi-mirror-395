import shutil
from pathlib import Path

import nesso_cli.models.context as context
from conftest import TestData
from nesso_cli.models.base_model import check_if_base_model_exists
from nesso_cli.models.common import call_shell, check_if_relation_exists
from nesso_cli.models.config import config, yaml
from nesso_cli.models.main import app
from nesso_cli.models.source import check_if_source_exists, check_if_source_table_exists
from typer.testing import CliRunner

PROJECT_DIR = Path(__file__).parent.joinpath("dbt_projects", "postgres")
context.set("PROJECT_DIR", PROJECT_DIR)

runner = CliRunner()


def test_check_if_source_exists(SOURCE_SCHEMA_PATH, TEST_SOURCE):
    assert not check_if_source_exists(TEST_SOURCE)

    SOURCE_SCHEMA_PATH.touch()

    assert check_if_source_exists(TEST_SOURCE)


def test_check_if_source_table_exists(
    SOURCE_SCHEMA_PATH, TEST_SOURCE, TEST_TABLE_CONTACT
):
    assert not check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_CONTACT)

    source_yaml = {
        "version": 2,
        "sources": [{"name": TEST_SOURCE, "tables": [{"name": TEST_TABLE_CONTACT}]}],
    }
    with open(SOURCE_SCHEMA_PATH, "w") as f:
        yaml.dump(source_yaml, f)

    assert check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_CONTACT)


def test_check_if_source_table_exists_substring(
    SOURCE_SCHEMA_PATH, TEST_SOURCE, TEST_TABLE_CONTACT
):
    assert not check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_CONTACT)

    source_yaml = {
        "version": 2,
        "sources": [
            {"name": TEST_SOURCE, "tables": [{"name": TEST_TABLE_CONTACT + "abc"}]}
        ],
    }
    with open(SOURCE_SCHEMA_PATH, "w") as f:
        yaml.dump(source_yaml, f)

    assert not check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_CONTACT)


def test_create(
    TEST_SOURCE,
    TEST_TABLE_CONTACT,
    TEST_TABLE_ACCOUNT,
):
    assert not check_if_source_exists(TEST_SOURCE)

    # Create a new source.
    result = runner.invoke(
        app,
        [
            "source",
            "create",
            TEST_SOURCE,
            "-p",
            PROJECT_DIR.name,
        ],
        input="\n\n",
    )

    assert result.exit_code == 0
    assert check_if_source_exists(TEST_SOURCE)
    assert check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_CONTACT)
    assert check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_ACCOUNT)

    # Cleanup
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", "sources", TEST_SOURCE),
        ignore_errors=False,
    )


def test_add_first_source(
    SOURCE_SCHEMA_PATH,
    TEST_SOURCE,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    """Verify adding the first source table works."""
    assert not check_if_source_exists(TEST_SOURCE)
    assert not check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_ACCOUNT)
    assert not check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    create_empty_source(TEST_SOURCE, SOURCE_SCHEMA_PATH)

    result = runner.invoke(
        app,
        [
            "source",
            "add",
            TEST_TABLE_ACCOUNT,
            "-p",
            PROJECT_DIR.name,
            "--non-interactive",
        ],
    )
    assert result.exit_code == 0
    assert check_if_source_exists(TEST_SOURCE)
    assert check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_ACCOUNT)

    expected_schema = TestData.source_props_no_overrides

    # This is required since until https://github.com/dyvenia/nesso-cli/issues/261 is
    # implemented, the `source add` command does not use the metadata config defined in
    # nesso config. So we need to manually remove extra keys specified in the test
    # config file.
    keys_to_remove = ("test_meta_key", "test_meta_key2", "test_meta_key3")
    for key in keys_to_remove:
        expected_schema["sources"][0]["tables"][0]["meta"].pop(key)

    # Applying changes to a copy of the object to reflect
    # the expected data changes after the test.
    expected_schema["sources"][0]["tables"][0][
        "description"
    ] = f"""{{{{ doc("{config.bronze_schema}_{TEST_TABLE_ACCOUNT}") }}}}"""

    with open(SOURCE_SCHEMA_PATH) as f:
        schema = yaml.load(f)

    assert schema == expected_schema

    # Check that comments are included in the schema file.
    with open(SOURCE_SCHEMA_PATH) as f:
        yaml_str = f.read()
    assert "# - unique" in yaml_str

    # Cleanup.
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", "sources", TEST_SOURCE),
        ignore_errors=True,
    )


def test_add_second_source(
    SOURCE_SCHEMA_PATH,
    TEST_SOURCE,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_CONTACT,
):
    """Verify that adding further source tables also works."""
    assert not check_if_source_exists(TEST_SOURCE)
    assert not check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_ACCOUNT)

    create_empty_source(TEST_SOURCE, SOURCE_SCHEMA_PATH)

    # Add the first table.
    result1 = runner.invoke(
        app,
        [
            "source",
            "add",
            TEST_TABLE_ACCOUNT,
            "-p",
            PROJECT_DIR.name,
        ],
        input="\n\n",
    )

    # Add another table.
    result2 = runner.invoke(
        app,
        [
            "source",
            "add",
            TEST_TABLE_CONTACT,
            "-p",
            PROJECT_DIR.name,
        ],
        input="\n\n",
    )
    assert result1.exit_code == 0
    assert result2.exit_code == 0
    assert check_if_source_exists(TEST_SOURCE)
    assert check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_ACCOUNT)
    assert check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_CONTACT)

    # Cleanup.
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", "sources", TEST_SOURCE),
        ignore_errors=True,
    )


def create_empty_source(source_name: str, schema_path: Path) -> None:
    # Add an empty source schema.
    empty_source_yaml = {
        "version": 2,
        "sources": [{"name": source_name, "schema": source_name}],
    }

    with open(schema_path, "w") as f:
        yaml.dump(empty_source_yaml, f)


def test_add_creates_dbt_metadata(
    SOURCE_SCHEMA_PATH,
    TEST_SOURCE,
    TEST_TABLE_ACCOUNT,
):
    """
    Verify that running `add()` generates correct metadata in dbt's manifest.json.

    We execute source add and then verify the metadata for the source table.
    """
    assert not check_if_source_exists(TEST_SOURCE)
    assert not check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_ACCOUNT)

    create_empty_source(TEST_SOURCE, SOURCE_SCHEMA_PATH)

    assert check_if_source_exists(TEST_SOURCE)

    # Add a table with a base model.
    runner.invoke(
        app,
        [
            "source",
            "add",
            TEST_TABLE_ACCOUNT,
            "-p",
            PROJECT_DIR.name,
        ],
        input="\n\n",
    )

    assert check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_ACCOUNT)

    # Update manifest.json
    compile_result = call_shell("dbt compile")
    assert compile_result is not None

    with open(PROJECT_DIR.joinpath("target", "manifest.json")) as f:
        manifest = yaml.load(f)

    fqn = f"{TEST_SOURCE}.{TEST_TABLE_ACCOUNT}"
    source_metadata = manifest["sources"][f"source.postgres.{fqn}"]
    assert source_metadata["schema"] == TEST_SOURCE

    # Cleanup.
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", "sources", TEST_SOURCE),
        ignore_errors=True,
    )


def test_add_nonexistent_table(TEST_SOURCE):
    result = runner.invoke(
        app,
        [
            "source",
            "add",
            "nonexistent_table",
            "-p",
            PROJECT_DIR.name,
        ],
        input="\n\n",
    )
    assert result.exception
    assert isinstance(result.exception, ValueError) is True

    assert not check_if_source_exists(TEST_SOURCE)
    assert not check_if_source_table_exists(TEST_SOURCE, "nonexistent_table")


def test_add_with_specified_env(
    SOURCE_SCHEMA_PATH,
    TEST_SOURCE,
    TEST_TABLE_ACCOUNT,
):
    assert not check_if_source_exists(TEST_SOURCE)
    assert not check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_ACCOUNT)

    # Create a source without any source tables.
    create_empty_source(TEST_SOURCE, SOURCE_SCHEMA_PATH)

    result = runner.invoke(
        app,
        [
            "source",
            "add",
            TEST_TABLE_ACCOUNT,
            "-p",
            PROJECT_DIR.name,
            "-e",
            "prod",
        ],
        input="\n\n",
    )
    assert result.exit_code == 0
    assert check_if_source_exists(TEST_SOURCE)
    assert check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_ACCOUNT)

    # Cleanup.
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", "sources", TEST_SOURCE),
        ignore_errors=True,
    )


def test_freshness(TEST_SOURCE, SOURCE_SCHEMA_PATH, TEST_TABLE_ACCOUNT):
    # Create a test source table.
    table_yaml = {
        "name": TEST_TABLE_ACCOUNT,
        "loaded_at_field": "_viadot_downloaded_at_utc::timestamp",
        "freshness": {
            "warn_after": {"count": 24, "period": "hour"},
            "error_after": {"count": 48, "period": "hour"},
        },
    }
    source_yaml = {
        "version": 2,
        "sources": [
            {"name": TEST_SOURCE, "schema": TEST_SOURCE, "tables": [table_yaml]}
        ],
    }

    with open(SOURCE_SCHEMA_PATH, "w") as f:
        yaml.dump(source_yaml, f)

    result = runner.invoke(
        app,
        ["source", "freshness", "-s", TEST_TABLE_ACCOUNT, "-e", "prod"],
        standalone_mode=False,
    )
    assert result.exit_code == 0
    assert "PASS" in result.return_value

    # Cleanup.
    SOURCE_SCHEMA_PATH.unlink()


def test_rm(TEST_TABLE_ACCOUNT, TEST_SOURCE, SOURCE_SCHEMA_PATH):
    # Create a source with a test table.
    source_yaml = {
        "version": 2,
        "sources": [
            {
                "name": TEST_SOURCE,
                "schema": TEST_SOURCE,
                "tables": [{"name": TEST_TABLE_ACCOUNT}],
            }
        ],
    }

    with open(SOURCE_SCHEMA_PATH, "w") as f:
        yaml.dump(source_yaml, f)

    assert check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_ACCOUNT)

    result = runner.invoke(
        app,
        [
            "source",
            "rm",
            TEST_TABLE_ACCOUNT,
        ],
    )
    assert result.exit_code == 0
    assert not check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_ACCOUNT)

    # Cleanup.
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", "sources", TEST_SOURCE),
        ignore_errors=True,
    )


def test_rm_drop_base_table(
    setup_base_model,
    TEST_TABLE_ACCOUNT,
    TEST_SOURCE,
    TEST_SCHEMA,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Assumptions.
    assert setup_base_model.exists()

    # Remove the source table & base model.
    result = runner.invoke(
        app,
        [
            "source",
            "rm",
            TEST_TABLE_ACCOUNT,
            "--remove-base-model",
        ],
    )

    assert result.exit_code == 0
    assert not check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_ACCOUNT)
    assert not check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)
    assert not check_if_relation_exists(
        TEST_TABLE_ACCOUNT_BASE_MODEL, schema=TEST_SCHEMA
    )
