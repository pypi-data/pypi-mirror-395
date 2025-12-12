{# Adapted from dbt-codegen #}
{# Generate column YAML template #}
{% macro generate_column_yaml(
    column,
    model_yaml,
    columns_metadata_dict,
    parent_column_name="",
    include_pii_tag=True,
    include_data_types=True,
    snakecase_columns=True
) %}
    {{ log("Generating YAML for column '" ~ column.name ~ "'...") }}
    {% if parent_column_name %} {% set column_name = parent_column_name ~ "." ~ column.name %}
    {% else %} {% set column_name = column.name %}
    {% endif %}

    {% set column_metadata_dict = columns_metadata_dict.get(column.name, {}) %}
    {% if include_pii_tag %} {% set tags = column_metadata_dict.get("tags", []) %}
    {% else %}
        {% set tags = column_metadata_dict.get("tags", []) | reject("equalto", "PII") | list %}
    {% endif %}

    {% if snakecase_columns %}
        {% do model_yaml.append("      - name: " ~ adapter.quote(snake_case(column.name))) %}
    {% else %} {% do model_yaml.append("      - name: " ~ adapter.quote(column.name)) %}
    {% endif %}
    {% do model_yaml.append("        quote: true") %}
    {% if include_data_types %}
        {% do model_yaml.append(
            "        data_type: " ~ (column.data_type | upper)
        ) %}
    {% endif %}
    {% do model_yaml.append(
        '        description: "' ~ column_metadata_dict.get("description", "") ~ '"'
    ) %}
    {% do model_yaml.append("        # tests:") %}
    {% do model_yaml.append("          # - unique") %}
    {% do model_yaml.append("          # - not_null") %}
    {% do model_yaml.append("        tags: " ~ tags) %}
    {% do model_yaml.append("") %}

    {% if column.fields | length > 0 %}
        {% for child_column in column.fields %}
            {% set model_yaml = generate_column_yaml(
                child_column,
                model_yaml,
                column_metadata_dict,
                parent_column_name=column_name,
            ) %}
        {% endfor %}
    {% endif %}
    {% do return(model_yaml) %}
{% endmacro %}


{% macro generate_model_yaml(
    model_name,
    technical_owner="None",
    business_owner="None",
    domains=[],
    source_systems=[],
    tags=[],
    upstream_metadata=True,
    include_sla=True,
    include_pii_tag=False,
    include_data_types=True,
    snakecase_columns=True,
    base_model_prefix=none,
    bootstrapped_base_model=False
) %}
    {# 
Generate model YAML template.

Args:
    model_name (str): The name of the model for which to generate the template.
    technical_owner (str, optional): The technical owner of the model.
    business_owner (str, optional): The business owner of the model.
    domains (List[str]): The domains the model belongs to.
    source_systems (List[str]): Sources from which the table originates, e.g., SQL Server, BigQuery, etc.
    tags (List[str]): The tags to attach to the model.
    upstream_metadata (bool, optional): Whether to inherit upstream model metadata.
    include_sla (bool, optional): Whether to include the SLA meta key.
    include_pii_tag (bool, optional): Whether to include the PII tag.
    include_data_types (bool, optional): Whether to include the data types of column.
    This may be useful when PII columns are already masked in the base model.
    snakecase_columns (bool, optional): Whether to standardize upstream column names
        to snakecase in the model.
    base_model_prefix (str, optional): Prefix to apply to the name of the base model.
        Defaults to empty string (no prefix).
    bootstrapped_base_model (bool, optional): Determines whether the base model was built using 
        the `base_model bootstrap` command.
#}  
    
    {# Set to True to enable debugging. #}
    {% set info=False %}

    {{
        log(
            "generate_model_yaml | Generating model YAML for model '"
            ~ model_name
            ~ "'...",
            info=info
        )
    }}

    {% if upstream_metadata %}
        {% set upstream_model_metadata = get_parent_source_or_model_metadata(model_name) %}
        {{
            log(
                "generate_model_yaml | Got upstream model metadata:\n\n"
                ~ upstream_model_metadata
                ~ "\n",
                info=info
            )
        }}
        {# {% set metadata_resolved = resolve_upstream_metadata(upstream_models_metadata) %}
        {{
            log(
                "generate_model_yaml()  | Resolved upstream metadata: \n\n"
                ~ metadata_resolved
                ~ "\n",
                info=info
            )
        }} #}
    {% else %}
        {# {% set metadata_resolved = {} %} #}
        {% set upstream_model_metadata = {} %}
    {% endif %}
    
    
    {% set dependencies = get_model_dependencies(model_name) %}
    {% set upstream_model_type = dependencies["type"] %}

    {% if base_model_prefix is none %}
        {% set base_model_prefix = "" %}
    {% else %}
        {% if base_model_prefix and not base_model_prefix.endswith("_") %}
            {% set base_model_prefix = base_model_prefix ~ "_" %}
        {% endif %}
        {% set model_name = base_model_prefix ~ model_name %}
    {% endif %}

    {{ log("generate_model_yaml | Base model prefix: " ~ base_model_prefix, info=info) }}

    {# Table metadata. #}
    {% set model_yaml = [] %}
    {% do model_yaml.append("version: 2") %}
    {% do model_yaml.append("") %}
    {% do model_yaml.append("models:") %}

    {% do model_yaml.append("  - name: " ~ model_name | lower) %}

    {% if upstream_model_type == "source" %}
        {% do model_yaml.append("    description: Base model of the `" ~ model_name | replace(base_model_prefix, "") ~ "` table.") %}
    {% else %} {% do model_yaml.append('    description: ""') %}
    {% endif %}

    {# {% set tags = metadata_resolved.get("tags", tags) %}

    {% if tags %}
        {% do model_yaml.append('    config:')%}
        {% do model_yaml.append('      tags: ' ~ tags)%}
    {% endif %} #}

    {{ log("generate_model_yaml | Adding meta key...", info=info) }}

    {% do model_yaml.append("    meta:") %}
    {% if upstream_model_metadata %}
        {% set meta = upstream_model_metadata.get("meta", {}) %}
        {# {% set meta = metadata_resolved.get("meta", {}) %} #}
    {% else %} {% set meta = {} %}
    {% endif %}

    {# Extract owners from metadata. #}
    {# Jinja forgets variables defined in loops -- but it has a concept of namespace as a workaround. #}
    {% set ns = namespace(technical_owner=technical_owner, business_owner=business_owner) %} 

    {{ log("generate_model_yaml | Getting owner metadata...", info=info) }}

    {% if (technical_owner == "None" or business_owner == "None") and meta %}

        {% for owner_meta in meta.get("owners") %}
            {% set typ = owner_meta.get("type") %}
            {% set email = owner_meta.get("email") %}

            {% if typ == "Technical owner" %}
                {# {{ print("Setting technical owner to " ~ email)}} #}
                {% if not technical_owner or technical_owner == "None" %}
                    {% set ns.technical_owner = email %}
                {% endif %}
            {% elif typ == "Business owner" %}
                {# {{ print("Setting business owner to " ~ email)}} #}
                {% if not business_owner or business_owner == "None" %}
                    {% set ns.business_owner = email %}
                {% endif %}
            {% endif %}

        {% endfor %}
    {% endif %}

    {% do model_yaml.append("      owners:") %}
    {% do model_yaml.append("        - type: Technical owner") %}
    {% do model_yaml.append("          email: " ~ ns.technical_owner) %}
    {% do model_yaml.append("        - type: Business owner") %}
    {% do model_yaml.append("          email: " ~ ns.business_owner) %}
    {% do model_yaml.append("      domains: " ~ meta.get("domains", domains)) %}
    {% do model_yaml.append("      true_source: " ~ meta.get("true_source", source_systems)) %}

    {% if include_sla %}
        {% do model_yaml.append("      SLA: " ~ meta.get("SLA", "24 hours")) %}
    {% endif %}

    {{ log("generate_model_yaml | Meta key added.", info=info) }}

    {% do model_yaml.append("    columns:") %}

    {# Separates base models created using bootstrap command
     because they can multiple parent sources and models. #}
    {% if upstream_model_type == "source" and not bootstrapped_base_model %}
        {% set schema = dependencies["node"].split(".")[-2] %}
        {% set relation = source(schema, model_name | replace(base_model_prefix, "")) %}
    {% else %} {% set relation = ref(model_name) %}
    {% endif %}

    {{ log("generate_model_yaml| Retrieving the list of columns...", info=info) }}

    {%- set columns = adapter.get_columns_in_relation(relation) -%}

    {# Column metadata. #}
    {% if meta %}
        {{ log("generate_model_yaml | Retrieving column metadata...", info=info) }}
        {% set columns_metadata_dict = (
            get_parent_source_or_model_column_metadata(
                model_name | replace(base_model_prefix, "")
            )
            if upstream_metadata
            else {}
        ) %}
        {{
            log(
                "generate_model_yaml | Successfully retrieved column metadata:\n"
                ~ columns_metadata_dict,
                info=info
            )
        }}
    {% else %} {% set columns_metadata_dict = {} %}
    {% endif %}

    {{ log("generate_model_yaml | Generating column YAML...", info=info) }}
    {% for column in columns %}
        {{ 
            log(
                "generate_model_yaml()  | Generating YAML for column: "
                ~ column,
                info=info
            )
        }}
        {% set model_yaml = generate_column_yaml(
            column,
            model_yaml,
            columns_metadata_dict,
            include_data_types=include_data_types,
            include_pii_tag=False,
            snakecase_columns=True,
        ) %}
        {{ log("generate_model_yaml()  | Generated YAML: " ~ model_yaml, info=info) }}
    {% endfor %}
    {{ log("generate_model_yaml | Successfully generated column YAML.", info=info) }}
 
    {%- if execute -%}

        {%- set joined = model_yaml | join("\n") -%}

        {{ print(joined) }}
        {{ log("generate_model_yaml()  | Final metadata:\n\n" ~ joined, info=info) }}

        {%- do return(joined) -%}

    {%- endif -%}

{%- endmacro -%}


+{% macro resolve_upstream_metadata(metadata) %}
+    {# Set to True to enable logging to console #}
+    {% set info = False %}
+    {# 
+    Merge upstream metadata using the following logic:
+    - fields of type string are taken from the first model in the list
+    - fields of type list are merged together
+    - for dict fields, same rules are applied to their subfields
+    #}
+
+    {{ log("resolve_upstream_metadata()  | Got metadata:\n\n" ~ metadata ~ "\n", info=info) }}
+
+    {% set metadata_resolved = {} %}
+    {% for model_name in metadata %}
+        {{ log("resolve_upstream_metadata()  | Processing model '" ~ model_name ~ "'...", info=info) }}
+        {% set model_metadata = metadata[model_name] %}
+
+        {{ log("resolve_upstream_metadata()  | Got model metadata: \n\n" ~ model_metadata ~ "\n", info=info) }}
+
+        {% for field in model_metadata %}
+            {# Workaround because dbt jinja doesn't have the `continue` loop control. #}
+            {% set continue_tracker = namespace(should_continue = True) %}
+            {% set field_content = model_metadata[field] %}
+            {% if field not in metadata_resolved %}
+                {% do metadata_resolved.update({field: field_content}) %}
+            {% else %}
+                {% if field_content is string %}
+                    {# String - keep the value from the first encountered upstream,
+                    as there's no way to decide which is the correct one. #}
+
+                    {{ log("resolve_upstream_metadata()  | String field found: " ~ field ~ ": " ~ field_content, info=info) }}
+                    
+                    {% set continue_tracker.should_continue = False %}
+                {% elif field_content is mapping and continue_tracker.should_continue %}
+                    {# A dictionary - merge the keys. #}
+
+                    {{ log("resolve_upstream_metadata()  | Dict field found: " ~ field ~ ": " ~ field_content, info=info) }}
+
+                    {% for subfield in field_content %}
+                        {% set subfield_content = field_content[subfield] %}
+                        {% set continue_tracker2 = namespace(should_continue = True) %}
+                        {# Each key in the dictionary can also be a string, 
+                        list, or dict. We apply the same rules as to top-level fields.#}
+                        {% if subfield_content is string %}
+                            {% set continue_tracker2.should_continue = False %}
+                        {% elif subfield_content is mapping and continue_tracker2.should_continue %}
+                            {% do metadata_resolved[field].update({subfield: subfield_content}) %}
+                        {% elif subfield_content is iterable and continue_tracker2.should_continue %}
+                            {% for key in subfield_content %}
+                                {% if key not in metadata_resolved[field][subfield] %}
+                                    {% do metadata_resolved[field][subfield].append(key) %}
+                                {% endif %}
+                            {% endfor %}
+                        {% else %}
+                            {% do metadata_resolved[field].update({subfield: model_metadata[field]}) %}  
+                        {% endif %}
+                    {% endfor %}
+                {% elif field_content is iterable and continue_tracker.should_continue %}
+                    {# A list - append all unique items into the final list. #}
+                    
+                    {{ log("resolve_upstream_metadata()  | List field found: " ~ field ~ ": " ~ field_content, info=info) }}
+
+                    {% for key in field_content %}
+                        {% if key not in metadata_resolved[field] %}
+                            {% do metadata_resolved[field].append(key) %}
+                        {% endif %}
+                    {% endfor %}
+                {% else %}
+                    {% do metadata_resolved.update({field: model_metadata[field]}) %}                
+                {% endif %}
+            {% endif %}
+        {% endfor %}
+    {% endfor %}
+
+    {{ log("resolve_upstream_metadata()  | Resolved metadata:\n\n" ~ metadata_resolved ~ "\n", info=info) }}
+
+    {% do return(metadata_resolved) %}
+
+{% endmacro %}