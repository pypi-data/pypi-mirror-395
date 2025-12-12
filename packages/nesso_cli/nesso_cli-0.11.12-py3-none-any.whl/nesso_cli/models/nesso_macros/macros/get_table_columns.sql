{%- macro get_table_columns(schema_name, table_name, database_name=target.database) -%}

    {% set table_relation = api.Relation.create(
                schema=schema_name, identifier=table_name, database=database_name
            ) %}

    {% set columns = adapter.get_columns_in_relation(table_relation) %}


    {% set columns_dict  = {} %}
    {% for column in columns %}
        {% set column_name = column.name %}
        {% set data_type = column.data_type | upper %}
        {% do columns_dict.update({column_name: data_type})%}
    {% endfor %}

    {% if execute %}

        {{ print(columns_dict) }} {% do return(columns_dict) %}

    {% endif %}

{%- endmacro -%}
