{%- macro hash(field) -%} {{ return(adapter.dispatch("hash", "dbt")(field)) }} {%- endmacro -%}

{%- macro default__hash(field) -%}
    md5(cast({{ adapter.quote(field) }} as {{ api.Column.translate_type("string") }}))
{%- endmacro -%}

{%- macro databricks__hash(field) -%}
    sha2(cast({{ adapter.quote(field) }} as {{ api.Column.translate_type("string") }}), 256)
{%- endmacro -%}

{%- macro sqlserver__hash(field) -%}
    HASHBYTES(
        'SHA2_256', cast({{ adapter.quote(field) }} as {{ api.Column.translate_type("string") }})
    )
{%- endmacro -%}
