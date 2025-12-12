import copy
from pathlib import Path
from typing import Any, Literal, Optional, Union

import dbt.version
from ruamel.yaml import CommentedMap

__dbt_major_version__ = int(dbt.version.installed.major or 0)
__dbt_minor_version__ = int(dbt.version.installed.minor or 0)

if (__dbt_major_version__, __dbt_minor_version__) > (1, 3):
    from dbt.contracts.graph.nodes import ColumnInfo
else:
    from dbt.contracts.graph.parsed import ColumnInfo

from nesso_cli.models.common import (
    DbtProject,
    get_current_dbt_project_obj,
    snakecase,
)
from nesso_cli.models.config import config, yaml
from nesso_cli.models.models import (
    ColumnMeta,
    Model,
    ModelProperties,
    SourceTable,
)


class NessoDBTResource:
    def __init__(
        self,
        name: str,
        dbt_project: DbtProject | None = None,
        env: str = config.default_env,
        base: bool = False,
        comments: list[tuple[str, str]] = [
            ("tests", "tests:"),
            ("unique", "- unique"),
            ("not_null", "- not_null"),
        ],
        **meta,
    ) -> None:
        """Base class for Nesso DBT resources

        Args:
            name (str): The name of the model.
            dbt_project (DbtProject | None, optional): The associated dbt project.
                Defaults to None.
            env (str, optional): The environment for fetching the DBT project.
                Defaults to config.default_env.
            base (bool, optional): Whether the model is a base model. Defaults to False.
            comments (list[tuple[str, str]], optional): List of comment tuples. Each
                tuple contains a comment type and its corresponding string. Defaults to
                [
                    ("tests", "tests:"),
                    ("unique", "- unique"),
                    ("not_null", "- not_null"),
                ].
            meta (dict[str, Any], optional): Keyword arguments specifying metadata
                fields.
        """
        if base:
            base_model_prefix = config.silver_schema_prefix
            if base_model_prefix and not base_model_prefix.endswith("_"):
                base_model_prefix = f"{base_model_prefix}_"

            if not name.startswith(base_model_prefix):
                name = f"{base_model_prefix}{name}"

        self.name = name
        if not dbt_project:
            dbt_project = get_current_dbt_project_obj(target=env, recompile=True)

        self.dbt_project = dbt_project
        self.manifest = self.dbt_project.manifest
        self.node = self._get_self_node()
        self.comments = comments
        self.meta = meta
        self.resource_type = self.node.resource_type.value
        # Validate that meta keys conform to the schema as specified in the config.
        config.validate(meta=meta)

    def _get_self_node(self):
        """Retrieve the node object representing the resource itself."""
        manifest_resources = self.manifest.nodes | self.manifest.sources
        for node in manifest_resources.values():
            if node.name == self.name:
                return node

    def _convert_node_columns_to_pydantic_model(
        self, columns: dict[str, ColumnInfo]
    ) -> list[ColumnMeta]:
        """Cast dbt.ColumnInfo object into ColumnMeta.

        Args:
            columns (dict[str, ColumnInfo]): Dictionary containing column information.

        Returns:
            list[ColumnMeta]: List of ColumnMeta objects.
        """
        columns_values = list(columns.values())
        columns_metadata = [
            ColumnMeta(
                name=col.name,
                data_type=col.data_type,
                description=col.description,
                quote=col.quote,
                tags=col.tags,
            )
            for col in columns_values
        ]
        return columns_metadata

    def get_columns(self) -> list[ColumnMeta]:
        """Retrieve columns for the source/model from the database.

        Raises:
            ValueError: If the specified source/model node cannot be found.

        Returns:
            list[ColumnMeta]: List of ColumnMeta objects.
        """
        if self.resource_type == "source":
            node = self.dbt_project.get_source_node(
                target_source_name=self.node.schema, target_table_name=self.name
            )
        else:
            node = self.dbt_project.get_ref_node(target_model_name=self.name)

        if node is None:
            raise ValueError(f"Could not find node for table '{self.name}'.")

        columns_list, *_ = self.dbt_project.get_columns_in_node(node)

        columns_metadata = []
        for column in columns_list:
            columns_metadata.append(
                ColumnMeta(
                    name=(
                        snakecase(column.name)
                        if config.snakecase_columns
                        else column.name
                    ),
                    data_type=column.data_type.upper(),
                )
            )

        return columns_metadata

    def _add_comments_to_yaml(self, content: dict[str, Any]) -> CommentedMap:
        """Adds a comments to the YAML file.

        Args:
            content (dict[str, Any]): Content of the YAML file to which
                add tests fields.

        Returns:
            CommentedMap: ruamel.yaml object with added comments.
        """

        # Set variables based on the content type.
        if "sources" in content.keys():
            content_type = "sources"
            key_indent = 12
            tables = content[content_type][0]["tables"]
        else:
            content_type = "models"
            key_indent = 8
            tables = content[content_type]

        value_indent = key_indent + 2

        for table in tables:
            for col in table["columns"]:
                # Changes column type to add Comments to it.
                col = CommentedMap(col)

                # Adds selected comments if tests field is already specified.
                if "tests" in col:
                    for comment_name, comment in self.comments:
                        if comment_name != "tests" and comment_name not in col["tests"]:
                            indent = (
                                value_indent if comment.startswith("-") else key_indent
                            )

                            col.yaml_set_comment_before_after_key(
                                "tags",
                                before=comment,
                                indent=indent,
                            )
                else:
                    for comment_name, comment in self.comments:
                        indent = value_indent if comment.startswith("-") else key_indent

                        col.yaml_set_comment_before_after_key(
                            "tags",
                            before=comment,
                            indent=indent,
                        )

                table["columns"][table["columns"].index(col)] = col

        return content


class NessoDBTModel(NessoDBTResource):
    def __init__(
        self,
        name: str,
        dbt_project: DbtProject | None = None,
        env: str = config.default_env,
        base: bool = False,
        comments: list[tuple[str, str]] = [
            ("tests", "tests:"),
            ("unique", "- unique"),
            ("not_null", "- not_null"),
        ],
        **meta,
    ) -> None:
        """An opinionated version of a DBT model.

        Args:
            name (str): The name of the model.
            dbt_project (DbtProject | None, optional): The associated dbt project.
                Defaults to None.
            env (str, optional): The environment for fetching the DBT project.
                Defaults to config.default_env.
            base (bool, optional): Whether the model is a base model. Defaults to False.
            comments (list[tuple[str, str]], optional): List of comment tuples. Each
                tuple contains a comment type and its corresponding string. Defaults to
                [
                    ("tests", "tests:"),
                    ("unique", "- unique"),
                    ("not_null", "- not_null"),
                ].
            meta (dict[str, Any], optional): Keyword arguments specifying metadata
                fields.
        """
        super().__init__(
            name,
            dbt_project,
            env,
            base,
            comments,
            **meta,
        )

    def get_model_upstream_dependencies(self) -> list[str]:
        """Retrieve the upstream dependencies of a given model, one level deep.

        Raises:
            ValueError: If the dependencies for model were not found in the manifest.

        Returns:
            list[str]: A list of model dependencies names.
        """
        upstream_dependencies = self.node.depends_on.nodes
        if not upstream_dependencies:
            msg = f"""Dependencies for model '{self.name}' were not found.

Possible causes:
- incorrect model name was specified
- some model(s) do not use ref() and/or source() macros
"""
            raise ValueError(msg)
        return self.node.depends_on.nodes

    def get_node_metadata(self, node_name: str) -> Union[SourceTable, Model]:
        """Retrieve metadata for a given node.

        Args:
            node_name (str): dbt project node name. Example of node name format
                "source.postgres.staging.test_table_account".

        Raises:
            ValueError: If the node is not found.

        Returns:
            Union[SourceTable, Model]: Metadata for the given node.
        """
        node_name_fqn = node_name.split(".")
        node_type = node_name_fqn[0]
        node_table_name = node_name_fqn[-1]
        if node_type == "source":
            for node in self.manifest.sources.values():
                if node.name == node_table_name:
                    metadata = SourceTable(
                        name=node.name,
                        description=node.description,
                        meta=node.meta,
                        columns=self._convert_node_columns_to_pydantic_model(
                            columns=node.columns
                        ),
                    )
        elif node_type == "model":
            for node in self.manifest.nodes.values():
                if node.name == node_table_name:
                    metadata = Model(
                        name=node.name,
                        description=node.description,
                        meta=node.meta,
                        columns=self._convert_node_columns_to_pydantic_model(
                            columns=node.columns
                        ),
                    )
        else:
            raise ValueError(f"Node '{node_name}' was not found.")

        return metadata

    def get_upstream_metadata(
        self, upstream_dependencies: Optional[list[str]] = None
    ) -> list[Union[SourceTable, Model]]:
        """Retrieve metadata for upstream dependencies.

        Args:
            upstream_dependencies (Optional[list[str]], optional): List of upstream
                dependencies. Defaults to None.

        Returns:
            list[Union[SourceTable, Model]]: List of metadata objects
                for given dependencies.
        """
        if upstream_dependencies is None:
            upstream_dependencies = self.get_model_upstream_dependencies()

        upstream_metadata = [
            self.get_node_metadata(node_name=dependency)
            for dependency in upstream_dependencies
        ]

        return upstream_metadata

    def resolve_columns_metadata(
        self,
        upstream_metadata: Optional[list[Union[SourceTable, Model]]] = None,
    ) -> list[ColumnMeta]:
        """Inherit column metadata from upstream resource(s).

        In case of multiple upstream resources, inherits on a "first come, first served"
        basis.

        Args:
            upstream_metadata (Optional[list[Union[SourceTable, Model]]], optional):
                List of upstream metadata. Defaults to None.

        Returns:
            list[ColumnMeta]: List of resolved model column metadata.
        """
        if not upstream_metadata:
            upstream_metadata = self.get_upstream_metadata()

        model_columns = self.get_columns()

        for model_column in model_columns:
            for dependency in upstream_metadata:
                upstream_column = next(
                    (
                        col
                        for col in dependency.columns
                        if col.name == model_column.name
                    ),
                    None,
                )
                if upstream_column:
                    self._resolve_column_values(model_column, upstream_column)

        return model_columns

    def _resolve_column_values(
        self, model_column: ColumnMeta, upstream_column: ColumnMeta
    ) -> None:
        """Resolve column metadata.

        In case of a `None` value, inherit the first encountered upstream column value
        for that field.

        Args:
            model_column (ColumnMeta): Model column metadata to be overwritten if empty.
            upstream_column (ColumnMeta): Upstream model column metadata to be used to
                overwrite model column fields.
        """
        for attribute in model_column.__fields__:
            value = getattr(model_column, attribute)
            if attribute != "tests" and not value:
                setattr(model_column, attribute, getattr(upstream_column, attribute))

    def _set_meta_value(
        self,
        meta: dict[str, Any],
        field_name: str,
        upstream_value: Any,
        inheritance_strategy: Literal["overwrite", "skip", "append"],
        default_value: Any,
    ) -> dict[str, Any]:
        """Set a meta field to a value based on the specified inheritance strategy.

        There are three available strategies:
        - append: extend upstream values with new values specified in `self.meta`. Only
            supported for meta keys of type `list`.
        - skip: do not inherit from upstream values, ie. take user-specified value or
            the default
        - overwrite: use upstream metadata over user-specified values

        Args:
            meta (dict[str, Any]): Dictionary with data to set.
            field_name (str): Filed name to update.
            upstream_value (Any): Upstream value for specified `field_name`.
            inheritance_strategy (Literal[overwrite, skip, append]): One of three
                possible inheritance strategies.
            default_value (Any): Default value for specified `field_name`.

        Raises:
            ValueError: If unknown inheritance strategy was specified.

        Returns:
            dict[str, Any]: Updated dictionary with meta fields.
        """
        if inheritance_strategy == "append":
            if isinstance(upstream_value, list):
                # Insert upstream list values in front of the list.
                meta[field_name][0:0] = upstream_value
            else:
                meta[field_name].append(upstream_value)
        elif inheritance_strategy == "overwrite":
            meta[field_name] = upstream_value
        elif inheritance_strategy == "skip":
            if meta[field_name] != default_value:
                pass
            else:
                meta[field_name] = default_value
        else:
            raise ValueError(f"Unknown inheritance strategy: '{inheritance_strategy}'.")

        return meta

    def _resolve_resource_level_metadata_values(
        self,
        upstream_metadata: list[Union[SourceTable, Model]],
    ) -> dict[str, Any]:
        """Resolve resource-level (as opposed to column-level) metadata.

        Resolve resource metadata with its upstream metadata using the inheritance
        strategy specified in the nesso-cli config.

        Args:
            upstream_metadata (list[Union[SourceTable, Model]]): List of upstream
                metadata objects.

        Returns:
            dict[str, Any]: Dictionary containing resolved metadata.
        """

        meta_fields_config = config.metadata["fields"]
        meta = copy.deepcopy(self.meta)

        # If a meta key is not specified, take the default value from config.
        for key in meta_fields_config:
            if key not in meta:
                meta[key] = meta_fields_config[key]["default"]

        # Set values for meta fields based on their configuration.
        for dependency in upstream_metadata:
            for key, value in dependency.meta.items():
                inheritance_strategy = config.get_inheritance_strategy(key)
                default_value = meta_fields_config[key]["default"]
                if key in meta:
                    meta = self._set_meta_value(
                        meta=meta,
                        field_name=key,
                        inheritance_strategy=inheritance_strategy,
                        upstream_value=value,
                        default_value=default_value,
                    )

        # Delete duplicates from meta fields.
        for key, value in meta.items():
            if isinstance(value, list):
                if not any(isinstance(item, dict) for item in value):
                    meta[key] = list(dict.fromkeys(value))

        return meta

    def resolve_model_metadata(self) -> Model:
        """Inherit metadata from upstream resource.

        Returns:
            Model: Pydantic object with metadata.
        """

        upstream_metadata = self.get_upstream_metadata()
        resource_metadata = self._resolve_resource_level_metadata_values(
            upstream_metadata
        )
        column_metadata = self.resolve_columns_metadata(
            upstream_metadata=upstream_metadata
        )

        return Model(name=self.name, meta=resource_metadata, columns=column_metadata)

    def to_dict(self) -> dict[str, Any]:
        """Convert model to a dictionary, first inheriting upstream metadata.

        Returns:
            dict[str, Any]: A `ModelProperties` model, converted to a dictionary.
        """
        model = self.resolve_model_metadata()
        model_properties = ModelProperties(models=[model])
        return model_properties.to_dict()

    def to_yaml(self, yml_path: Path | str, comments: bool = True) -> None:
        """Serialize model metadata as a YAML file.

        Args:
            yml_path (Path | str): Path to the YAML file.
            comments (bool, optional): Whether add comments to the YAML file.
                Defaults to True.
        """
        model_properties = self.to_dict()

        if comments:
            model_properties = self._add_comments_to_yaml(content=model_properties)

        with open(yml_path, "w") as file:
            yaml.dump(model_properties, file)
