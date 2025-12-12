from enum import Enum
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field, create_model

from nesso_cli.models.common import (
    dict_diff,
    get_db_table_columns,
)
from nesso_cli.models.config import yaml


class BaseNessoModel(BaseModel):
    def to_dict(self):
        # Convert to dictionary, excluding fields with None values,
        # as dbt >= 1.5 doesn't accept None in the `tests` field.
        return self.dict(exclude_none=True, by_alias=True)


class ColumnMeta(BaseNessoModel):
    name: str
    data_type: str
    description: str = ""
    quote: bool = True
    tests: list[str] | None = None
    tags: list[str] = []


class SourceTable(BaseNessoModel):
    name: str
    description: str = ""
    loaded_at_field: str = "_viadot_downloaded_at_utc::timestamp"
    freshness: dict[str, dict[str, int | str]] = {
        "warn_after": {"count": 24, "period": "hour"},
        "error_after": {"count": 48, "period": "hour"},
    }
    tags: list[str] = []
    meta: dict[str, Any]
    columns: list[ColumnMeta]


class Model(BaseNessoModel):
    name: str
    description: str = ""
    meta: dict[str, Any]
    columns: list[ColumnMeta]


class Source(BaseNessoModel):
    name: str
    schema_: str = Field(alias="schema")
    description: str | None = None
    tables: list[SourceTable]


class SourceProperties(BaseNessoModel):
    version: int = 2
    sources: list[Source]


class ModelProperties(BaseNessoModel):
    version: int = 2
    models: list[Model]


class DBTDatabaseConfig(BaseModel):
    """Common DBT database configuration (for most databases)."""

    db_type: str = Field(default=None, alias="type")
    host: str = "localhost"
    schema_: str = Field(default="dbt_nesso_user", alias="schema")
    threads: int = 16
    retries: int = 1
    # connect_timeout: int = None


class DBTTrinoConfig(DBTDatabaseConfig):
    db_type: str = Field(default="trino", alias="type")
    port: int = 8080
    database: str = "default"
    user: str = "nesso_user"


class DBTPostgresConfig(DBTDatabaseConfig):
    db_type: str = Field(default="postgres", alias="type")
    port: int = 5432
    dbname: str = "postgres"
    user: str = "nesso_user"
    password: str = ""


class DBTRedshiftConfig(DBTPostgresConfig):
    db_type: str = Field(default="redshift", alias="type")
    method: Literal["database", "sso"] = "database"
    scope: str | None = None
    client_id: str | None = None
    idp_tenant: str | None = None
    sso_cache: bool = True


class DBTDatabricksConfig(DBTDatabaseConfig):
    db_type: str = Field(default="databricks", alias="type")
    http_path: str = "sql/protocolv1/o/<workspace-id>/<cluster-id>"
    token: str = ""
    session_properties: dict = {
        "query_max_planning_time": "2m",
        "query_max_run_time": "60m",
        "retry_initial_delay": "1s",
        "retry_max_delay": "30s",
        "late_materialization": True,
    }


class DBTSQLServerConfig(DBTDatabaseConfig):
    db_type: str = Field(default="sqlserver", alias="type")
    driver: str = "Microsoft ODBC Driver 17 for SQL Server"
    port: int = 1433
    database: str = "dbo"
    login_timeout: int = 10
    query_timeout: int = 3600
    user: str = "nesso_user"
    password: str = "nesso_password"


class DBTDuckDBConfig(BaseModel):
    db_type: str = Field(default="duckdb", alias="type")
    schema_: str = Field(default="main", alias="schema")
    path: str = "nesso.duckdb"
    threads: int = 16


def NessoDBTConfig(
    db_type: str, project_name: str = "my_nesso_project"
) -> "NessoDBTConfig":
    config_class = get_dbt_config_class(db_type)
    config = {"target": "dev", "outputs": {"dev": config_class()}}
    model = create_model(
        "NessoDBTConfig", **{project_name: (dict, {project_name: config})}
    )
    return model(**{project_name: config})


dbt_config_map = {
    "trino": DBTTrinoConfig,
    "postgres": DBTPostgresConfig,
    "redshift": DBTRedshiftConfig,
    "databricks": DBTDatabricksConfig,
    "sqlserver": DBTSQLServerConfig,
    "duckdb": DBTDuckDBConfig,
}


def get_dbt_config_class(dbt_db_type: str) -> DBTDatabaseConfig:
    """A factory method-ish helper for getting the correct dbt config class.

    Get dbt config class depending on the database used.

    Args:
        dbt_db_type (str): One of the supported dbt database types.

    Raises:
        NotImplementedError: If a non-supported database type is passed.

    Returns:
        DBTDatabaseConfig: The pydantic model for the configuration
            of the specified database.

    """
    if dbt_db_type not in dbt_config_map:
        raise NotImplementedError(f"Unsupported database type: '{dbt_db_type}'.")

    config_class = dbt_config_map[dbt_db_type]
    return config_class


class ModelColumnsMetadata(BaseModel):
    quote: bool
    data_type: str
    description: str | None
    tests: list[str] | None
    tags: list[str]


class DBTResourceType(Enum):
    SOURCE = "sources"
    MODEL = "models"


class DBTProperties(dict):
    def __init__(self, file_path: str | Path):
        self.file_path = file_path
        self.__resource_type = None
        self._load_properties()
        self.__modification_time = self.file_path.stat().st_mtime

    def _load_properties(self):
        """Load dbt properties from the specified YAML file."""
        with open(self.file_path) as file:
            yaml_dict = yaml.load(file)

        for key in yaml_dict:
            if key not in self.keys():
                self[key] = yaml_dict[key]

    @property
    def resource_type(self):
        """Determine resource type based on the content of the props file."""
        if DBTResourceType.SOURCE.value in self:
            self.__resource_type = DBTResourceType.SOURCE.value
            return self.__resource_type
        if DBTResourceType.MODEL.value in self:
            self.__resource_type = DBTResourceType.MODEL.value
            return self.__resource_type
        msg = "Unsupported dbt resource type (must be either a source or a model)."
        raise ValueError(msg)

    def set_yaml_content(self):
        """Write the content of a dictionary to a YAML file."""
        with open(self.file_path, "w") as file:
            yaml.dump(dict(self), file)

        self.__modification_time = self.file_path.stat().st_mtime

    def set_columns_order(
        self,
        desired_order: list[str],
        table_name: str,
    ) -> None:
        """Reorder columns in a specified table in a YAML file.

        Args:
            desired_order (list[str]): List of column names in the desired order.
            table_name (str): Name of the table to reorder columns in.

        """

        def custom_sort(item):
            return desired_order.index(item["name"])

        for content in self[self.resource_type]:
            if self.resource_type == DBTResourceType.SOURCE.value:
                for table in content["tables"]:
                    if table["name"] == table_name:
                        table["columns"] = sorted(table["columns"], key=custom_sort)
            elif self.resource_type == DBTResourceType.MODEL.value:
                content["columns"] = sorted(content["columns"], key=custom_sort)

        self.set_yaml_content()

    def get_yaml_table_columns(
        self,
        table_name: str,
    ) -> dict[str, ModelColumnsMetadata]:
        """Retrieve column information for a specific table from a YAML file.

        Args:
            table_name (str): The name of the table for which to retrieve column names.

        Returns:
            columns_dict_metadata (dict[str, ModelColumnsMetadata]): A dictionary
                containing columns and their metadata.

        """
        # Checks the validity of dbt properties
        if self.__modification_time != self.file_path.stat().st_mtime:
            raise ValueError("The file was modified during the processing.")

        def create_metadata_dict(
            column: dict[str, Any],
        ) -> dict[str, ModelColumnsMetadata]:
            # Creates a dict with only metadata (without column name).
            column_metadata = column.copy()
            del column_metadata["name"]
            # Verifies if metadata types align with those specified in
            # ModelColumnsMetadata.
            ModelColumnsMetadata.validate(column_metadata)
            return column_metadata

        columns_dict_metadata = {}
        for content in self[self.resource_type]:
            if self.resource_type == DBTResourceType.SOURCE.value:
                for table in content["tables"]:
                    if table["name"] == table_name:
                        for column in table["columns"]:
                            column_metadata = create_metadata_dict(column)
                            # Creates a dictionary with column names and their metadata,
                            # for example: {column_name: {metadata}}
                            columns_dict_metadata.update(
                                {column["name"]: column_metadata}
                            )

            elif self.resource_type == DBTResourceType.MODEL.value:
                for column in content["columns"]:
                    column_metadata = create_metadata_dict(column)
                    # Creates a dictionary with column names and their metadata,
                    # for example: {column_name: {metadata}}
                    columns_dict_metadata.update({column["name"]: column_metadata})

        return columns_dict_metadata

    def coherence_scan(
        self,
        table_name: str,
        schema_name: str | None = None,
        env: str | None = None,
    ) -> tuple[dict[str, str], dict[str, ModelColumnsMetadata], dict[str, str]]:
        """Get differences between the model metadata in the YAML file and the database.

        Args:
            table_name (str): Name of the table to compare.
            schema_name (Optional[str], optional): Name of the schema.
                Required when scanning source. Defaults to None.
            env (Optional[str], optional): The name of the environment.
                Defaults to None.

        Returns:
            Tuple[dict[str, str], dict[str, ModelColumnsMetadata], dict[str, str]]:
                A tuple containing three dictionaries:
                    1. diff (dict[str, str]): A dictionary containing
                        differences between database columns and YAML columns,
                        or False if no differences are found.
                    2. yaml_columns_metadata (dict[str, ModelColumnsMetadata]):
                        A dictionary containing columns and their metadata
                        from the YAML file.
                    3. db_columns (dict[str, str]): A dictionary representing columns
                        from the database.

        """
        yaml_columns_metadata = self.get_yaml_table_columns(table_name=table_name)

        db_columns = get_db_table_columns(
            schema_name=schema_name, table_name=table_name, env=env
        )

        # Normalize the dictionary in order to compare to the metadata retrieved
        # from the database.
        yaml_columns = {
            col: meta["data_type"] for col, meta in yaml_columns_metadata.items()
        }
        diff = dict_diff(db_columns, yaml_columns)

        return diff, yaml_columns_metadata, db_columns

    def add_column(
        self,
        table_name: str,
        column_name: str,
        index: int,
        data_type: str,
        description: str = "",
        tags: list[str] = [],
        quote: bool = True,
        tests: list[str] | None = None,
    ) -> None:
        """Add a new column to a model in a YAML file.

        Args:
            table_name (str): Name of the table to which the column will be added.
            column_name (str): Name of the new column.
            index (int): Index at which the new column will be inserted.
            data_type (str): Data type of the new column.
            description (str, optional): Description for the new column.
                Defaults to "".
            tags (list[str], optional): Tags associated with the new column.
                Defaults to [].
            quote (bool, optional): Whether the name of the column should be quoted.
                Defaults to True.
            tests (list[str] or None, optional): List of tests associated
                with the column. Defaults to None.

        """
        metadata = {
            "name": column_name,
            "quote": quote,
            "data_type": data_type,
            "description": description,
            "tags": tags,
        }

        # Do not add the "tests" key at all if tests are not specified.
        if tests:
            metadata.update({"tests": tests})

        for content in self[self.resource_type]:
            if self.resource_type == DBTResourceType.SOURCE.value:
                for table in content["tables"]:
                    if table["name"] == table_name:
                        table["columns"].insert(index, metadata)
            elif self.resource_type == DBTResourceType.MODEL.value:
                content["columns"].insert(index, metadata)

        self.set_yaml_content()

    def delete_column(
        self,
        table_name: str,
        column_name: str,
    ) -> None:
        """Delete a column from a table in the YAML file.

        Args:
            table_name (str): Name of the table from which the column will be deleted.
            column_name (str): Name of the column to be deleted.

        """
        for content in self[self.resource_type]:
            if self.resource_type == DBTResourceType.SOURCE.value:
                for table in content["tables"]:
                    if table["name"] == table_name:
                        columns = table["columns"]

                        for column in columns:
                            if column["name"] == column_name:
                                columns.remove(column)

            elif self.resource_type == DBTResourceType.MODEL.value:
                for column in content["columns"]:
                    if column["name"] == column_name:
                        content["columns"].remove(column)

        self.set_yaml_content()

    def update_column(
        self,
        table_name: str,
        column_name: str,
        index: int,
        data_type: str,
        description: str,
        tags: list[str],
        quote: bool,
        tests: list[str] | None,
    ) -> None:
        """Update a column in a YAML file.

        Delete the existing column and add a new column in its place.

        Args:
            table_name (str): The name of the table from which the column
                will be updated.
            column_name (str): The name of the column to be updated.
            index (int): The index where the new column should be added.
            data_type (str): The data type of the new column.
            description (str, optional): Description for the new column.
                Defaults to "".
            tags (list[str], optional): Tags associated with the new column.
                Defaults to [].
            quote (bool, optional): Whether the name of the column should be quoted.
                Defaults to True.
            tests (list[str] or None, optional): List of tests associated
                with the column. Defaults to None.

        """
        self.delete_column(
            table_name=table_name,
            column_name=column_name,
        )
        self.add_column(
            table_name=table_name,
            column_name=column_name,
            index=index,
            data_type=data_type,
            description=description,
            tags=tags,
            quote=quote,
            tests=tests,
        )

    def synchronize_columns(
        self,
        diff: dict[str, str],
        yaml_columns: dict[str, ModelColumnsMetadata],
        db_columns: dict[str, str],
        table_name: str,
    ) -> None:
        """Synchronize columns between a YAML schema definition and a database table.

        Args:
            diff (dict[str, str]): Dictionary of column names and data types
                from YAML vs database.
            yaml_columns (dict[str, ModelColumnsMetadata]): Columns and metadata
                from YAML schema.
            db_columns (dict[str, str]): Columns and data types from
                the database schema.
            table_name (str): Name of the table being synchronized.

        """
        db_column_names = list(db_columns.keys())

        for column_name, column_data_type in diff.items():
            db_column_data_type = db_columns.get(column_name)
            # In the database but not in YAML.
            if column_name not in yaml_columns:
                self.add_column(
                    table_name=table_name,
                    column_name=column_name,
                    index=db_column_names.index(column_name),
                    data_type=column_data_type,
                )

            # In the YAML but not in the database.
            elif column_name in yaml_columns and column_name not in db_columns:
                self.delete_column(
                    table_name=table_name,
                    column_name=column_name,
                )

            # Data type has changed.
            elif (
                db_column_data_type is not None
                and db_column_data_type != column_data_type
            ):
                self.update_column(
                    table_name=table_name,
                    column_name=column_name,
                    index=db_column_names.index(column_name),
                    data_type=db_column_data_type,
                    description=yaml_columns[column_name].get("description"),
                    tags=yaml_columns[column_name].get("tags"),
                    quote=yaml_columns[column_name].get("quote"),
                    tests=yaml_columns[column_name].get("tests"),
                )

        # Overwrites `yaml_columns` with the current state of the columns
        # from the YAML file.
        yaml_columns = self.get_yaml_table_columns(table_name=table_name)
        db_columns_list = list(db_columns.keys())
        yaml_columns_list = list(yaml_columns.keys())

        # Reorder columns in the YAML to match the schema in the database.
        if yaml_columns_list != db_columns_list:
            self.set_columns_order(
                desired_order=db_columns_list,
                table_name=table_name,
            )
