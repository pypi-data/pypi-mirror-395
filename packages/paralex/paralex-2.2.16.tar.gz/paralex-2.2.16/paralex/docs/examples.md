Although the standard specifies how to handle many complex case, at its core, it only requires very little.
This page demonstrates some examples of small, minimal valid paralex packages.

# Minimal dataset

This example does only the very minimum to have a valid paralex dataset

!!! example

    === "readme.md"
        
        {% include "examples/minimal/readme.md" %}

    === "Forms Table"
        
        ~~~ csv title="forms.csv"
        {% include "examples/minimal/forms.csv" %}
        ~~~

    === "Metadata: yaml config file"

        ~~~ yaml title="paralex-infos.yml"
        {% include "examples/minimal/paralex-infos.yml" %}
        ~~~

    === "Generated: json metadata"

        File generated automatically by running `paralex meta paralex-infos.yml`

        ~~~ json title="paralex-min-chanter.package.json"
        {% include "examples/minimal/paralex-min-chanter.package.json" %}
        ~~~

# Multi paths

This dataset illustrates the usage of multiple data paths.

!!! example

    === "readme.md"
        
        {% include "examples/multipath/readme.md" %}

    === "Forms Table in two csv files"
        
        ~~~ csv title="forms.csv"
        {% include "examples/multipath/forms.csv" %}
        ~~~

        ~~~ csv title="forms2.csv"
        {% include "examples/multipath/forms2.csv" %}
        ~~~

    === "Metadata: yaml config file"
        ~~~ yaml title="paralex-infos.yml"
        {% include "examples/multipath/paralex-infos.yml" %}
        ~~~

    === "Generated: json metadata"

        File generated automatically by running `paralex meta paralex-infos.yml`

        ~~~ json title="paralex-multipart-chanter.package.json"
        {% include "examples/multipath/paralex-multipart-chanter.package.json" %}
        ~~~

# Sources

This dataset illustrates adding a source file

!!! example

    === "readme.md"
        
        {% include "examples/sources/readme.md" %}

    === "Forms Table"
        
        ~~~ csv title="forms.csv"
        {% include "examples/sources/forms.csv" %}
        ~~~

    === "Sources"
        
        ~~~ bib title="sources.bib"
        {% include "examples/sources/sources.bib" %}
        ~~~

    === "Metadata: yaml config file"

        ~~~ yaml title="paralex-infos.yml"
        {% include "examples/sources/paralex-infos.yml" %}
        ~~~

    === "Generated: json metadata"

        File generated automatically by running `paralex meta paralex-infos.yml`

        ~~~ json title="paralex-sources-chanter.package.json"
        {% include "examples/sources/paralex-sources-chanter.package.json" %}
        ~~~
