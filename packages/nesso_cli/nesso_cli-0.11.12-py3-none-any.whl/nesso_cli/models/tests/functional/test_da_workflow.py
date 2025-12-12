import shutil
from pathlib import Path

import nesso_cli.models.context as context
import pytest
from nesso_cli.models.base_model import check_if_base_model_exists
from nesso_cli.models.common import call_shell
from nesso_cli.models.config import config, yaml
from nesso_cli.models.main import app
from nesso_cli.models.seed import check_if_seed_exists
from nesso_cli.models.source import check_if_source_exists, check_if_source_table_exists
from nesso_cli.models.tests.test_source import create_empty_source
from typer.testing import CliRunner

runner = CliRunner()

PROJECT_DIR = Path(__file__).parent.parent.joinpath("dbt_projects", "postgres")
context.set("PROJECT_DIR", PROJECT_DIR)
TEST_SEED_COUNTRIES_NAME = "countries_example"


@pytest.fixture(scope="function")
def create_seed(postgres_connection):
    # Create seed
    SEED_SCHEMA_PATH = PROJECT_DIR.joinpath("seeds", "schema.yml")
    result = runner.invoke(
        app,
        [
            "seed",
            "register",
            TEST_SEED_COUNTRIES_NAME,
            "--yaml-path",
            SEED_SCHEMA_PATH,  # type: ignore
            "--technical-owner",
            "test_technical_owner",
            "--business-owner",
            "test_business_owner",
        ],
    )
    assert result.exit_code == 0

    # Check if the schema file was created.
    assert SEED_SCHEMA_PATH.exists()

    # Check if the seed was materialized.
    seed_table_query = f"""SELECT FROM information_schema.tables
    WHERE table_name='{TEST_SEED_COUNTRIES_NAME}'"""
    exists_query = f"SELECT EXISTS ({seed_table_query});"
    is_materialized = postgres_connection.execute(exists_query).fetchone()[0]
    assert is_materialized

    # Check if the seed was added to the schema file.
    assert check_if_seed_exists(TEST_SEED_COUNTRIES_NAME, schema_path=SEED_SCHEMA_PATH)

    yield

    # Cleanup.
    SEED_SCHEMA_PATH.unlink()
    postgres_connection.execute(f"DROP TABLE IF EXISTS {TEST_SEED_COUNTRIES_NAME};")


@pytest.fixture(scope="function")
def create_source(
    postgres_connection,
    TEST_SOURCE,
    TEST_SCHEMA,
    SOURCE_SCHEMA_PATH,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Assumptions.
    assert not check_if_source_exists(TEST_SOURCE)
    assert not check_if_source_table_exists(TEST_SOURCE, TEST_TABLE_ACCOUNT)
    assert not check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

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

    yield

    # Cleanup.
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", "sources", TEST_SOURCE),
        ignore_errors=True,
    )


@pytest.fixture(scope="function")
def create_base_model(
    TEST_SCHEMA,
    TEST_SOURCE,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
    postgres_connection,
):
    base_model_path = (
        PROJECT_DIR / "models" / config.silver_schema / TEST_TABLE_ACCOUNT_BASE_MODEL
    )
    base_model_file_sql = base_model_path / f"{TEST_TABLE_ACCOUNT_BASE_MODEL}.sql"
    base_model_path.mkdir(parents=True, exist_ok=True)
    with open(base_model_file_sql, "w") as f:
        f.write(
            f"select * from {{{{ source('{TEST_SOURCE}', '{TEST_TABLE_ACCOUNT}') }}}}"
        )
    # Bootstrap YAML for the model.
    result = runner.invoke(
        app,
        [
            "base_model",
            "bootstrap-yaml",
            TEST_TABLE_ACCOUNT,
        ],
    )
    assert result.exit_code == 0
    assert check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    yield

    # Cleanup.
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", config.silver_schema),
        ignore_errors=False,
    )
    postgres_connection.execute(
        f"DROP VIEW {TEST_SCHEMA}.{TEST_TABLE_ACCOUNT_BASE_MODEL} CASCADE"
    )


@pytest.fixture(scope="function")
def create_model(
    postgres_connection,
    create_source,
    create_base_model,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Create model SQL.
    MODEL_PATH = PROJECT_DIR.joinpath(
        "models",
        config.gold_layer_name,
        "test_mart",
        "test_project",
        TEST_TABLE_ACCOUNT,
        TEST_TABLE_ACCOUNT + ".sql",
    )
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(MODEL_PATH, "w") as f:
        f.write(f"""SELECT * FROM {{{{ ref("{TEST_TABLE_ACCOUNT_BASE_MODEL}") }}}}""")

    # Bootstrap YAML for the model.
    result = runner.invoke(
        app,
        [
            "model",
            "bootstrap-yaml",
            TEST_TABLE_ACCOUNT,
        ],
    )
    assert result.exit_code == 0

    yield

    # Cleanup.
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", config.gold_layer_name), ignore_errors=True
    )


@pytest.fixture(scope="function")
def create_manifest() -> None:
    """Run dbt commands in a specific order to generate the manifest.json file."""

    manifest_path = PROJECT_DIR.joinpath("target", "manifest.json")
    manifest_path.unlink(missing_ok=True)

    call_shell("dbt clean")
    call_shell("dbt deps")

    # fix https://github.com/dbt-labs/dbt-utils/issues/627
    shutil.rmtree(
        PROJECT_DIR.joinpath(
            "dbt_packages",
            "dbt_utils",
            "tests",
        ),
        ignore_errors=True,
    )

    run_results = call_shell("dbt run")
    test_results = call_shell("dbt test")
    freshness_results = call_shell("dbt source freshness")
    docs_results = call_shell("dbt docs generate")

    assert run_results is not None
    assert test_results is not None
    assert freshness_results is not None
    assert docs_results is not None

    assert manifest_path.exists()

    yield

    # Cleanup.
    manifest_path.unlink()


def test_manifest(
    create_manifest,
    create_seed,
    create_model,
    TEST_SOURCE,
    TEST_SCHEMA,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    """
    This test has 3 stages:
    1. Create resources of each type (seed, source, base model, model).
    2. Run dbt commands in a specific order to generate the manifest.json file.
    3. Inspect that the results for each resource match expectations.
    """

    with open(PROJECT_DIR.joinpath("target", "manifest.json")) as f:
        manifest = yaml.load(f)

    # Tests.
    # Seed.
    seed_metadata = manifest["nodes"][f"seed.postgres.{TEST_SEED_COUNTRIES_NAME}"]
    assert seed_metadata["schema"] == TEST_SCHEMA

    # Source table.
    source_table_fqn = f"{TEST_SOURCE}.{TEST_TABLE_ACCOUNT}"
    source_metadata = manifest["sources"][f"source.postgres.{source_table_fqn}"]
    assert source_metadata["schema"] == TEST_SOURCE

    # Base model.
    base_model_metadata = manifest["nodes"][
        f"model.postgres.{TEST_TABLE_ACCOUNT_BASE_MODEL}"
    ]
    assert base_model_metadata["schema"] == TEST_SCHEMA

    # Model.
    model_metadata = manifest["nodes"][f"model.postgres.{TEST_TABLE_ACCOUNT}"]
    assert model_metadata["schema"] == TEST_SCHEMA
