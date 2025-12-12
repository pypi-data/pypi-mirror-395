
- **`{{ field.name }}`** {% if field.type %}(`{{ field.type }}`){% endif %}{% if 
  field.title %}: {{ field.title }}{% endif %}{% if field.description +%}. {{ field.
  description }}{% endif %}


    {% if field.constraints %}
     - constraints: {% set constr_language = { "required": "is obligatory",
                                "unique": "must be unique",
                                "minLength": "must have a minimum length of {v}",
                                "maxLength": "must have a maximum length of {v}",
                                "minimum": "must be >= {v}",
                                "maximum": "must be <= {v}",
                                "pattern": "must match the regular expression `{v}`",
                                "enum": "must be one of the values: {v}"} -%}
    a `{{ field.name }}` {% for key, value in field.constraints.items() if value %}
 {% if value is sequence and not value is string -%}
 {% set value = "`" +  value | join("`, `")  + "`" -%}
    {% endif -%}
 {{ constr_language[key].format(v=value) }}{{ "; it " if not loop.last else "." }}
  {% endfor -%}
{% endif %}
{% if field.rdfType +%}
     - `rdfType`: [{{ field.rdfType }}]({{ field.rdfType }})
{% endif %}
{% if field.rdfProperty +%}
     - `rdfProperty`: [{{ field.rdfProperty }}]({{ field.rdfProperty }})
{% endif %}
{%+ for key, value in field.items() if key not in ["name", "type", "title", "constraints", "description", "rdfType", "rdfProperty"] %}
{% if value is sequence and not value is string %}
     - `{{ key }}`: {{ "`" + value |join("`, `") + "`"}}
  {% elif value == True %}
     - {{ key }}
  {% else %}
     - `{{ key }}`: `{{ value }}`
  {% endif %}
  {% endfor %}
