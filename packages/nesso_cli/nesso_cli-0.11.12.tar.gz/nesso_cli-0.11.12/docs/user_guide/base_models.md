# Base models

## Creating base models

To create a base model follow the instructions below:
- first, create the necessary directory and SQL file with `nesso models base_model bootstrap`
!!! note
    You will be shown a clickable link to the generated file - use Ctrl+Click to open it in your editor.
- then, edit the SQL file to your liking
- once done, run `nesso models base_model bootstrap-yaml` to generate a [properties file](../reference/glossary.md#property-files) for the model
!!! note
    Similar to `nesso models base_model bootstrap`, you will be shown a clickable link to the generated YAML file. Make sure to open it and add any required metadata!

## Materialization

Except for some special cases, base model materialization should only be specified at the project level.

By default, all silver layer models are materialized as views. There are three main reasons for this:

- to save space
- to decrease computation costs (by limiting the amount of ETL)
- no need to be as performant as user-facing data models

## Next steps

Head over to the [next section](models.md) to learn how to create and manage models.
