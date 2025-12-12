# Models

A data model is essentially a select statement. Models are defined in `.sql` (code) and `.yml` (metadata) files in the `models` directory. Here, we will describe how to use them with `nesso models`.

## Preparation

Before we begin, let's add another source table and base model to our project.
We now should have the following directory structure:

```bash hl_lines="7-9 15"
└── my_nesso_project
    └── models
        ├── intermediate
        │   ├──int_contact
        │   │   ├── int_contact.sql
        │   │   └── int_contact.yml
        │   └── int_account
        │       ├── int_account.sql
        │       └── int_account.yml
        ├── marts
        └── sources
            └── staging
                ├── docs
                │   ├── contact.md
                │   └── account.md
                └── staging.yml
```

## Bootstrapping

To bootstrap a new model, use the `nesso models model bootstrap` command:

```bash
nesso models model bootstrap account --subdir sales
```

??? note "Remember about --help"
    Remember you can use the `--help` parameter to see the documentation of each command. For example, this is what you can see after running `nesso models model bootstrap --help`:

    ```bash
    Usage: nesso models model bootstrap [OPTIONS] MODEL

    ╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────╮
    │ *    model      TEXT  The name of the model. [required]                                      │
    ╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ --subdir  -s      TEXT  Subdirectory inside the gold layer where the model should be located. [default: None]                                                                                                                                                               │
    │ --help                  Show this message and exit.                                                           │
    ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ```

This will produce an `account.sql` file and related folders, resulting in the following directory structure:

```bash hl_lines="12-13"
└── my_nesso_project
    └── models
        ├── intermediate
        │   ├──int_contact
        │   │   ├── int_contact.sql
        │   │   └── int_contact.yml
        │   └── int_account
        │       ├── int_account.sql
        │       └── int_account.yml
        ├── marts
        │   └── sales
        │       └── account
        │           └── account.sql
        └── sources
            └── staging
                ├── docs
                │   ├── contact.md
                │   └── account.md
                └── staging.yml
```

## Modelling

Now is the time to start writing our model. Paste below query into `account.sql`:

```sql
with account as (

    select * from {{ ref('int_account') }}

),
contact as (

    select * from {{ ref('int_contact') }}

),

final as (

    select
        account."id",
        contact."ContactEMail"
    from account

    inner join contact on contact."Id" = account."id"

)

select * from final
```

As you can see, this model represents a simple join between our two silver layer models, `int_account` and `int_contact`.

## Materialization

Now we can materialize this model (ie. actually create it in our database):

!!! note
    Currently, command `nesso models run -s <model_name>` is included in `bootstrap-yaml` commands, so you can manually materialize model or nesso will do it for you.

```bash
nesso models run -s account
```

!!! warning "Only run your model"
    The `-s` ("s" for "select") flag is used to specify the model(s) to run. In this case, we only want to run the `account` model. Be careful to **always** include this flag - otherwise, all models in the project will be materialized into your schema, which can take a lot of time and space.

This will create the `account` view at `<YOUR_DBT_SCHEMA>.account`, where `<YOUR_DBT_SCHEMA>` is the schema specified during the onboarding (`nesso models init user`) (you can find it with `nesso models debug | grep schema`).

Note that in production, the view will be located in the gold layer schema of your project (in our example project, this would be the `sales` schema).

## Tests

### Basic tests

In order to test a model, we first need to create a `.yml` file for it. Luckily, `nesso` does the heavy lifting for us. Run the following command:

```bash
nesso models model bootstrap-yaml account
```

This will create the following YAML file under `marts/sales/account.yml`:

```yaml
version: 2

models:
  - name: account
    description: ""
    meta:
      owners:
        - type: "Technical owner"
          email: None
        - type: "Business owner"
          email: None
      domains: []
      true_source: []
      SLA: 24 hours
    columns:
      - name: id
        quote: true
        data_type: INTEGER
        description: ""
        tests:
            # - unique
            # - not_null
        tags: []

      - name: ContactEMail
        quote: true
        data_type: CHARACTER VARYING(100)
        description: ""
        tests:
            # - unique
            # - not_null
        tags: []
```

This is the final structure of our project:

```bash
└── my_nesso_project
    └── models
        ├── intermediate
        │   ├── int_account
        │   │   ├── int_account.sql
        │   │   └── int_account.yml
        │   └── int_contact
        │       ├── int_contact.sql
        │       └── int_contact.yml
        ├── marts
        │   └── sales
        │       └── account
        │           ├── account.sql
        │           └── account.yml
        └── sources
            └── staging
                ├── docs
                │   ├── contact.md
                │   └── account.md
                └── staging.yml
```

To add tests to the model, simply uncomment the tests of choice (in most editors, this can be done with the `Ctrl`+`/` keyboard shortcut). If you require more advanced tests, see [Advanced tests](#advanced-tests).

In this example, we've uncommented the `unique` test for the `id` column:

```yaml hl_lines="21"
version: 2

models:
  - name: account
    description: ""
    meta:
      owners:
        - type: "Technical owner"
          email: None
        - type: "Business owner"
          email: None
      domains: []
      true_source: []
      SLA: 24 hours
    columns:
      - name: id
        quote: true
        data_type: INTEGER
        description: ""
        tests:
            - unique
            # - not_null
        tags: []

      - name: ContactEMail
        quote: true
        data_type: CHARACTER VARYING(100)
        description: ""
        tests:
            # - unique
            # - not_null
        tags: []
```

To run tests for this model, execute the following command:

```bash
nesso models test -s account
```

!!! warning "Only test your model"
    Notice we specified the `-s` option here as well.

### Advanced tests

### Available tests

Nesso supports the following tests:

- [builtin dbt tests](https://github.com/calogica/dbt-expectations#available-tests)
- [dbt_utils tests](https://github.com/dbt-labs/dbt-utils#generic-tests)
- [dbt-expectations tests](https://github.com/calogica/dbt-expectations#available-tests)

### How-to

For non-builtin tests, you will need to prefix the name of the test with the name of the package where it's coming from. For example, if you'd like to use the `expect_column_distinct_count_to_equal` test from `dbt-expectations`, you would state it like this:

```yaml
tests:
    - dbt_expectations.expect_column_distinct_count_to_equal:
        value: 10
```

Additionally, as you can see above, some of the tests will take parameters. For example, above test [takes the following parameters](https://github.com/calogica/dbt-expectations#expect_column_distinct_count_to_equal): `value`, `quote_values`, `group_by`, and `row_condition`. However, in this case, only the `value` parameter is required.

See the documentation of the test you're using to see which parameters are available.
