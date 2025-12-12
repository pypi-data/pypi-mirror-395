# Model maintenance

## Introduction

Model schema may change over time. New columns may be created. Existing columns may be deleted or altered.

Luckily, nesso CLI provides an `update` command which automatically updates a model's YAML file to reflect the current schema of the model in the database.

## Supported operations

!!! info
    Currently, the `update` command only supports updating one model at a time.

The `update` command supports the following schema changes:

- Column addition
- Column removal
- Column renaming
!!! note
    Currently, renaming a column will result in the loss of column metadata (except for data type).
- Data type change

## Example 1 - updating a source table YAML

Below is our example project structure:

```bash
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

Below is the content of the `staging.yml` file:

```yaml
version: 2

sources:
  - name: staging
    schema: staging
    description: ""

    tables:
      - name: contact
        description: |
          {{ doc("staging_contact") }}
        loaded_at_field: _viadot_downloaded_at_utc::timestamp
        freshness:
          warn_after: { count: 24, period: hour }
          error_after: { count: 48, period: hour }
        tags: []
        meta:
          owners:
            - type: Technical owner
              email: admin@example.com
            - type: Business owner
              email: admin2@example.com
          domains: []
          true_source: []
          SLA: "24 hours"
        columns:
          - name: "id"
            quote: true
            data_type: INTEGER
            description: "Customer ID"
            tests:
              - unique
              - not_null
            tags: ["prod"]
          - name: "email"
            quote: true
            data_type: CHARACTER VARYING(100)
            description: "Customer email"
            tests:
              - unique
              - not_null
            tags: ["prod"]

```

Let's assume that after some time, a `phone_number` column was added to `staging.contact`, and the name of the `email` column was changed to `customer_email`.

In this case, we will use `source update` to update the `contact` table in `staging.yml`:

```bash
nesso models update source contact
```

This results in the following `staging.yml`:

```yaml hl_lines="35-46"
version: 2

sources:
  - name: staging
    schema: staging
    description: ''

    tables:
      - name: contact
        description: |
            {{ doc("staging_contact") }}
        loaded_at_field: _viadot_downloaded_at_utc::timestamp
        freshness:
            warn_after: {count: 24, period: hour}
            error_after: {count: 48, period: hour}
        tags: []
        meta:
            owners:
              - type: Technical owner
                email: admin@example.com
              - type: Business owner
                email: admin2@example.com
            domains: []
            true_source: []
            SLA: 24 hours
        columns:
          - name: id
            quote: true
            data_type: INTEGER
            description: Customer ID
            tests:
              - unique
              - not_null
            tags: ["prod"]
          - name: customer_email
            quote: true
            data_type: CHARACTER VARYING(100)
            description: ''
            tests:
            tags: []
          - name: phone_number
            quote: true
            data_type: CHARACTER VARYING(15)
            description: ''
            tests:
            tags: []
```

!!! warning
    Notice that the new column, `customer_email`, did not inherit the metadata (description, tests, and tags) from the `email` column.

## Example 1 - cascading updates from upstream models

In this example, we will look at cascading changes done in the source table down to a base model inheriting the source table's metadata.

Let's assume that we have created a base model based on `staging.contact`:

```bash hl_lines="4-6"
└── my_first_project
    └── models
        ├── intermediate
        │   └── int_contact
        │       ├── int_contact.sql
        │       └── int_contact.yml
        └── sources
            └── staging
                ├── docs
                │   └── contact.md
                └── staging.yml
```

Now, let's assume that we have removed the `phone_number` column from `staging.contact`. How do we update not only the model definition in `staging.yml`, but also in `int_contact.yml`?

Below is how we would go about this with `nesso`:

1. Correct the query in `int_contact.sql` by removing the any references to the `phone_number` column.
2. Update `staging.yml` with `nesso models update source contact`.
3. Update `int_contact.yml` file with `nesso models update base_model int_contact`.
