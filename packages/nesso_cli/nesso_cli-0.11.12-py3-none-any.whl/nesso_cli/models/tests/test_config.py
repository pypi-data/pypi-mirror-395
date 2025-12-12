import pytest
from nesso_cli.models.config import config


def test_get_inheritance_strategy_global_default():
    retrieved_strategy = config.get_inheritance_strategy("test_meta_key")
    expected_strategy = "overwrite"
    assert retrieved_strategy == expected_strategy


def test_get_inheritance_strategy_per_type_default():
    retrieved_strategy = config.get_inheritance_strategy("test_meta_key2")
    expected_strategy = "append"
    assert retrieved_strategy == expected_strategy


def test_get_inheritance_strategy_key_specific():
    retrieved_strategy = config.get_inheritance_strategy("test_meta_key3")
    expected_strategy = "skip"
    assert retrieved_strategy == expected_strategy


def test_validate():
    meta = {"test_meta_key": "123"}
    with pytest.raises(ValueError):
        config.validate(meta)
