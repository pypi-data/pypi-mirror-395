# Sources

Below are examples showing how to create and manage [sources](../reference/glossary.md#source) and [source tables](../reference/glossary.md#source-table) in `nesso models`.

We use the `nesso models source add` command to add source tables.

The command does one (optionally two) things:

- creates an entry in the [source properties file](../reference/glossary.md#property-files)  
- (optionally) creates a Markdown file where you can add table description

## Creating a source properties file

The source [properties file](../reference/glossary.md#property-files) is created as part of project setup (`nesso init project`) inside the `models/sources` directory.

## Adding a new source table to source properties

Below we describe the process of adding a new [source table](../reference/glossary.md#source-table) to the source [properties file](../reference/glossary.md#property-files).

!!! note "Best practice"
    While the `nesso models source add` command supports adding multiple sources at once, in production, it's usually better to add each source table separately in order to ensure the quality of the metadata.

Here is our example project structure:

```bash
└── my_first_project
    └── models
        ├── intermediate
        ├── marts
        └── sources
            └── staging
                └── staging.yml
```

In our example project, our database contains a bronze schema named `staging` with a table named `contact`, so we can run the following command:

```bash
nesso models source add contact
```

!!! note "In ELT, E comes before the T"
    Remember that this is strictly a metadata operation: the table must already exist in bronze schema before running `nesso models source add`.

Once finished, the following file structure will be created:

```bash hl_lines="7-8"
└── my_first_project
    └── models
        ├── intermediate
        ├── marts
        └── sources
            └── staging
                ├── docs
                │   └── contact.md
                └── staging.yml
```

`nesso models source add` did a two things here:

- added the source table metadata to `staging.yml`
- created a template Markdown file, `sources/staging/docs/contact.md`, with the description of the table


During the process, the user can manually override the source [properties file](../reference/glossary.md#property-files) and the description Markdown file.

## Next steps

Head over to the [next section](base_models.md) to learn how to create and manage base models in `nesso models`.
