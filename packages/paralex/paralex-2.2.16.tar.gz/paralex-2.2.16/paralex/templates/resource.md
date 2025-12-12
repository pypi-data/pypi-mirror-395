## **{{resource.name}}**

{% if resource.title %}{{resource.title}}{% endif %}
{% if resource.description %}
| {{ resource.description }}
{% endif %}

{% if resource.path %}
- This file is located in `{{ resource.path }}`.
{% endif %}

{% if resource.schema %}
- The identifier column (or `primaryKey`) is `{{ resource.schema.primaryKey }}`
{%+ for key, value in resource.schema.items() if key not in ['fields', 'name', 'primaryKey', 'foreignKeys'] %}
{% if value is sequence and not value is string %}
- `{{ key }}`: {{ "`" + value |join("`, `") + "`"}}
  {% elif value == True %}
- {{ key }}
  {% else %}
- `{{ key }}`: `{{ value }}`
{% endif %}
{% endfor %}

{% if resource.schema.foreignKeys %}

- **Formal relations (foreignKeys)** with other tables:
    {% for relation in resource.schema.foreignKeys %}
    - Each value in column `{{ relation.fields }}` of {{resource.name}} must refer to `{{ 
    relation.reference.fields }}` in table `{{ relation.reference.resource }}` 
    {% endfor %}
{% endif %}

**Columns** defined by `{{ resource.schema.name }}`:

{% for field in resource.schema.fields %}
    {% include 'field.md' %}
  {% endfor %}
{% endif %}




