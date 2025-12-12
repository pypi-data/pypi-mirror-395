import copy
import os
import random
import shutil
from datetime import datetime
from enum import Enum
from functools import cached_property
from pathlib import Path

import pandas as pd
import pytest
from dotenv import load_dotenv
from faker import Faker
from nesso_cli.models.config import config, yaml
from nesso_cli.models.models import (
    ColumnMeta,
    Model,
    ModelProperties,
    Source,
    SourceProperties,
    SourceTable,
)
from nesso_cli.models.resources import NessoDBTModel
from nesso_cli.models.tests.test_init import (
    TEST_EXAMPLE_PROFILES_PATH,
    TEST_PROJECT_FILE,
    TEST_PROJECT_PATH,
    TEST_TEMPLATE_FILE,
    TEST_TEMPLATE_FILE_TEMPLATED_FILENAME,
)
from nesso_cli.models.tests.test_seed import SEED_SCHEMA_PATH
from pydantic import BaseModel, Field
from sqlalchemy import create_engine

load_dotenv()

fake = Faker()

POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
PROJECT_DIR = Path(__file__).parent.joinpath("dbt_projects", "postgres")

test_tables_nrows = 100
meta_fields_config = config.metadata["fields"]


@pytest.fixture(scope="session")
def MART():
    yield "test_mart"


@pytest.fixture(scope="session")
def MODEL():
    yield "test_model"


@pytest.fixture(scope="session")
def PROJECT():
    yield "test_project"


@pytest.fixture(scope="session")
def MODEL_BASE_DIR(MART, MODEL):
    yield PROJECT_DIR / "models" / config.gold_layer_name / MART / MODEL


@pytest.fixture(scope="session")
def MODEL_PATH(MODEL_BASE_DIR, MODEL):
    yield MODEL_BASE_DIR.joinpath(MODEL + ".sql")


@pytest.fixture(scope="session")
def MODEL_YAML_PATH(MODEL_BASE_DIR, MODEL):
    yield MODEL_BASE_DIR.joinpath(MODEL + ".yml")


@pytest.fixture(scope="session")
def BASE_MODEL_YAML_PATH(TEST_TABLE_ACCOUNT_BASE_MODEL):
    base_model_path = (
        PROJECT_DIR / "models" / config.silver_schema / TEST_TABLE_ACCOUNT_BASE_MODEL
    )
    yield base_model_path / f"{TEST_TABLE_ACCOUNT_BASE_MODEL}.yml"


@pytest.fixture(scope="session")
def TEST_SOURCE():
    yield config.bronze_schema


@pytest.fixture(scope="function")
def SOURCE_SCHEMA_PATH(TEST_SOURCE):
    schema_file_name = TEST_SOURCE + ".yml"
    schema_path = PROJECT_DIR / "models" / "sources" / TEST_SOURCE / schema_file_name
    schema_path.parent.mkdir(parents=True, exist_ok=True)

    yield schema_path

    shutil.rmtree(schema_path.parent, ignore_errors=True)


@pytest.fixture(scope="session")
def TEST_TABLE_CONTACT():
    yield "test_table_contact"


@pytest.fixture(scope="session")
def TEST_TABLE_ACCOUNT():
    yield "test_table_account"


@pytest.fixture(scope="session")
def TEST_TABLE_CONTACT_BASE_MODEL():
    prefix = config.silver_schema_prefix
    table_name = "test_table_contact"
    yield f"{prefix}_{table_name}" if prefix else table_name


@pytest.fixture(scope="session")
def TEST_TABLE_ACCOUNT_BASE_MODEL():
    prefix = config.silver_schema_prefix
    table_name = "test_table_account"
    yield f"{prefix}_{table_name}" if prefix else table_name


@pytest.fixture(scope="session")
def TEST_SCHEMA():
    yield "test_schema"


class Name(Enum):
    ID = "id"
    NAME = "name"
    EMAIL = "email"
    MOBILE = "mobile"
    COUNTRY = "country"
    DOWNLOADED_AT_UTC = "_viadot_downloaded_at_utc"


class DataType(Enum):
    BIGINT = "BIGINT"
    TIMESTAMP = "TIMESTAMP WITHOUT TIME ZONE"
    TEXT = "TEXT"


class Description(Enum):
    ID = "description_id"
    NAME = "description_name"
    EMAIL = "description_email"
    MOBILE = "description_mobile"
    COUNTRY = "description_country"
    DOWNLOADED_AT_UTC = "description_viadot_downloaded_at_utc"


class Test(Enum):
    NOT_NULL = ["not_null"]
    UNIQUE = ["unique"]
    UNIQUE_AND_NOT_NULL = ["unique", "not_null"]


class TestData:
    """Attributes and methods for generating test data."""

    SAMPLE_TAG = ["uat"]

    COLUMNS = [
        ColumnMeta(
            name=Name.ID.value,
            data_type=DataType.BIGINT.value,
            description=Description.ID.value,
            tests=Test.NOT_NULL.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.NAME.value,
            data_type=DataType.TEXT.value,
            description=Description.NAME.value,
            tests=Test.NOT_NULL.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.EMAIL.value,
            data_type=DataType.TEXT.value,
            description=Description.EMAIL.value,
            tests=Test.UNIQUE_AND_NOT_NULL.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.MOBILE.value,
            data_type=DataType.TEXT.value,
            description=Description.MOBILE.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.COUNTRY.value,
            data_type=DataType.TEXT.value,
            description=Description.COUNTRY.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.DOWNLOADED_AT_UTC.value,
            data_type=DataType.TIMESTAMP.value,
            description=Description.DOWNLOADED_AT_UTC.value,
            tags=SAMPLE_TAG,
        ),
    ]

    # Same as above, but without any tests.
    COLUMNS_WITHOUT_TESTS = [
        ColumnMeta(
            name=Name.ID.value,
            data_type=DataType.BIGINT.value,
            description=Description.ID.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.NAME.value,
            data_type=DataType.TEXT.value,
            description=Description.NAME.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.EMAIL.value,
            data_type=DataType.TEXT.value,
            description=Description.EMAIL.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.MOBILE.value,
            data_type=DataType.TEXT.value,
            description=Description.MOBILE.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.COUNTRY.value,
            data_type=DataType.TEXT.value,
            description=Description.COUNTRY.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.DOWNLOADED_AT_UTC.value,
            data_type=DataType.TIMESTAMP.value,
            description=Description.DOWNLOADED_AT_UTC.value,
            tags=SAMPLE_TAG,
        ),
    ]

    # Columns with minimal metadata.
    COLUMNS_MINIMAL = [
        ColumnMeta(
            name=Name.ID.value,
            data_type=DataType.BIGINT.value,
        ),
        ColumnMeta(
            name=Name.NAME.value,
            data_type=DataType.TEXT.value,
        ),
        ColumnMeta(
            name=Name.EMAIL.value,
            data_type=DataType.TEXT.value,
        ),
        ColumnMeta(
            name=Name.MOBILE.value,
            data_type=DataType.TEXT.value,
        ),
        ColumnMeta(
            name=Name.COUNTRY.value,
            data_type=DataType.TEXT.value,
        ),
        ColumnMeta(
            name=Name.DOWNLOADED_AT_UTC.value,
            data_type=DataType.TIMESTAMP.value,
        ),
    ]

    DEFAULT_RESOURCE_METADATA = {
        field: meta_fields_config[field]["default"] for field in meta_fields_config
    }

    # Update the default meta config with some concrete values.
    SOURCE_META = copy.deepcopy(DEFAULT_RESOURCE_METADATA)
    SOURCE_META.update(domains=["source_domain"])

    # This should contain inherited source meta plus any overrides we wish to test for.
    BASE_MODEL_META = copy.deepcopy(DEFAULT_RESOURCE_METADATA)
    BASE_MODEL_META.update(domains=["source_domain", "base_model_domain"])

    # Only the metadata defaults from config plus meta specified below.
    BASE_MODEL_META_NO_INHERITANCE = copy.deepcopy(DEFAULT_RESOURCE_METADATA)
    BASE_MODEL_META_NO_INHERITANCE.update(domains=["base_model_domain"])

    # This should contain inherited base model meta plus any model overrides.
    MODEL_META = copy.deepcopy(DEFAULT_RESOURCE_METADATA)
    MODEL_META.update(domains=["source_domain", "base_model_domain", "model_domain"])

    # Only the metadata defaults from config plus meta specified below.
    MODEL_META_NO_INHERITANCE = copy.deepcopy(DEFAULT_RESOURCE_METADATA)
    MODEL_META_NO_INHERITANCE.update(domains=["model_domain"])

    # Note: until https://github.com/dyvenia/nesso-cli/issues/261 is implemented,
    # `source add` does not actually utilize the nesso config when creating the YAML,
    # and thus below props objects contain some extra keys that are specified in the
    # test config file. These keys are not present when creating the source with
    # `source add`, and so within tests, they need to be manually removed before
    # testing the schema of the output of `source add`.

    # Keep in mind that below source props docstrings are written as if
    # https://github.com/dyvenia/nesso-cli/issues/261 is already implemented.

    @cached_property
    def source_props(self):
        """A source properties object with some metadata overrides.

        Emulates a source props file that is created with `source add` and then modified
        manually to provide additional resource and column metadata.
        """
        table = SourceTable(
            name="test_table_account",
            description="test_description",
            meta=TestData.SOURCE_META,
            columns=TestData.COLUMNS,
        )
        source = Source(
            name=config.bronze_schema, schema=config.bronze_schema, tables=[table]
        )
        source_props = SourceProperties(sources=[source])
        return source_props.to_dict()

    @cached_property
    def source_props_no_overrides(self):
        """A source properties object with only default metadata values.

        Emulates a source props file that is freshly created with `source add`, with no
        metadata overrides.
        """
        table = SourceTable(
            name="test_table_account",
            meta=TestData.DEFAULT_RESOURCE_METADATA,
            columns=TestData.COLUMNS_MINIMAL,
        )
        source = Source(
            name=config.bronze_schema,
            schema=config.bronze_schema,
            tables=[table],
        )
        source_props = SourceProperties(sources=[source])
        return source_props.to_dict()

    # Represent base models which have inherited metadata form above defined source.
    @cached_property
    def base_model_props(self):
        """A model properties object with some metadata overrides.

        Emulates a model props file that is created with `base model bootstrap-yaml`
        and then modified manually to provide additional resource and column metadata.
        """
        model = Model(
            name="int_test_table_account",
            meta=TestData.BASE_MODEL_META,
            columns=TestData.COLUMNS,
        )
        model_props = ModelProperties(models=[model])
        return model_props.to_dict()

    @cached_property
    def base_model_props_without_tests(self):
        """Similar as above, using the same resource metadata, but using modified column
        metadata, with tests removed."""
        model = Model(
            name="int_test_table_account",
            meta=TestData.BASE_MODEL_META,
            columns=TestData.COLUMNS_WITHOUT_TESTS,
        )
        model_props = ModelProperties(models=[model])
        return model_props.to_dict()

    @cached_property
    def base_model_props_no_overrides(self):
        """A model properties object with only default metadata values.

        Emulates a model props file that is freshly created with
        `base_model bootstrap-yaml`, with no metadata overrides.
        """
        model = Model(
            name="int_test_table_account",
            meta=TestData.SOURCE_META,
            columns=TestData.COLUMNS_WITHOUT_TESTS,
        )
        model_props = ModelProperties(models=[model])
        return model_props.to_dict()

    # Represent models which have inherited metadata form above defined base model.
    @cached_property
    def model_props(self):
        """A model properties object with some metadata overrides.

        Emulates a model props file that is created with `model bootstrap-yaml` and then
        modified manually to provide additional resource and column metadata.

        The model inherits above defined base model metadata.
        """
        model = Model(
            name="test_model",
            meta=TestData.MODEL_META,
            columns=TestData.COLUMNS,
        )
        model_props = ModelProperties(models=[model])
        return model_props.to_dict()

    @cached_property
    def model_props_without_tests(self):
        """Similar as above, using the same resource metadata, but using modified column
        metadata, with tests removed."""
        model = Model(
            name="test_model",
            meta=TestData.MODEL_META,
            columns=TestData.COLUMNS_WITHOUT_TESTS,
        )
        model_props = ModelProperties(models=[model])
        return model_props.to_dict()

    @cached_property
    def model_props_no_overrides(self):
        """A model properties object with only default metadata values.

        Emulates a model props file that is freshly created with `model bootstrap-yaml`,
        with no metadata overrides.
        """
        model = Model(
            name="test_model",
            meta=TestData.BASE_MODEL_META,
            columns=TestData.COLUMNS_WITHOUT_TESTS,
        )
        model_props = ModelProperties(models=[model])
        return model_props.to_dict()

    @property
    def model(self):
        return NessoDBTModel(name="test_model")

    @property
    def base_model(self):
        return NessoDBTModel(name="test_table_account", base=True)


TestData = TestData()


@pytest.fixture(params=[TestData.source_props])
def setup_source(request, TEST_SOURCE):
    schema_file_name = TEST_SOURCE + ".yml"
    schema_path = PROJECT_DIR / "models" / "sources" / TEST_SOURCE / schema_file_name
    schema_path.parent.mkdir(parents=True, exist_ok=True)

    with open(schema_path, "w") as file:
        yaml.dump(request.param, file)

    yield schema_path

    shutil.rmtree(schema_path.parent, ignore_errors=True)


@pytest.fixture(
    params=[
        (
            {"model_props": TestData.base_model_props},
            {"silver_schema": config.silver_schema},
        )
    ],
)
def setup_base_model(
    request,
    setup_source,
    postgres_connection,
    TEST_SOURCE,
    TEST_SCHEMA,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Handle the very strange way fixture params work in pytest.
    if isinstance(request.param, tuple):
        model_props = request.param[0]["model_props"]
        silver_schema = request.param[1]["silver_schema"]
    else:
        model_props = request.param["model_props"]
        silver_schema = request.param["silver_schema"]

    base_model_path = (
        PROJECT_DIR / "models" / silver_schema / TEST_TABLE_ACCOUNT_BASE_MODEL
    )
    base_model_file_yml = base_model_path / f"{TEST_TABLE_ACCOUNT_BASE_MODEL}.yml"
    base_model_file_sql = base_model_path / f"{TEST_TABLE_ACCOUNT_BASE_MODEL}.sql"
    base_model_path.mkdir(parents=True, exist_ok=True)

    with open(base_model_file_sql, "w") as f:
        f.write(
            f"select * from {{{{ source('{TEST_SOURCE}', '{TEST_TABLE_ACCOUNT}') }}}}"
        )
    table_fqn = f"{TEST_SOURCE}.{TEST_TABLE_ACCOUNT}"
    view_fqn = f"{TEST_SCHEMA}.{TEST_TABLE_ACCOUNT_BASE_MODEL}"
    postgres_connection.execute(f"CREATE SCHEMA IF NOT EXISTS {TEST_SCHEMA};")
    postgres_connection.execute(
        f"CREATE OR REPLACE VIEW {view_fqn} AS SELECT * FROM {table_fqn};"
    )

    with open(base_model_file_yml, "w") as file:
        yaml.dump(model_props, file)

    yield base_model_file_yml

    shutil.rmtree(base_model_path, ignore_errors=True)
    postgres_connection.execute(f"DROP SCHEMA IF EXISTS {TEST_SCHEMA} CASCADE;")


@pytest.fixture(params=[TestData.model_props])
def setup_model(
    request,
    setup_base_model,
    postgres_connection,
    TEST_SCHEMA,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
    MODEL,
    MODEL_BASE_DIR,
):
    model_file_yml = MODEL_BASE_DIR / f"{MODEL}.yml"
    model_file_sql = MODEL_BASE_DIR / f"{MODEL}.sql"
    MODEL_BASE_DIR.mkdir(parents=True, exist_ok=True)

    with open(model_file_sql, "w") as f:
        f.write(f"select * from {{{{ ref('{TEST_TABLE_ACCOUNT_BASE_MODEL}') }}}}")

    base_model_fqn = f"{TEST_SCHEMA}.{TEST_TABLE_ACCOUNT_BASE_MODEL}"
    model_fqn = f"{TEST_SCHEMA}.{MODEL}"
    postgres_connection.execute(
        f"CREATE OR REPLACE VIEW {model_fqn} AS SELECT * FROM {base_model_fqn};"
    )
    with open(model_file_yml, "w") as file:
        yaml.dump(request.param, file)

    yield model_file_yml

    shutil.rmtree(MODEL_BASE_DIR, ignore_errors=True)
    postgres_connection.execute(f"DROP SCHEMA IF EXISTS {TEST_SCHEMA} CASCADE;")


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown(postgres_connection, TEST_SOURCE):
    # fix https://github.com/dbt-labs/dbt-utils/issues/627
    shutil.rmtree(
        PROJECT_DIR.joinpath(
            "dbt_packages",
            "dbt_utils",
            "tests",
        ),
        ignore_errors=True,
    )

    shutil.rmtree(PROJECT_DIR.joinpath("target"), ignore_errors=True)

    postgres_connection.execute(f"DROP SCHEMA IF EXISTS {TEST_SOURCE} CASCADE;")
    postgres_connection.execute("DROP SCHEMA IF EXISTS test_schema CASCADE;")

    postgres_connection.execute(f"CREATE SCHEMA {TEST_SOURCE};")

    working_dir = os.getcwd()

    os.chdir(PROJECT_DIR)

    shutil.rmtree(PROJECT_DIR.joinpath("models", "sources"), ignore_errors=True)
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", config.silver_schema),
        ignore_errors=True,
    )
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", config.gold_layer_name),
        ignore_errors=True,
    )

    yield

    shutil.rmtree(PROJECT_DIR.joinpath("models", "sources"), ignore_errors=True)
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", config.silver_schema),
        ignore_errors=True,
    )
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", config.gold_layer_name),
        ignore_errors=True,
    )
    SEED_SCHEMA_PATH.unlink(missing_ok=True)

    os.chdir(working_dir)

    postgres_connection.execute(f"DROP SCHEMA IF EXISTS {TEST_SOURCE} CASCADE;")
    postgres_connection.execute("DROP SCHEMA IF EXISTS test_schema CASCADE;")

    shutil.rmtree(PROJECT_DIR.joinpath("target"), ignore_errors=True)

    shutil.rmtree(
        PROJECT_DIR.joinpath(
            "dbt_packages",
            "dbt_utils",
            "tests",
        ),
        ignore_errors=True,
    )

    shutil.rmtree(
        TEST_PROJECT_PATH,
        ignore_errors=True,
    )

    TEST_EXAMPLE_PROFILES_PATH.unlink(missing_ok=True)
    TEST_PROJECT_FILE.unlink(missing_ok=True)
    TEST_TEMPLATE_FILE.unlink(missing_ok=True)
    TEST_TEMPLATE_FILE_TEMPLATED_FILENAME.unlink(missing_ok=True)


@pytest.fixture(scope="session")
def postgres_connection():
    connection = create_engine(
        f"postgresql://user:password@{POSTGRES_HOST}:5432/db",
        connect_args={"connect_timeout": 5},
    )
    yield connection
    connection.dispose()


@pytest.fixture(autouse=True)
def create_contacts_table(
    postgres_connection, setup_and_teardown, TEST_SOURCE, TEST_TABLE_CONTACT
):
    fqn = f"{TEST_SOURCE}.{TEST_TABLE_CONTACT}"
    postgres_connection.execute(f"DROP TABLE IF EXISTS {fqn} CASCADE;")

    class Contact(BaseModel):
        Id: int = Field(default_factory=lambda: i)
        AccountId: str = Field(
            default_factory=lambda: random.randint(1, test_tables_nrows)
        )
        FirstName: str = Field(default_factory=fake.first_name)
        LastName: str = Field(default_factory=fake.last_name)
        ContactEMail: str = Field(default_factory=fake.email)
        MailingCity: str = Field(default_factory=fake.city)
        Country: str = Field(default_factory=fake.country)
        # Pydantic doesn't support fields starting with an underscore so we use aliases
        viadot_downloaded_at_utc: datetime = Field(
            default_factory=datetime.utcnow, alias="_viadot_downloaded_at_utc"
        )

    contacts = []

    for i in range(1, test_tables_nrows + 1):
        contacts.append(Contact(Id=i).dict(by_alias=True))
    contacts_df_pandas = pd.DataFrame(contacts)

    contacts_df_pandas.to_sql(
        TEST_TABLE_CONTACT,
        postgres_connection,
        schema=TEST_SOURCE,
        if_exists="replace",
        index=False,
    )

    yield

    postgres_connection.execute(f"DROP TABLE IF EXISTS {fqn} CASCADE;")


@pytest.fixture(autouse=True)
def create_accounts_table(
    postgres_connection, setup_and_teardown, TEST_SOURCE, TEST_TABLE_ACCOUNT
):
    fqn = f"{TEST_SOURCE}.{TEST_TABLE_ACCOUNT}"
    postgres_connection.execute(f"DROP TABLE IF EXISTS {fqn} CASCADE;")

    class Account(BaseModel):
        id: int = Field(default_factory=lambda: i)
        name: str = Field(default_factory=fake.company)
        email: str = Field(default_factory=fake.email)
        mobile: str = Field(default_factory=fake.phone_number)
        country: str = Field(default_factory=fake.country)
        # Pydantic doesn't support fields starting with an underscore so we use aliases
        viadot_downloaded_at_utc: datetime = Field(
            default_factory=datetime.utcnow, alias="_viadot_downloaded_at_utc"
        )

    accounts = []

    for i in range(1, test_tables_nrows + 1):
        accounts.append(Account(id=i).dict(by_alias=True))
    accounts_df_pandas = pd.DataFrame(accounts)

    accounts_df_pandas.to_sql(
        TEST_TABLE_ACCOUNT,
        postgres_connection,
        schema=TEST_SOURCE,
        if_exists="replace",
        index=False,
    )

    yield

    postgres_connection.execute(f"DROP TABLE IF EXISTS {fqn} CASCADE;")
