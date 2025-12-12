# `nesso`

**Usage**:

```console
$ nesso [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-v, --version`
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `jobs`: Manage ELT jobs.
* `models`: Manage data models.

## `nesso jobs`

**Usage**:

```console
$ nesso jobs [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

## `nesso models`

**Usage**:

```console
$ nesso models [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `base_model`: Manage base models.
* `debug`: Validate project configuration and...
* `init`: Initialize a new nesso project or user.
* `metadata`: Manage model metadata.
* `model`: Manage models.
* `run`: Run model(s).
* `seed`: Manage seeds.
* `setup`: Setup the project.
* `source`: Manage sources.
* `test`: Run tests.
* `update`: Update YAMLs with latest information from the database.

### `nesso models base_model`

**Usage**:

```console
$ nesso models base_model [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `bootstrap`: Generate an empty...
* `bootstrap-yaml`: Bootstrap the YAML file for a base model.
* `rm`: Remove a base model (YAML and optionally...

#### `nesso models base_model bootstrap`

Generate an empty [bright_black]{silver_schema}/{base_model_name}/{base_model_name}.sql[/] file.

If silver schema prefix is not specified at the beginning of the model name, it
will be added automatically.

**Usage**:

```console
$ nesso models base_model bootstrap [OPTIONS] BASE_MODEL_NAME
```

**Arguments**:

* `BASE_MODEL_NAME`: The name of the base model.  [required]

**Options**:

* `-s, --silver-schema TEXT`: The silver schema to use for the base model.  [default: intermediate]
* `--help`: Show this message and exit.

#### `nesso models base_model bootstrap-yaml`

Bootstrap the YAML file for a base model.

If `silver_schema_prefix` is not specified at the beginning of the base_model_name,
it will be added automatically.

**Usage**:

```console
$ nesso models base_model bootstrap-yaml [OPTIONS] BASE_MODEL_NAME
```

**Arguments**:

* `BASE_MODEL_NAME`: The name of the base model.  [required]

**Options**:

* `-s, --silver-schema TEXT`: The silver schema to use for the base model.  [default: intermediate]
* `-e, --env TEXT`: The environment to use.  [default: dev]
* `--help`: Show this message and exit.

#### `nesso models base_model rm`

Remove a base model (YAML and optionally the relation).

**Usage**:

```console
$ nesso models base_model rm [OPTIONS] NAME
```

**Arguments**:

* `NAME`: The name of the base model to remove.  [required]

**Options**:

* `-s, --silver-schema TEXT`: The silver schema where the base model is located.  [default: intermediate]
* `-r, --relation`: Whether to remove the model's relation as well.
* `-e, --env TEXT`: The environment to use.  [default: dev]
* `--help`: Show this message and exit.

### `nesso models debug`

Validate project configuration and database connectivity.

**Usage**:

```console
$ nesso models debug [OPTIONS]
```

**Options**:

* `-e, --env TEXT`: The environment to use.  [default: dev]
* `--help`: Show this message and exit.

### `nesso models init`

**Usage**:

```console
$ nesso models init [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `project`: Initialize a new nesso-models project.
* `user`: Create a user config and install any...

#### `nesso models init project`

Initialize a new nesso-models project. :rocket:

-----------------------------------------

Create a new project directory with the following structure:

<project_name>
├── .gitignore  # Git config file.
|── .luma  # (optional) Luma Data Catalog config file.
├── .nesso
│   └── config.yml  # Project config file.
├── dbt_project.yml  # Project config file.
├── models
│   ├── <silver_schema>  # Silver schema models.
│   ├── <gold_layer>  # Gold layer models.
│   └── sources
│       └── <bronze_schema>  # Bronze tables.
│           └── <bronze_schema>.yml  # Bronze table metadata.
├── packages.yml  # Internal project dependencies.
├── prepare.sh  # A helper installation script.
├── profiles.yml.example  # Example dbt profiles.yml.
├── README.md  # Template project README.
└── requirements.txt  # nesso-cli version used by the project.

Args:
    project_name (Annotated[str, typer.Option], optional): The name of the project.
    db_type (Annotated[str, typer.Option], optional): The database type that
        the project will connect to.
    db_kwargs (Annotated[str, typer.Option], optional): JSON-encoded parameters to
        pass to the database config. For example, `'{"host": "localhost"}'`.
    data_architecture (Annotated[str, typer.Option], optional): The data
        architecture to use.
    bronze_schema (Annotated[str, typer.Option], optional): The schema where
        raw data is ingested ("input schema").
    silver_schema (Annotated[str, typer.Option], optional): The intermediate
        schema between raw data and user-facing models.
    silver_schema_prefix (Annotated[str, typer.Option], optional): The prefix to use
        for models in the silver schema.
    gold_layer_name (Annotated[str, typer.Option], optional): The name of the gold
        layer.
    luma (Annotated[bool, typer.Option], optional): Whether to enable Luma Data
        Catalog integration.
    snakecase_columns (Annotated[bool, typer.Option], optional): Whether to
        standardize column names to snakecase.
    no_install_dependencies (Annotated[bool, typer.Option], optional): Whether to
        skip installing project dependencies.

**Usage**:

```console
$ nesso models init project [OPTIONS]
```

**Options**:

* `-p, --project-name TEXT`: [default: postgres]
* `-t, --database-type [trino|postgres|redshift|databricks|sqlserver|duckdb]`: [default: postgres]
* `-k, --db-kwargs TEXT`: The parameters to pass to the database config
* `-d, --data-architecture [marts|medallion]`: [default: marts]
* `-b, --bronze-schema TEXT`: [default: staging]
* `-s, --silver-schema TEXT`: [default: intermediate]
* `-sp, --silver-schema-prefix TEXT`: [default: int]
* `-g, --gold-layer-name TEXT`: [default: marts]
* `-l, --luma`: [default: True]
* `-sc, --snakecase_columns`: [default: True]
* `--no-install-dependencies`
* `--help`: Show this message and exit.

#### `nesso models init user`

Create a user config and install any necessary packages.

kwargs (dict): Keyword arguments to pass to `_generate_user_profile()`.

**Usage**:

```console
$ nesso models init user [OPTIONS]
```

**Options**:

* `-p, --profiles-path TEXT`: [default: ~/.dbt/profiles.yml]
* `--no-install-dependencies`
* `--help`: Show this message and exit.

### `nesso models metadata`

**Usage**:

```console
$ nesso models metadata [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `generate`: Generate metadata for the project.

#### `nesso models metadata generate`

Generate metadata for the project.

**Usage**:

```console
$ nesso models metadata generate [OPTIONS]
```

**Options**:

* `-s, --select TEXT`: The model(s) to select.
* `--help`: Show this message and exit.

### `nesso models model`

**Usage**:

```console
$ nesso models model [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `bootstrap`: Generate an empty...
* `bootstrap-yaml`: Bootstrap the YAML file for a particular...

#### `nesso models model bootstrap`

Generate an empty models/<MODEL_NAME>/<MODEL_NAME>.sql file.

**Usage**:

```console
$ nesso models model bootstrap [OPTIONS] MODEL
```

**Arguments**:

* `MODEL`: The name of the model.  [required]

**Options**:

* `-s, --subdir TEXT`: Subdirectory inside the gold layer where the model should be located.
* `--help`: Show this message and exit.

#### `nesso models model bootstrap-yaml`

Bootstrap the YAML file for a particular model.

**Usage**:

```console
$ nesso models model bootstrap-yaml [OPTIONS] MODEL
```

**Arguments**:

* `MODEL`: The name of the model.  [required]

**Options**:

* `-e, --env TEXT`: The environment to use.  [default: dev]
* `--help`: Show this message and exit.

### `nesso models run`

Run model(s).

**Usage**:

```console
$ nesso models run [OPTIONS]
```

**Options**:

* `-s, --select TEXT`: The model(s) to select.
* `-e, --env TEXT`: The environment to use.  [default: dev]
* `--help`: Show this message and exit.

### `nesso models seed`

**Usage**:

```console
$ nesso models seed [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `register`: Add an entry for the seed in seed schema...

#### `nesso models seed register`

Add an entry for the seed in seed schema and, if needed, materialize it.

**Usage**:

```console
$ nesso models seed register [OPTIONS] SEED
```

**Arguments**:

* `SEED`: The name of the seed to register.  [required]

**Options**:

* `-t, --technical-owner TEXT`: The technical owner of this dataset.
* `-b, --business-owner TEXT`: The business owner of this dataset.
* `--yaml-path TEXT`: The absolute path of the schema file to which to append seed schema,
by default PROJECT_DIR/seeds/schema.yml
* `-e, --env TEXT`: The environment to use.  [default: dev]
* `-f, --force`: Whether to overwrite the seed metadata
if it's is already present in the schema YAML.
* `--help`: Show this message and exit.

### `nesso models setup`

Setup the project. Also useful for creating a fresh environment.

Clean up the folders specified in `dbt_project.yml` and pull project dependencies
specified in `packages.yml`.

**Usage**:

```console
$ nesso models setup [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `nesso models source`

**Usage**:

```console
$ nesso models source [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add`: Add a new table to a source schema and...
* `create`: Add a new source schema with all existing...
* `freshness`: Validate the freshness of source table(s).
* `rm`: Remove a source table from the schema YAML.

#### `nesso models source add`

Add a new table to a source schema and materializes it as a base model.

**Usage**:

```console
$ nesso models source add [OPTIONS] TABLE_NAME
```

**Arguments**:

* `TABLE_NAME`: The name of the table to add.  [required]

**Options**:

* `-c, --case-sensitive-cols`: Whether the column names are case-sensitive.  [default: True]
* `-np, --no-profile`: Whether to document data profiling information.  [default: True]
* `-p, --project TEXT`: The name of the project to use.  [default: postgres]
* `-e, --env TEXT`: The environment to use.  [default: dev]
* `-ni, --non-interactive`: Whether to execute the command without interactive prompts.
* `--help`: Show this message and exit.

#### `nesso models source create`

Add a new source schema with all existing tables in it.

**Usage**:

```console
$ nesso models source create [OPTIONS] SOURCE
```

**Arguments**:

* `SOURCE`: The name of the source schema.  [required]

**Options**:

* `--schema-path TEXT`: The path to the source YAML.
Defaults to `{PROJECT_DIR}/models/sources/{source}.yml`.
* `-c, --case-sensitive-cols`: Whether the column names of the source are case-sensitive.  [default: True]
* `-np, --no-profile`: Whether to skip table profiling.  [default: True]
* `-e, --env TEXT`: The environment to use.  [default: dev]
* `-p, --project TEXT`: The name of the project to use.  [default: postgres]
* `-f, --force`: Overwrite the existing source.
* `--help`: Show this message and exit.

#### `nesso models source freshness`

Validate the freshness of source table(s).

**Usage**:

```console
$ nesso models source freshness [OPTIONS]
```

**Options**:

* `-s, --select TEXT`: The source(s) to select.
* `-e, --env TEXT`: The environment to use.  [default: dev]
* `--help`: Show this message and exit.

#### `nesso models source rm`

Remove a source table from the schema YAML.

**Usage**:

```console
$ nesso models source rm [OPTIONS] TABLE_NAME
```

**Arguments**:

* `TABLE_NAME`: The name of the table to add.  [required]

**Options**:

* `-b, --remove-base-model`: Whether to remove the corresponding base model.
* `-e, --env TEXT`: The environment to use.  [default: dev]
* `--help`: Show this message and exit.

### `nesso models test`

Run tests.

**Usage**:

```console
$ nesso models test [OPTIONS]
```

**Options**:

* `-s, --select TEXT`: The model(s) to select.
* `-e, --env TEXT`: The environment to use.  [default: dev]
* `--help`: Show this message and exit.

### `nesso models update`

**Usage**:

```console
$ nesso models update [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `base_model`: Updates the base model YAML file.
* `model`: Updates the model YAML file.
* `source`: Updates the source YAML file.

#### `nesso models update base_model`

Updates the base model YAML file.

If silver schema prefix is not specified at the beginning of the model name, it
will be added automatically.

**Usage**:

```console
$ nesso models update base_model [OPTIONS] BASE_MODEL
```

**Arguments**:

* `BASE_MODEL`: The name of the base_model to update.  [required]

**Options**:

* `-e, --env TEXT`: The environment to use.  [default: dev]
* `--help`: Show this message and exit.

#### `nesso models update model`

Updates the model YAML file.

**Usage**:

```console
$ nesso models update model [OPTIONS] MODEL
```

**Arguments**:

* `MODEL`: The name of the model to update.  [required]

**Options**:

* `-e, --env TEXT`: The environment to use.  [default: dev]
* `--help`: Show this message and exit.

#### `nesso models update source`

Updates the source YAML file.

**Usage**:

```console
$ nesso models update source [OPTIONS] TABLE_NAME
```

**Arguments**:

* `TABLE_NAME`: The name of the table to update.  [required]

**Options**:

* `-s, --schema TEXT`: The schema where the table is located.  [default: staging]
* `-e, --env TEXT`: The environment to use.  [default: dev]
* `--help`: Show this message and exit.
