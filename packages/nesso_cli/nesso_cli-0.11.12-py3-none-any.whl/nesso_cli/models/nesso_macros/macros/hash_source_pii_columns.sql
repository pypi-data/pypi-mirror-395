{%- macro hash_source_pii_columns(dbt_project, schema, table=None) -%}

    {%- set pii_columns = get_source_pii_columns(
        dbt_project=dbt_project, schema=schema, table=table
    ) -%}

    {% for column in pii_columns %}
        {{ hash(column) | indent(4) }} as {{ adapter.quote(column) }},
        {{ "\n" if not loop.last else "\n      " }}
    {%- endfor -%}
    {{ dbt_utils.star(from=source(schema, table), except=pii_columns) | indent(4) | trim }}

{%- endmacro -%}
