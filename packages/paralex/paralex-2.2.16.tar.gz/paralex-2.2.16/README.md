# Paralex: lexicons of morphological paradigms

[Paralex](https://www.paralex-standard.org) is a standard for morphological lexicons which document inflectional paradigms.

This package contains:
- The paralex specification
- The full documentation
- Utilities to generate metadata and to validate paralex lexicons

# Generating metadata

To generate paralex metadata (more in the docs):


```python title="gen-metadata.py"
from paralex import paralex_factory

package = paralex_factory("Vulcan Verbal Paradigms",
                          {
                              "forms": {"path": "vulcan_v_forms.csv"},
                          }
                          )
package.to_json("vulcan.package.json")
```

The package returned is a [frictionless Package object](https://framework.frictionlessdata.io/docs/framework/package.html) and can be manipulated as such as needed.


# Validation of paralex datasets

To validate a paralex lexicon:

~~~
    paralex validate <mypackagename>.package.json
~~~

This checks that the data is valid using frictionless, as well as a number of statements to match the paralex standard.
For a detailed report on frictionless metadata, do:


~~~
    frictionless validate <mypackagename>.package.json
~~~

# Accessing datasets

Available datasets in the Zenodo community:

~~~
    paralex list
~~~

Download a dataset and extract the .zip archive:

~~~
    paralex get <ZENODO_ID>
~~~

The Zenodo ID can be found with the `paralex list` command.

# Serving the paralex site

First, build the standard package from files:

~~~
	paralex make_standard
~~~

Second, build the specs files from the standard package:

~~~
	paralex make_doc
~~~

Third, use mkdocs (which needs to be installed) to build this site:

~~~
	mkdocs serve
~~~
