from pathlib import Path

import nesso_cli.models.context as context
import pytest
from nesso_cli.models.main import app
from nesso_cli.models.models import DBTProperties
from typer.testing import CliRunner

PROJECT_DIR = Path(__file__).parent.joinpath("dbt_projects", "postgres")
context.set("PROJECT_DIR", PROJECT_DIR)

runner = CliRunner()

YAML_SOURCE_COLUMNS = {
    "id": "BIGINT",
    "name": "TEXT",
    "email": "TEXT",
    "mobile": "TEXT",
    "country": "TEXT",
    "_viadot_downloaded_at_utc": "TIMESTAMP WITHOUT TIME ZONE",
}

YAML_SOURCE_COLUMNS_METADATA = {
    "id": {
        "quote": True,
        "data_type": "BIGINT",
        "description": "description_id",
        "tests": ["not_null"],
        "tags": ["uat"],
    },
    "name": {
        "quote": True,
        "data_type": "TEXT",
        "description": "description_name",
        "tests": ["not_null"],
        "tags": ["uat"],
    },
    "email": {
        "quote": True,
        "data_type": "TEXT",
        "description": "description_email",
        "tests": ["unique", "not_null"],
        "tags": ["uat"],
    },
    "mobile": {
        "quote": True,
        "data_type": "TEXT",
        "description": "description_mobile",
        "tags": ["uat"],
    },
    "country": {
        "quote": True,
        "data_type": "TEXT",
        "description": "description_country",
        "tags": ["uat"],
    },
    "_viadot_downloaded_at_utc": {
        "quote": True,
        "data_type": "TIMESTAMP WITHOUT TIME ZONE",
        "description": "description_viadot_downloaded_at_utc",
        "tags": ["uat"],
    },
}


COLUMNS_AFTER_INSERT = {
    "id": {
        "quote": True,
        "data_type": "BIGINT",
        "description": "description_id",
        "tests": ["not_null"],
        "tags": ["uat"],
    },
    "name": {
        "quote": True,
        "data_type": "TEXT",
        "description": "description_name",
        "tests": ["not_null"],
        "tags": ["uat"],
    },
    "email": {
        "quote": True,
        "data_type": "TEXT",
        "description": "description_email",
        "tests": ["unique", "not_null"],
        "tags": ["uat"],
    },
    "mobile": {
        "quote": True,
        "data_type": "TEXT",
        "description": "description_mobile",
        "tags": ["uat"],
    },
    "country": {
        "quote": True,
        "data_type": "TEXT",
        "description": "description_country",
        "tags": ["uat"],
    },
    "_viadot_downloaded_at_utc": {
        "quote": True,
        "data_type": "TIMESTAMP WITHOUT TIME ZONE",
        "description": "description_viadot_downloaded_at_utc",
        "tags": ["uat"],
    },
    "new_column_name": {
        "quote": True,
        "data_type": "CHARACTER VARYING(255)",
        "description": "",
        "tags": [],
    },
}
COLUMNS_AFTER_DELETE = {
    "id": {
        "quote": True,
        "data_type": "BIGINT",
        "description": "description_id",
        "tests": ["not_null"],
        "tags": ["uat"],
    },
    "name": {
        "quote": True,
        "data_type": "TEXT",
        "description": "description_name",
        "tests": ["not_null"],
        "tags": ["uat"],
    },
    "email": {
        "quote": True,
        "data_type": "TEXT",
        "description": "description_email",
        "tests": ["unique", "not_null"],
        "tags": ["uat"],
    },
    "mobile": {
        "quote": True,
        "data_type": "TEXT",
        "description": "description_mobile",
        "tags": ["uat"],
    },
    "country": {
        "quote": True,
        "data_type": "TEXT",
        "description": "description_country",
        "tags": ["uat"],
    },
}

COLUMNS_AFTER_UPDATE = {
    "id": {
        "quote": True,
        "data_type": "BIGINT",
        "description": "description_id",
        "tests": ["not_null"],
        "tags": ["uat"],
    },
    "name": {
        "quote": True,
        "data_type": "TEXT",
        "description": "description_name",
        "tests": ["not_null"],
        "tags": ["uat"],
    },
    "email": {
        "quote": True,
        "data_type": "TEXT",
        "description": "description_email",
        "tests": ["unique", "not_null"],
        "tags": ["uat"],
    },
    "mobile": {
        "quote": True,
        "data_type": "TEXT",
        "description": "description_mobile",
        "tags": ["uat"],
    },
    "new_updated_name": {
        "quote": True,
        "data_type": "TEXT",
        "description": "",
        "tags": [],
    },
    "_viadot_downloaded_at_utc": {
        "quote": True,
        "data_type": "TIMESTAMP WITHOUT TIME ZONE",
        "description": "description_viadot_downloaded_at_utc",
        "tags": ["uat"],
    },
}

COLUMNS_AFTER_UPDATE_DATA_TYPE = {
    "id": {
        "quote": True,
        "data_type": "BIGINT",
        "description": "description_id",
        "tests": ["not_null"],
        "tags": ["uat"],
    },
    "name": {
        "quote": True,
        "data_type": "TEXT",
        "description": "description_name",
        "tests": ["not_null"],
        "tags": ["uat"],
    },
    "email": {
        "quote": True,
        "data_type": "TEXT",
        "description": "description_email",
        "tests": ["unique", "not_null"],
        "tags": ["uat"],
    },
    "mobile": {
        "quote": True,
        "data_type": "CHARACTER VARYING(255)",
        "description": "description_mobile",
        "tags": ["uat"],
    },
    "country": {
        "quote": True,
        "data_type": "TEXT",
        "description": "description_country",
        "tags": ["uat"],
    },
    "_viadot_downloaded_at_utc": {
        "quote": True,
        "data_type": "TIMESTAMP WITHOUT TIME ZONE",
        "description": "description_viadot_downloaded_at_utc",
        "tags": ["uat"],
    },
}

ADD_COLUMN = "ADD COLUMN new_column_name VARCHAR(255)"
DELETE_COLUMN = "DROP COLUMN _viadot_downloaded_at_utc CASCADE"
UPDATE_COLUMN = "RENAME COLUMN country TO new_updated_name"
UPDATE_COLUMN_DATA_TYPE = "ALTER COLUMN mobile TYPE VARCHAR(255);"


@pytest.fixture(params=[ADD_COLUMN])
def setup_models_in_db(
    request,
    postgres_connection,
    TEST_SOURCE,
    TEST_SCHEMA,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
    MODEL,
):
    # Definitions of the source, base model, and model.
    source_fqn = f"{TEST_SOURCE}.{TEST_TABLE_ACCOUNT}"
    base_model_fqn = f"{TEST_SCHEMA}.{TEST_TABLE_ACCOUNT_BASE_MODEL}"
    model_fqn = f"{TEST_SCHEMA}.{MODEL}"

    # Creates tables and views mimicking the source, base model, and model.
    sql_statement = f"""
    CREATE SCHEMA IF NOT EXISTS {TEST_SCHEMA};
    DROP VIEW IF EXISTS {base_model_fqn} CASCADE;
    ALTER TABLE {source_fqn} {request.param};
    CREATE OR REPLACE VIEW {base_model_fqn} AS SELECT * FROM {source_fqn};
    CREATE OR REPLACE VIEW {model_fqn} AS SELECT * FROM {base_model_fqn};
    """
    postgres_connection.execute(sql_statement)

    yield

    # Cleaning.
    drop_sql_statement = f"""
    DROP TABLE IF EXISTS {source_fqn} CASCADE;
    """
    postgres_connection.execute(drop_sql_statement)


def test_update_model_create_new_column(
    setup_model,
    setup_models_in_db,
    MODEL,
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(file_path=setup_model).get_yaml_table_columns(
        MODEL
    )
    assert yaml_columns_metadata != COLUMNS_AFTER_INSERT

    # Test.
    result = runner.invoke(
        app,
        [
            "update",
            "model",
            MODEL,
        ],
    )

    yaml_columns_metadata = DBTProperties(file_path=setup_model).get_yaml_table_columns(
        MODEL
    )

    assert result.exit_code == 0
    assert yaml_columns_metadata == COLUMNS_AFTER_INSERT


@pytest.mark.parametrize("setup_models_in_db", [UPDATE_COLUMN], indirect=True)
def test_update_model_update_column(
    setup_model,
    setup_models_in_db,
    MODEL,
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(file_path=setup_model).get_yaml_table_columns(
        MODEL
    )
    assert yaml_columns_metadata != COLUMNS_AFTER_INSERT

    # Test.
    result = runner.invoke(
        app,
        [
            "update",
            "model",
            MODEL,
        ],
    )

    yaml_columns_metadata = DBTProperties(file_path=setup_model).get_yaml_table_columns(
        MODEL
    )

    assert result.exit_code == 0
    assert yaml_columns_metadata == COLUMNS_AFTER_UPDATE


@pytest.mark.parametrize("setup_models_in_db", [DELETE_COLUMN], indirect=True)
def test_update_model_delete_column(
    setup_model,
    setup_models_in_db,
    MODEL,
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(file_path=setup_model).get_yaml_table_columns(
        MODEL
    )
    assert yaml_columns_metadata != COLUMNS_AFTER_INSERT

    # Test.
    result = runner.invoke(
        app,
        [
            "update",
            "model",
            MODEL,
        ],
    )

    yaml_columns_metadata = DBTProperties(file_path=setup_model).get_yaml_table_columns(
        MODEL
    )

    assert result.exit_code == 0
    assert yaml_columns_metadata == COLUMNS_AFTER_DELETE


@pytest.mark.parametrize("setup_models_in_db", [UPDATE_COLUMN_DATA_TYPE], indirect=True)
def test_update_model_column_data_type(
    setup_model,
    setup_models_in_db,
    MODEL,
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(file_path=setup_model).get_yaml_table_columns(
        MODEL
    )
    assert yaml_columns_metadata != COLUMNS_AFTER_INSERT

    # Test.
    result = runner.invoke(
        app,
        [
            "update",
            "model",
            MODEL,
        ],
    )

    yaml_columns_metadata = DBTProperties(file_path=setup_model).get_yaml_table_columns(
        MODEL
    )

    assert result.exit_code == 0
    assert yaml_columns_metadata == COLUMNS_AFTER_UPDATE_DATA_TYPE


def test_update_base_model_create_new_column(
    setup_base_model,
    setup_models_in_db,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(
        file_path=setup_base_model
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT_BASE_MODEL)
    assert yaml_columns_metadata != COLUMNS_AFTER_INSERT

    # Test.
    result = runner.invoke(
        app,
        [
            "update",
            "base_model",
            TEST_TABLE_ACCOUNT_BASE_MODEL,
        ],
    )

    yaml_columns_metadata = DBTProperties(
        file_path=setup_base_model
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT_BASE_MODEL)

    assert result.exit_code == 0
    assert yaml_columns_metadata == COLUMNS_AFTER_INSERT


@pytest.mark.parametrize("setup_models_in_db", [UPDATE_COLUMN], indirect=True)
def test_update_base_model_update_column(
    setup_base_model,
    setup_models_in_db,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(
        file_path=setup_base_model
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT_BASE_MODEL)
    assert yaml_columns_metadata != COLUMNS_AFTER_UPDATE

    # Test.
    result = runner.invoke(
        app,
        [
            "update",
            "base_model",
            TEST_TABLE_ACCOUNT_BASE_MODEL,
        ],
    )

    yaml_columns_metadata = DBTProperties(
        file_path=setup_base_model
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT_BASE_MODEL)

    assert result.exit_code == 0
    assert yaml_columns_metadata == COLUMNS_AFTER_UPDATE


@pytest.mark.parametrize("setup_models_in_db", [DELETE_COLUMN], indirect=True)
def test_update_base_model_delete_column(
    setup_base_model,
    setup_models_in_db,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(
        file_path=setup_base_model
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT_BASE_MODEL)
    assert yaml_columns_metadata != COLUMNS_AFTER_DELETE

    # Test.
    result = runner.invoke(
        app,
        [
            "update",
            "base_model",
            TEST_TABLE_ACCOUNT_BASE_MODEL,
        ],
    )

    yaml_columns_metadata = DBTProperties(
        file_path=setup_base_model
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT_BASE_MODEL)
    assert result.exit_code == 0
    assert yaml_columns_metadata == COLUMNS_AFTER_DELETE


@pytest.mark.parametrize("setup_models_in_db", [UPDATE_COLUMN_DATA_TYPE], indirect=True)
def test_update_base_model_column_data_type(
    setup_base_model,
    setup_models_in_db,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(
        file_path=setup_base_model
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT_BASE_MODEL)
    assert yaml_columns_metadata != COLUMNS_AFTER_UPDATE_DATA_TYPE

    # Test.
    result = runner.invoke(
        app,
        [
            "update",
            "base_model",
            TEST_TABLE_ACCOUNT_BASE_MODEL,
        ],
    )

    yaml_columns_metadata = DBTProperties(
        file_path=setup_base_model
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT_BASE_MODEL)

    assert result.exit_code == 0
    assert yaml_columns_metadata == COLUMNS_AFTER_UPDATE_DATA_TYPE


def test_update_source_create_new_column(
    setup_source, setup_models_in_db, TEST_TABLE_ACCOUNT
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(
        file_path=setup_source
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT)
    assert yaml_columns_metadata != COLUMNS_AFTER_INSERT

    # Test.
    result = runner.invoke(
        app,
        [
            "update",
            "source",
            TEST_TABLE_ACCOUNT,
        ],
    )

    yaml_columns_metadata = DBTProperties(
        file_path=setup_source
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT)

    assert result.exit_code == 0
    assert yaml_columns_metadata == COLUMNS_AFTER_INSERT


@pytest.mark.parametrize("setup_models_in_db", [UPDATE_COLUMN], indirect=True)
def test_update_source_update_column(
    setup_source, setup_models_in_db, TEST_TABLE_ACCOUNT
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(
        file_path=setup_source
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT)
    assert yaml_columns_metadata != COLUMNS_AFTER_UPDATE

    # Test.
    result = runner.invoke(
        app,
        [
            "update",
            "source",
            TEST_TABLE_ACCOUNT,
        ],
    )

    yaml_columns_metadata = DBTProperties(
        file_path=setup_source
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT)

    assert result.exit_code == 0
    assert yaml_columns_metadata == COLUMNS_AFTER_UPDATE


@pytest.mark.parametrize("setup_models_in_db", [DELETE_COLUMN], indirect=True)
def test_update_source_delete_column(
    setup_source,
    setup_models_in_db,
    TEST_SOURCE,
    TEST_TABLE_ACCOUNT,
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(
        file_path=setup_source
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT)
    assert yaml_columns_metadata != COLUMNS_AFTER_DELETE

    # Test.
    result = runner.invoke(
        app,
        [
            "update",
            "source",
            TEST_TABLE_ACCOUNT,
            "-s",
            TEST_SOURCE,
        ],
    )

    yaml_columns_metadata = DBTProperties(
        file_path=setup_source
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT)

    assert result.exit_code == 0
    assert yaml_columns_metadata == COLUMNS_AFTER_DELETE


@pytest.mark.parametrize("setup_models_in_db", [UPDATE_COLUMN_DATA_TYPE], indirect=True)
def test_update_source_update_column_data_type(
    setup_source, setup_models_in_db, TEST_SOURCE, TEST_TABLE_ACCOUNT
):
    # Assumptions.
    yaml_columns_metadata = DBTProperties(
        file_path=setup_source
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT)
    assert yaml_columns_metadata != COLUMNS_AFTER_UPDATE_DATA_TYPE

    # Test.
    result = runner.invoke(
        app,
        [
            "update",
            "source",
            TEST_TABLE_ACCOUNT,
            "-s",
            TEST_SOURCE,
        ],
    )

    yaml_columns_metadata = DBTProperties(
        file_path=setup_source
    ).get_yaml_table_columns(TEST_TABLE_ACCOUNT)

    assert result.exit_code == 0
    assert yaml_columns_metadata == COLUMNS_AFTER_UPDATE_DATA_TYPE
