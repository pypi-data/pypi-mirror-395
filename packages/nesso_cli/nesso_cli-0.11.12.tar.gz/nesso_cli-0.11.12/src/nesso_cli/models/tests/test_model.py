from pathlib import Path

import nesso_cli.models.context as context
from conftest import TestData
from nesso_cli.models.config import yaml
from nesso_cli.models.main import app
from typer.testing import CliRunner

PROJECT_DIR = Path(__file__).parent.joinpath("dbt_projects", "postgres")
context.set("PROJECT_DIR", PROJECT_DIR)
TEST_DBT_TARGET = "dev"

runner = CliRunner()


def test_model_bootstrap(MODEL, MODEL_PATH, MART):
    # Assumptions.
    assert not MODEL_PATH.exists()

    # Test.
    result = runner.invoke(app, ["model", "bootstrap", MODEL, "--subdir", MART])

    assert result.exit_code == 0
    assert MODEL_PATH.exists()

    # Cleaning up after the test
    MODEL_PATH.unlink()


def test_model_bootstrap_yaml(
    setup_model,
    MODEL,
    MODEL_YAML_PATH,
):
    # Delete model YAML file created by the `setup_model()` fixture.
    setup_model.unlink()

    # Assumption.
    assert not MODEL_YAML_PATH.exists()

    # Bootstrap YAML for the model.
    result = runner.invoke(
        app,
        [
            "model",
            "bootstrap-yaml",
            MODEL,
            "-e",
            TEST_DBT_TARGET,
        ],
    )

    assert result.exit_code == 0
    assert MODEL_YAML_PATH.exists()
    assert setup_model.exists()

    expected_schema = TestData.model_props_no_overrides

    with open(setup_model) as f:
        schema = yaml.load(f)

    assert schema == expected_schema

    with open(setup_model) as f:
        yaml_str = f.read()

    # Check that comments are included in the YAML file.
    assert "# tests:" in yaml_str


def test_model_bootstrap_yaml_provide_meta_as_options(
    setup_model,
    MODEL,
    MODEL_YAML_PATH,
):
    # Delete model YAML file created by the `setup_model()` fixture.
    setup_model.unlink()

    # Assumption.
    assert not MODEL_YAML_PATH.exists()

    # Bootstrap YAML for the model with meta args.
    result = runner.invoke(
        app,
        [
            "model",
            "bootstrap-yaml",
            MODEL,
            "-e",
            TEST_DBT_TARGET,
            "--domains",
            '["model_domain"]',
        ],
    )

    assert result.exit_code == 0
    assert MODEL_YAML_PATH.exists()
    assert setup_model.exists()

    with open(setup_model) as f:
        schema = yaml.load(f)

    # Validate whether the `domain` key was created as expected, ie. the provided value
    # was added to the inherited list.
    assert schema == TestData.model_props_without_tests

    with open(setup_model) as f:
        yaml_str = f.read()

    # Check that comments are included in the YAML file.
    assert "# tests:" in yaml_str
