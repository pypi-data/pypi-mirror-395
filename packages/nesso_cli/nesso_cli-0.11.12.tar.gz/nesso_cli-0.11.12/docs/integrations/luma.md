# Integrating `nesso-cli` projects with Luma

## Introduction

`nesso-cli` generated metadata can be easily ingested into [Luma](https://dyvenia.com/products/luma-data-catalog/).

!!! note "Model & model run metadata"
    Model & model run metadata are ingested using separate commands (`luma dbt ingest` vs `luma dbt send-test-results`).

## Workflows

### Preparation

Before executing luma commands, run below:

```bash
export NESSO_CLI_PROJECT_REPO_PATH=
export LUMA_URL=

cd ${NESSO_CLI_PROJECT_REPO} && git pull
```

### Creating groups

In Luma, [groups](https://github.com/dyvenia/lumaCLI/blob/main/docs/manual/config/groups.md) are custom groupings of metadata items. They can include eg. Department, Domain, etc. They are assigned an icon and are visible on Luma's sidebar.

Creating groups in an optional one-time effort which has to be performed before ingesting any models that reference the custom groups. Follow [luma-cli](https://github.com/dyvenia/lumaCLI/blob/main/docs/manual/config/groups.md)'s documentation on how to specify and ingest groups into your Luma instance. 

Once configured, ingest Luma config files with:

```console
luma config send
```

### Ingesting model metadata

```bash
nesso models metadata generate
luma dbt ingest --metadata-dir target/ --no-config
```

### Ingesting model run metadata

!!! note "Running a subset of models"
    While generating metadata for only a subset of models is not yet supported, the models to execute and test can be filtered with the `-s` flag, eg. `nesso models run -s my_model`, `nesso models run -s intermediate+`, etc.
    For more details, see [the user guide](../user_guide/models.md#materialization).

```bash
nesso models run
nesso models test
luma dbt send-test-results --metadata-dir target/ --no-config
```
