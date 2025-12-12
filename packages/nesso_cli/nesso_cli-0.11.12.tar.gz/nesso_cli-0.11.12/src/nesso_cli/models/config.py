import ast
from typing import Any

from ruamel.yaml import YAML

from nesso_cli.models import context

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.representer.ignore_aliases = lambda x: True


class NessoConfig:
    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self.set(key, value)

    @staticmethod
    def get(key: str):
        path = context.get("PROJECT_DIR") / ".nesso/config.yml"
        if not path.exists():
            if key in globals():
                # Return the default value, specified below in this file.
                return globals()[key]
            raise ValueError(f"Config file '{path}' does not exist.")
        with open(path) as f:
            # Get the config as dict. Ruamel.yaml doesn't provide any API to convert to
            # dict, but we can hack it ourselves using the repr, which provides a
            # dictionary representation of the object, although using single quotes,
            # hence the need to load it using `ast.literal_eval()` instead of using
            # `json.loads()`.
            config_ruamel_object = yaml.load(f)
            config = ast.literal_eval(repr(config_ruamel_object))
            return config.get(key)

    @staticmethod
    def set(key: str, value: str) -> None:
        path = context.get("PROJECT_DIR") / ".nesso/config.yml"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path) as f:
            config = yaml.load(f)
            config[key] = value
        with open(path, "w") as f:
            yaml.dump(config, f)

    def validate(self, meta: dict[str, Any]):
        """Validate that meta keys conform to the schema as specified in the config.

        Args:
            meta (dict[str, Any]): The meta keys to validate.

        Raises:
            ValueError: If the default value is not specified for a metadata field.
            ValueError: If the metadata field is of an incorrect type.
        """
        for key in meta:
            meta_type_in_param = type(meta[key])
            meta_type_in_config = type(self.metadata["fields"][key]["default"])

            if "default" not in self.metadata["fields"][key].keys():
                msg = "Default values are required for all metadata fields."
                raise ValueError(msg)
            elif not meta_type_in_param == meta_type_in_config:
                msg = f"Meta field '{key}' is of incorrect type."
                msg += f" Expected: '{meta_type_in_config.__name__}'."
                raise ValueError(msg)

    def get_inheritance_strategy(self, key: Any) -> Any:
        """Get the inheritance strategy for a specified value."""
        # First, attempt to use the inheritance strategy specified at the field level.
        for field in self.metadata["fields"]:
            if field == key:
                strategy = self.metadata["fields"][key].get("inheritance_strategy")
                if strategy:
                    return strategy

        # In case it's not, fall back to per-type defaults.
        value_type = type(self.metadata["fields"][key]["default"]).__name__
        is_defaults = self.metadata["inheritance_strategies"]["defaults"]
        for types_group in is_defaults:
            if value_type in types_group["types"]:
                return types_group["strategy"]

        # Fall back to a global default if no default for the given type is found.
        return self.metadata["inheritance_strategies"]["default_strategy"]


# These values are only used as defaults when first creating the config
# with `nesso models init project`.
project_name = "my_nesso_project"
database_type = "duckdb"
bronze_schema = "staging"
silver_schema = "intermediate"
silver_schema_prefix = "int"
gold_layer_name = "marts"
data_architecture = "marts"
macros_path = "dbt_packages/nesso_macros/macros"
default_env = "dev"
snakecase_columns = True
luma = {"enabled": True}

config = NessoConfig()
