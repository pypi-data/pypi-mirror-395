# Introduction

This guide provides an overview of the `nesso models` CLI tool and its capabilities. 

Using an example project, we will walk you through the main features of the tool and how to use them. Upon finishing the guide, you will be equipped with all the necessary knowledge to use `nesso models` to create and manage your data models.

The example assumes we have a pre-existing database with a `staging` schema, which contains exactly one table, `contact`.

We will assume the data warehouse/lakehouse we're connecting to utilizes a [marts structure](../reference/glossary.md#data-architectures).

!!! note "Working with the CLI"
    Documentation for all CLI commands and options can be found by adding `--help` to the command, eg. `nesso source add --help`.

    This information can also be obtained in the [API reference](../reference/reference.md).

## Creating a project

To create a new project with `nesso models`, simply execute

```bash
nesso models init project
```

You will be guided through a series of prompts to specify the project's configuration.

For the purposes of this guide, let's assume we specified `duckdb` as the database type, using default values for all other options.

## Onboarding to an existing project

Once a project is created, users can start interacting with it.

{%
    include-markdown "../../src/nesso_cli/models/templates/README.md"
    start="<!-- getting-started-begin -->"
    end="<!-- getting-started-end -->"
%}

The prompts differ depending on the database used by the project. For example, for a DuckDB-based project, you will only be asked for the user schema to use for local development. A common way to name such schema is `dbt_<user>`, eg. `dbt_jdoe`.

## Next steps

With this, you're ready to start using `nesso models` to create your first data models!

Move on to the [next section](./sources.md) to learn how to add data sources to your project.

!!! note  "Managing sources"
    Managing sources is typically done by Data Engineers. If you're a Data Analyst or Data Scientist, you might want to skip to the [data modelling section](./models.md) to learn how to create data models.
