from pathlib import Path

import nesso_cli.models.context as context
import pytest
from nesso_cli.models.common import call_shell
from nesso_cli.models.config import yaml
from nesso_cli.models.main import app
from nesso_cli.models.seed import (
    add_to_schema,
    check_if_schema_exists,
    check_if_seed_exists,
    create_schema,
)
from typer.testing import CliRunner

runner = CliRunner()

PROJECT_DIR = Path(__file__).parent.joinpath("dbt_projects", "postgres")
context.set("PROJECT_DIR", PROJECT_DIR)

TEST_SEED_AVG_NAME = "average_salary_test"
TEST_SEED_COUNTRIES_NAME = "countries_example"
TEST_SEED_PEOPLE_NAME = "people_example"

SEED_SCHEMA_PATH = PROJECT_DIR.joinpath("seeds", "schema.yml")
TEST_SEED_AVG_PATH = SEED_SCHEMA_PATH.parent.joinpath(f"{TEST_SEED_AVG_NAME}.csv")
TEST_SEED_COUNTRIES_PATH = SEED_SCHEMA_PATH.parent.joinpath(
    f"{TEST_SEED_COUNTRIES_NAME}.csv"
)
TEST_SEED_PEOPLE_PATH = SEED_SCHEMA_PATH.parent.joinpath(f"{TEST_SEED_PEOPLE_NAME}.csv")


@pytest.fixture(scope="function")
def seed_schema_yaml():
    assert not SEED_SCHEMA_PATH.exists()

    # Create test seed.
    seed_schema_yaml = {
        "version": 2,
        "seeds": [{"name": TEST_SEED_COUNTRIES_NAME}],
    }
    with open(SEED_SCHEMA_PATH, "w") as f:
        yaml.dump(seed_schema_yaml, f)

    yield

    # Cleanup.
    SEED_SCHEMA_PATH.unlink()


def test_check_if_schema_exists(seed_schema_yaml):
    assert check_if_schema_exists(SEED_SCHEMA_PATH)


def test_check_if_seed_exists(seed_schema_yaml):
    # Assumptions.
    assert TEST_SEED_COUNTRIES_PATH.exists()

    # Validate.
    assert SEED_SCHEMA_PATH.exists()
    assert check_if_seed_exists(TEST_SEED_COUNTRIES_NAME, schema_path=SEED_SCHEMA_PATH)


def test_check_if_seed_exists_returns_false_when_untrue(seed_schema_yaml):
    # Assumptions.
    assert TEST_SEED_COUNTRIES_PATH.exists()

    # Create test seed.
    seed_schema_yaml = {
        "version": 2,
        "seeds": [{"name": "some_other_seed"}],
    }
    with open(SEED_SCHEMA_PATH, "w") as f:
        yaml.dump(seed_schema_yaml, f)

    # Validate.
    assert not check_if_seed_exists(
        TEST_SEED_COUNTRIES_NAME, schema_path=SEED_SCHEMA_PATH
    )


def test_check_if_seed_exists_handles_empty_schema():
    # Assumptions.
    assert TEST_SEED_COUNTRIES_PATH.exists()
    assert not SEED_SCHEMA_PATH.exists()

    # Create test seed.
    seed_schema_yaml = {
        "version": 2,
        "seeds": [],
    }
    with open(SEED_SCHEMA_PATH, "w") as f:
        yaml.dump(seed_schema_yaml, f)

    exists = check_if_seed_exists(
        TEST_SEED_COUNTRIES_NAME, schema_path=SEED_SCHEMA_PATH
    )

    # Validate.
    assert exists is False

    # Cleanup.
    SEED_SCHEMA_PATH.unlink()


def test_check_if_seed_exists_reads_seed_schema_path():
    fake_schema_path = Path("fake_schema.yml")

    # Assumptions.
    assert TEST_SEED_COUNTRIES_PATH.exists()
    assert not fake_schema_path.exists()

    # Only one seed should be present.
    exists = check_if_seed_exists(
        TEST_SEED_COUNTRIES_NAME, schema_path=fake_schema_path
    )

    assert exists is False

    # Create test seed.
    seed_schema_yaml = {
        "version": 2,
        "seeds": [{"name": TEST_SEED_COUNTRIES_NAME}],
    }
    with open(fake_schema_path, "w") as f:
        yaml.dump(seed_schema_yaml, f)

    # Validate.
    assert check_if_seed_exists(TEST_SEED_COUNTRIES_NAME, schema_path=fake_schema_path)

    # Cleanup.
    fake_schema_path.unlink()


def test_create_schema():
    # Assumptions.
    assert not SEED_SCHEMA_PATH.exists()

    create_schema(SEED_SCHEMA_PATH)

    # Validate.
    assert SEED_SCHEMA_PATH.exists()

    with open(SEED_SCHEMA_PATH) as f:
        schema = yaml.load(f)
    assert "version" in schema
    assert "seeds" in schema

    # Cleanup.
    SEED_SCHEMA_PATH.unlink()


def test_add_to_schema():
    # Assumptions.
    assert not SEED_SCHEMA_PATH.exists()

    # Preconditions.
    create_schema(SEED_SCHEMA_PATH)
    assert SEED_SCHEMA_PATH.exists()

    # Validate
    add_to_schema(
        TEST_SEED_COUNTRIES_NAME,
        schema_path=SEED_SCHEMA_PATH,
        technical_owner="test_technical_owner",
        business_owner="test_business_owner",
        target="dev",
    )
    assert check_if_seed_exists(TEST_SEED_COUNTRIES_NAME, schema_path=SEED_SCHEMA_PATH)

    # Cleanup.
    SEED_SCHEMA_PATH.unlink()


def test_add_to_schema_duplicate_seed_fails():
    """Verify that adding a seed that already exists fails."""
    # Assumptions.
    assert not SEED_SCHEMA_PATH.exists()

    # Preconditions.
    create_schema(SEED_SCHEMA_PATH)
    assert SEED_SCHEMA_PATH.exists()

    # Validate
    add_to_schema(
        TEST_SEED_COUNTRIES_NAME,
        schema_path=SEED_SCHEMA_PATH,
        technical_owner="test_technical_owner",
        business_owner="test_business_owner",
        target="dev",
    )
    assert check_if_seed_exists(TEST_SEED_COUNTRIES_NAME, schema_path=SEED_SCHEMA_PATH)

    with pytest.raises(ValueError):
        add_to_schema(
            TEST_SEED_COUNTRIES_NAME,
            schema_path=SEED_SCHEMA_PATH,
            technical_owner="test_technical_owner",
            business_owner="test_business_owner",
            target="dev",
        )

    # Cleanup.
    SEED_SCHEMA_PATH.unlink()


def test_register(postgres_connection):
    # Assumptions.
    assert TEST_SEED_COUNTRIES_PATH.exists()
    assert not SEED_SCHEMA_PATH.exists()

    # Register the seed, ie. materialize it and create an entry for it
    # in the seed schema file.
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

    # Check the file structure.
    expected_schema = {
        "version": 2,
        "seeds": [
            {
                "name": "countries_example",
                "description": "",
                "meta": {
                    "owners": [
                        {"type": "Technical owner", "email": "test_technical_owner"},
                        {"type": "Business owner", "email": "test_business_owner"},
                    ],
                },
                "columns": [
                    {
                        "name": "country_code",
                        "description": "",
                        "quote": True,
                    },
                    {
                        "name": "country_name",
                        "description": "",
                        "quote": True,
                    },
                ],
            }
        ],
    }

    with open(SEED_SCHEMA_PATH) as f:
        schema = yaml.load(f)

    assert schema == expected_schema

    # Check that comments are included in the schema file.
    with open(SEED_SCHEMA_PATH) as f:
        yaml_str = f.read()
    assert "# - unique" in yaml_str

    # Cleanup.
    SEED_SCHEMA_PATH.unlink()
    postgres_connection.execute(f"DROP TABLE IF EXISTS {TEST_SEED_COUNTRIES_NAME};")


def test_register_existing_seed_relation_fails(postgres_connection):
    """Verify that registering a seed for a relation that already exists fails."""

    # Assumptions.
    assert not SEED_SCHEMA_PATH.exists()

    # Preconditions.
    create_schema(SEED_SCHEMA_PATH)
    assert SEED_SCHEMA_PATH.exists()

    # Create the seed relation.
    call_shell(f"dbt seed -s {TEST_SEED_COUNTRIES_NAME}")

    # Validate
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

    assert result.exit_code == 1
    assert isinstance(result.exception, ValueError)

    assert not check_if_seed_exists(
        TEST_SEED_COUNTRIES_NAME, schema_path=SEED_SCHEMA_PATH
    )

    # Cleanup.
    SEED_SCHEMA_PATH.unlink()
    postgres_connection.execute(f"DROP TABLE IF EXISTS {TEST_SEED_COUNTRIES_NAME};")
