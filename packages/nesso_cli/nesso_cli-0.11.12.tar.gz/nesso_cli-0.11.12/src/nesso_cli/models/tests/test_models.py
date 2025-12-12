import copy

import pytest
from conftest import TestData
from nesso_cli.models.config import config, yaml
from nesso_cli.models.models import DBTProperties, ModelProperties
from test_update import (
    COLUMNS_AFTER_DELETE,
    COLUMNS_AFTER_INSERT,
    YAML_SOURCE_COLUMNS,
    YAML_SOURCE_COLUMNS_METADATA,
)


@pytest.fixture()
def BASE_MODEL_FQN(TEST_TABLE_ACCOUNT_BASE_MODEL):
    return f"model.{config.database_type}.{TEST_TABLE_ACCOUNT_BASE_MODEL}"


@pytest.fixture()
def dbt_properties(setup_source):
    dp = DBTProperties(file_path=setup_source)
    yield dp


#####################
### DBTProperties ### # noqa
#####################


def test_set_yaml_content(dbt_properties):
    dbt_properties[dbt_properties.resource_type] = "test"
    dbt_properties.set_yaml_content()

    with open(dbt_properties.file_path, "r") as file:
        yaml_dict = yaml.load(file)

    assert yaml_dict == {"version": 2, dbt_properties.resource_type: "test"}


def test_set_columns_order(TEST_TABLE_ACCOUNT, dbt_properties):
    def _get_columns_order(path):
        with open(path, "r") as file:
            yaml_dict = yaml.load(file)

        columns = yaml_dict[dbt_properties.resource_type][0]["tables"][0]["columns"]
        columns_order = [col["name"] for col in columns]

        return columns_order

    initial_columns_order = [
        "id",
        "name",
        "email",
        "mobile",
        "country",
        "_viadot_downloaded_at_utc",
    ]

    columns_order = _get_columns_order(dbt_properties.file_path)

    assert columns_order == initial_columns_order

    desired_columns_order = [
        "id",
        "mobile",
        "country",
        "name",
        "_viadot_downloaded_at_utc",
        "email",
    ]
    dbt_properties.set_columns_order(
        desired_order=desired_columns_order, table_name=TEST_TABLE_ACCOUNT
    )

    columns_order = _get_columns_order(dbt_properties.file_path)

    assert columns_order == desired_columns_order


def test_get_yaml_table_columns(TEST_TABLE_ACCOUNT, dbt_properties):
    columns_metadata = dbt_properties.get_yaml_table_columns(
        table_name=TEST_TABLE_ACCOUNT,
    )
    assert columns_metadata == YAML_SOURCE_COLUMNS_METADATA


def test_coherence_scan(TEST_SOURCE, TEST_TABLE_ACCOUNT, dbt_properties):
    diff, yaml_columns, db_columns = dbt_properties.coherence_scan(
        schema_name=TEST_SOURCE,
        table_name=TEST_TABLE_ACCOUNT,
    )
    assert not diff
    assert yaml_columns == YAML_SOURCE_COLUMNS_METADATA
    assert db_columns == YAML_SOURCE_COLUMNS


def test_add_column(TEST_TABLE_ACCOUNT, dbt_properties):
    dbt_properties.add_column(
        table_name=TEST_TABLE_ACCOUNT,
        column_name="new_column_name",
        index=6,
        data_type="CHARACTER VARYING(255)",
    )

    yaml_columns_metadata = dbt_properties.get_yaml_table_columns(
        table_name=TEST_TABLE_ACCOUNT
    )

    assert yaml_columns_metadata == COLUMNS_AFTER_INSERT


def test_delete_column(TEST_TABLE_ACCOUNT, dbt_properties):
    dbt_properties.delete_column(
        table_name=TEST_TABLE_ACCOUNT, column_name="_viadot_downloaded_at_utc"
    )
    yaml_columns_metadata = dbt_properties.get_yaml_table_columns(
        table_name=TEST_TABLE_ACCOUNT
    )

    assert yaml_columns_metadata == COLUMNS_AFTER_DELETE


#####################
### NessoDBTModel ### # noqa
#####################


def test_dbt_model_get_model_upstream_dependencies(setup_model, BASE_MODEL_FQN):
    model_nodes = TestData.model.get_model_upstream_dependencies()
    assert model_nodes == [BASE_MODEL_FQN]


def test_dbt_model_get_node_metadata(setup_model, BASE_MODEL_FQN):
    node_metadata = TestData.model.get_node_metadata(node_name=BASE_MODEL_FQN)
    node_metadata_properties = ModelProperties(models=[node_metadata]).to_dict()
    assert node_metadata_properties == TestData.base_model_props_without_tests


def test_dbt_model_get_upstream_metadata(setup_model):
    base_model_metadata = TestData.model.get_upstream_metadata()
    base_model_properties = ModelProperties(models=base_model_metadata).to_dict()
    assert base_model_properties == TestData.base_model_props_without_tests


def test_dbt_model_get_columns(setup_model):
    columns = TestData.model.get_columns()
    assert columns == TestData.COLUMNS_MINIMAL


def test_dbt_model_resolve_columns_metadata(setup_model):
    model_columns = TestData.model.resolve_columns_metadata()
    assert model_columns == TestData.COLUMNS_WITHOUT_TESTS


def test_dbt_model__resolve_column_values(setup_model):
    model_column = copy.deepcopy(TestData.COLUMNS_MINIMAL)[0]
    upstream_column = copy.deepcopy(TestData.COLUMNS_WITHOUT_TESTS)[0]
    # Currently, _resolve_column_values() modifies `model_column` inplace.
    TestData.model._resolve_column_values(
        model_column=model_column,
        upstream_column=upstream_column,
    )
    assert model_column.dict() == upstream_column.dict()


@pytest.mark.parametrize(
    "inheritance_strategy, expected",
    [
        (
            "append",
            {"test_list": ["upstream_value", "element1", "element2", "element3"]},
        ),
        ("skip", {"test_list": ["element1", "element2", "element3"]}),
        ("overwrite", {"test_list": ["upstream_value"]}),
    ],
)
def test__set_meta_value(setup_model, inheritance_strategy, expected):
    test_field_name = "test_list"
    default_meta = {test_field_name: ["element1", "element2", "element3"]}
    meta = TestData.model._set_meta_value(
        meta=default_meta,
        field_name=test_field_name,
        upstream_value=["upstream_value"],
        inheritance_strategy=inheritance_strategy,
        default_value=default_meta[test_field_name],
    )
    assert meta == expected


def test_dbt_model_resolve_model_metadata(setup_model):
    """Verify that the model correctly inherits metadata from the base model."""
    model = TestData.model.resolve_model_metadata()
    props = ModelProperties(models=[model]).to_dict()
    assert props == TestData.model_props_no_overrides


def test_dbt_model_to_dict_model(setup_model):
    # In setup_model(), we create a base model and then a model without any overrides.
    # Thus, the model should inherit base model metadata without adding anything on top.
    data = TestData.model.to_dict()
    assert data == TestData.model_props_no_overrides


def test_dbt_model_to_dict_base_model(setup_base_model):
    # In setup_base_model(), we create a source and then a base model without any
    # overrides. Thus, the base model should inherit source metadata without adding
    # anything on top.
    data = TestData.base_model.to_dict()
    assert data == TestData.base_model_props_no_overrides


def test_dbt_model_to_yaml_model(setup_model, MODEL_YAML_PATH):
    # Remove the YAML file created by setup_model().
    MODEL_YAML_PATH.unlink(missing_ok=True)

    # Test.
    TestData.model.to_yaml(MODEL_YAML_PATH)

    # Validate.
    with open(MODEL_YAML_PATH) as f:
        schema = yaml.load(f)

    assert schema == TestData.model_props_no_overrides


def test_dbt_model_to_yaml_model_quoting(setup_model, MODEL_YAML_PATH):
    """Validate quoting in the created YAML."""
    # Remove the YAML file created by setup_model().
    MODEL_YAML_PATH.unlink(missing_ok=True)

    # Test.
    TestData.model.to_yaml(MODEL_YAML_PATH)

    with open(MODEL_YAML_PATH) as f:
        text = f.read()

    descr_start_pos = text.find("description:") + len("description: ")
    descr_end_pos = descr_start_pos + 2
    assert text[descr_start_pos:descr_end_pos] == "''"


def test_dbt_model_to_yaml_base_model(setup_base_model, BASE_MODEL_YAML_PATH):
    # Remove the YAML file created by setup_base_model().
    BASE_MODEL_YAML_PATH.unlink(missing_ok=True)

    # Test.
    TestData.base_model.to_yaml(BASE_MODEL_YAML_PATH)

    # Validate.
    with open(BASE_MODEL_YAML_PATH) as f:
        schema = yaml.load(f)

    assert schema == TestData.base_model_props_no_overrides
