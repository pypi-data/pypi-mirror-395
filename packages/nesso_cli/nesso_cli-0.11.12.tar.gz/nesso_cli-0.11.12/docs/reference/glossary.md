# Glossary

Below is a glossary of terms used throughout `nesso` CLI documentation.

## Metadata

We divide model metadata into two categories:

- model metadata  
- model run metadata  

Alternatively, one can think of them as static vs dynamic metadata.

This distinction allows us to utilize the two types in different places of the data product workflow.

Specifically, since model metadata [only changes upon a pull request to the `nesso models` project repository](../user_guide/workflows.md#creating-data-models), it can be ingested into the data catalog as part of the Continuous Integration process in that repository. In other words, the model metadata in the data catalog entry for our model will only be refreshed upon PR approval.

On the other hand, since model run metadata changes each time the model is executed, this metadata does not need be ingested as part of the CI process of the `nesso models` project, but instead is a step in the [model execution workflow](../advanced_usage/scheduling.md#full-workflow). In other words, this metadata is refreshed in the data catalog every time the model is executed (typically, once a day).

### Model metadata

Model/static metadata is the metadata that is defined in the model itself. This includes user-provided properties such as name, description, tags, owner(s), etc., as well as system-generated attributes such as column data types or model lineage.

### Model run metadata

Model run/dynamic metadata type includes metadata generated at the runtime of the model. This mainly includes test and profiling information, but also model execution information such as start time or duration.

## Data architectures

Currently, nesso supports two data architectures:

- data marts
- medallion

Both architectures consist of four storage layers: landing, bronze, silver, and gold. The difference between the two architectures is in the way the data is organized in the gold layer.

### Layers

#### Landing

The landing layer is where the raw, unprocessed data is stored. This layer is typically used for data ingestion, and is not used for data modelling. In nesso, this layer includes raw data files such as CSV, JSON, and parquet.

#### Bronze

Bronze layer is the first layer in the data lakehouse. The goal of this layer is to unify the *format* of the data by converting raw data lake files into data lakehouse* tables.

*Note that [nesso customized](https://nesso.docs.hetzner.dyvenia.lan/architecture/nesso-customized) can utilize a database such as [Azure SQL](https://azure.microsoft.com/en-us/products/azure-sql/database) instead of a data lakehouse. In such case, the data lake files are converted into regular database tables.

!!! note "Lakehouse table formats"
    [nesso SAAS](https://nesso.docs.hetzner.dyvenia.lan/architecture/nesso-saas), [nesso on-prem](https://nesso.docs.hetzner.dyvenia.lan/architecture/nesso-on-prem), as well as [nesso on cloud](https://nesso.docs.hetzner.dyvenia.lan/architecture/nesso-on-cloud) utilize the [Iceberg](https://nesso.docs.hetzner.dyvenia.lan/architecture/components/iceberg/) [table format](https://www.dremio.com/blog/comparison-of-data-lake-table-formats-apache-iceberg-apache-hudi-and-delta-lake/#h-what-is-a-table-format).

    [nesso customized](https://nesso.docs.hetzner.dyvenia.lan/architecture/nesso-customized) supports additional table formats, such Delta and Redshift Spectrum.

Common names for the bronze layer include: `raw`, `bronze`, `staging`.

#### Silver

The silver layer is the middle layer between raw and user-facing data. It stores pre-transformed and pre-aggregated data. It also stores common datasets (used by multiple user-facing datasets).

Common names for the silver layer include: `conformed`, `silver`, `intermediate`.

#### Gold

The gold layer is the user-facing layer. It stores data in a format that is optimized for querying (aggregated, standardized). It is also the layer where the data is organized in a way that is most convenient for the end user. The datasets in this layer are usually well-tested and documented, and SLAs are specified to guarantee their availability to end users.

### Data marts architecture

In the data marts architecture, the gold layer consists of multiple schemas. The schemas are arbitrarily specified by users depending on business need. For example, they commonly refer to business departments, eg. `finance`, `sales`, etc.

As a result, a data modelling project using the data marts architecture will contain a `marts` directory, with each subdirectory representing a schema in the gold layer.

### Medallion architecture

In the medallion architecture, the gold layer consists of a single schema. The name of this schema is configured at the project level. Popular names for this schema include: `analytics`, `operational`, `gold`.

## ELTC

**E**xtract, **L**oad, **T**ransform, **C**atalog. It's an extension of the [ELT](https://en.wikipedia.org/wiki/Extract,_load,_transform) paradigm, with "C" for Catalog. The ELTC process doesn't stop at transforming the data; it also sends metadata about the data to a data catalog.

In nesso, we split the ELTC process into two separate data pipelines: EL and TC. This way, we decouple source data ingestion from data modelling, allowing eg. the same source data to be reused by multiple data models with different scheduling setup.

## Source

The schema containing input data to the nesso models project. In other words, the [bronze layer](#layers) schema.

Metadata describing sources is stored in a source [properties file](#property-files) in the `models/sources` directory.

!!! info
    In nesso, we only use a single source properties file and a single source.

## Source table

A table inside a source. In a nesso models project, we refer to such tables using the `{{ source(<source_name>, <table_name>) }}` [jinja macro](#jinja-macro).

Since we only use a single source - the [bronze schema](#layers) - `source_name` will always be the name of the bronze schema (eg. `staging`).

## Property files

Property files are YAML files used to describe the properties of project resources (seeds, sources, and models). There are four important things to know about these files:

- a property file holds metadata about each resource's properties, such as its name, description, assumptions about the data (in the form of tests), etc.
- a property file describes information *about* the resources, whereas resource configuration provides information on *how to materialize* the resource.

    For example, things such as [materialization](#materialization) type, the schema to use, or database-specific configuration will be provided in resource configuration (either in `dbt_project.yml` or in the model itself via the `config()` [macro](#jinja-macro))

- there are three types of property files, one for each resource type
- we use a single property file for seeds, one for sources, and one property file **per model**. This strikes a balance between having many small files and having few very large, basically human-unreadable files.

## Materialization

A model's materialization describes how the dataset described by the model is stored. The main types of materialization are `table` and `view`.

"To materialize" means to create a representation of a model in the database (in other words, to create a database relation) using one of materialization types.

In `nesso models`, materialization is performed using the `nesso models run` command.

## Registering a seed/source table

To register a source table/seed means to create an entry for it in the relevant [properties file](#property-files).

In the case of seeds, registering also includes [materializing](#materialization) the seed.

## Jinja macro

Jinja is a text templating engine. Its purpose is to allow providing dynamic values inside a text document. This is done by specifying a variable or macro inside a special `{{}}` block inside a file, eg. `{{ my_variable }}`.

The goal of Jinja is to allow creating template text documents. These can by any text files, including standard `.txt`, but also SQL, Python, or Markdown files. Templated files can be reused multiple times with different values, based eg. on user input or configuration.

Jinja macros are a way to specify functions inside jinja templates. In `nesso models`, we utilize jinja macros in several ways:

- templating SQL code (eg `source()` and `ref()` macros)
- automating YAML file generation
- automating new project generation

### Jinja macros in SQL

Let's take the `source()` macro as an example. Imagine we have the following SQL file:

```sql
SELECT * FROM {{ source('staging', 'contact') }}
```

We can see that this file uses a Jinja macro called `source()`, specifying two arguments: `staging` and `contact`. Whenever this SQL file is executed to materialize the model defined in it (ie. when running `nesso models run`), `nesso models` will evaluate the project configuration, and substitute the Jinja block with computed values. In this case, the resulting SQL file (also referred to as ["rendered file"](#rendering)) will look like this:

```sql
SELECT * FROM my_db.staging.contact
```

Notice that we didn't specify `my_db` anywhere in the SQL file. This is because `nesso models` automatically adds the database name to the schema name, based on the project configuration.

Under the hood, `nesso models` the macro also creates a lineage graph of models, adding `staging.contact` as a node to the graph. In other words, using `source()` and `ref()` macros lets `nesso models` create a lineage graph of models.

Thanks to this, the SQL files used in `nesso models` are generic and do not need to be modified when the project configuration (eg. the schema or database name) changes.

## Rendering

In the context of Jinja, rendering refers to the process of evaluating Jinja templates and macros and substituting them with computed values. In `nesso models`, rendering is done automatically when running `nesso models run`. We refer to files which values are evaluated as "rendered files". The power of Jinja is the fact that we can use a single template file to render many different files, depending on specified parameters.
