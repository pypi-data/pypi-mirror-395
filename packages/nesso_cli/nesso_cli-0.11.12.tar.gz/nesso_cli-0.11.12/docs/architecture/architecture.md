# Architecture

## Architectural decisions

### Using a prefix for silver layer models

This prefix is used due to dbt not allowing models with the same name (even if they're located in different schemas).

The two solutions to this problem are:

- using a prefix in one of the layers
- separating layers into different projects (dbt [has a two-argument variant of the ref() function](https://docs.getdbt.com/reference/dbt-jinja-functions/ref#two-argument-variant) that supports cross-project references)

We decided to go with the first option, as it's simpler and more intuitive.

### Custom schemas

[By default](https://docs.getdbt.com/docs/build/custom-schemas), dbt uses the convention of `<target_schema>_<specified_schema>` for schemas specified in `dbt_project.yml`. This is quite confusing, hence we utilize a [macro](https://github.com/dyvenia/nesso-cli/blob/main/src/nesso_cli/models/nesso_macros/macros/get_custom_schema.sql) that overrides this behavior. Thanks to this macro, when we specify the schema like so in `dbt_project.yml`:

```yaml
models:
  sales:
    cloud_for_customer:
      schema: sales
```

the models are created in the `sales` schema, rather than eg. `dev_sales`.
