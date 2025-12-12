from conftest import TestData
from nesso_cli.models.config import yaml
from nesso_cli.models.resources import NessoDBTModel


def test__add_comments_to_yaml(setup_model, MODEL):
    props = NessoDBTModel(name=MODEL)
    props.to_yaml(setup_model)

    with open(setup_model) as f:
        yaml_content = yaml.load(f)

    # Test.
    yaml_content_with_comments = TestData.model._add_comments_to_yaml(
        content=yaml_content
    )
    with open(setup_model, "w") as file:
        yaml.dump(yaml_content_with_comments, file)

    # Check that comments are included in the YAML file and correctly indented.
    with open(setup_model) as f:
        yaml_str = f.read()

    assert " " * 8 + "# tests:" in yaml_str
    assert " " * 10 + "# - unique" in yaml_str
