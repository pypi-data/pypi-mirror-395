# {% if package.title %}{{ package.title }}{% else %}{{ package.name }}{% endif %}

This is a human-readable rendition of a JSON file defining a frictionless package. It 
was generated automatically.

- `name`: {{ package.name }}
{% if package.licenses %}
- `licenses`: 
{% for lc in  package.licenses %}
    - [{{lc.name}}{% if lc.title %}: {{lc.title}}{% endif %}]({{lc.path}})
{% endfor %}
{% endif %}
{% if package.keywords %}
- `keywords`: {{package.keywords | join(", ")}}
{% endif %}

{{ package | filter_dict(exclude=['name', 'title', 'resources', 'keywords',  'licenses']) | dict_to_markdown }}

This package describes the following files:

{% for resource in package.resources %}
  {% include 'resource.md' %}
{% endfor %}