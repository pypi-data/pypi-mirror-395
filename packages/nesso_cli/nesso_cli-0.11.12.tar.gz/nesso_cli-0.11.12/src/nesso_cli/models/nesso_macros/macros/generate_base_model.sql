{% macro generate_base_model(
    source_name, table_name, dbt_project, snakecase_columns=False, leading_commas=False
) %}

    {%- set source_relation = source(source_name, table_name) -%}

    {%- set columns = adapter.get_columns_in_relation(source_relation) -%}
    {%- set column_names = columns | map(attribute="name") -%}

    {%- set base_model_sql -%}
with _masked as (
    select {{ '\n      ' ~ hash_source_pii_columns(table=table_name, schema=source_name, dbt_project=dbt_project ) | trim }}
    from {{ "{{ source(" ~ '"' ~ source_name ~ '"' ~ ", " ~ '"' ~ table_name ~ '"' ~ ") }}" }}
),

renamed as (
    select
    {%- if leading_commas -%}
        {%- for column in column_names %}
            {{", " if not loop.first}}
            {% if snakecase_columns %}
                {{ adapter.quote(column) ~ ' as ' ~ adapter.quote(snake_case(column)) }}
            {% else %}
                {{ adapter.quote(column) }}
            {% endif %}
        {%- endfor %}
    {% else %}
        {% for column in column_names %}
            {%- if snakecase_columns -%}
                {{ adapter.quote(column) ~ ' as ' ~ adapter.quote(snake_case(column)) }}
            {%- else -%}
                {{ adapter.quote(column) }}
            {%- endif -%}
            {{"," if not loop.last}}
        {% endfor %}
    {%- endif %}
    from _masked
)

select * from renamed
    {%- endset -%}

    {% if execute %} {{ print(base_model_sql) }} {% do return(base_model_sql) %} {% endif %}

{% endmacro %}
