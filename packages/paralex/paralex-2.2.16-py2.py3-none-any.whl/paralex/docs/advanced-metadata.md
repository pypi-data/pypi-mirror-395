
# More information and tables

The example above is minimal: a title and name for the package and at least a paradigm table. However, we recommend you add more information. In particular, provide a full text citation specifying how you wish your
dataset to be cited, a list of collaborators following the [frictionless specification](https://specs.frictionlessdata.io/), a license, a DOI identifier. All relevant tables should be listed. 

??? example "Richer metadata example"

    Here is an example with more metadata, and a full list of five tables, including `french_v_cells.csv`, `french_v_features.csv`, `french_v_lexemes.csv`, `french_v_sounds.csv`. The forms table has also been divided into two files:
    
    ```yaml title="paralex-infos.yml"
    title: french Verbal Paradigms
    languages_iso639: 
    - fra
    files:
      cells:
        path: french_v_cells.csv
      features-values:
        path: french_v_features.csv
      forms:
        path:
        - french_v_forms.csv
        - french_v_forms2.csv
      lexemes:
        path: french_v_lexemes.csv
      sounds:
        path: french_v_sounds.csv
    name: french
    citation: AuthorName (2025). french Verbal Paradigms dataset. Online.
    contributors:
    - role: author
      title: AuthorName
    id: http://dx.doi.org/S.179-276.SP
    keywords:
    - french
    - paradigms
    licenses:
    - name: CC-BY-SA-4.0
      path: https://creativecommons.org/licenses/by-sa/4.0/
      title: Creative Commons Attribution Share-Alike 4.0
    version: 1.0.2
    ```

# More files

In presence of documentation files (`readme.md`, `data_sheet.md`) or sources (`sources.md`), one can add more files which are not tables:
    
```yaml title="paralex-infos.yml"
title: french Verbal Paradigms
...
files:
  forms:
    path: french_v_forms.csv
  readme:
    path: readme.md
  sources:
    path: sources.bib
  data_sheet:
    path: data_sheet.md
...
```

See an [example with sources and readme](examples.md#sources).

# Custom columns 

For any columns already defined in the [specification](specs.md), rich metadata is automatically generated, including a column name, title and description, its expected type, and potential constraints. This is written in the `<dataset>.package.json` file. For example, the metadata for the lexeme column from the forms table looks as follows:

```json
{
  "name": "lexeme",
  "type": "string",
  "title": "Reference to a lexeme identifier",
  "description": "Lexeme identifiers must be unique to paradigms.",
  "constraints": {
    "required": true
  },
  "rdfProperty": "https://www.paralex-standard.org/paralex_ontology.xml#lexeme"
}
```

The Paralex standard allows users to define their own custom columns, on top of pre-defined ones. For these columns, very little metadata can be inferred automatically. For example, imagine we have a `consonantal` column in the `sounds` table, coding whether each sound is a consonant or not. Since it is not pre-defined in the standard, the only inferred metadata would be:

```json

{
  "name": "consonantal",
  "type": "any"
}
```

It is possible to inject more detailed metadata by adding a "schema" key under a specific table in the config file. 
The syntax of the schema section follows the `frictionless` standard.


??? example "Injecting frictionless schema info"
    
    ```yaml title="paralex-infos.yml"
    title: french Verbal Paradigms
    languages_iso639: 
    - fra
    files:
    files:
      cells:
        path: french_v_cells.csv
      features-values:
        path: french_v_features.csv
      forms:
        path:
        - french_v_forms.csv
        - french_v_forms2.csv
      lexemes:
        path: french_v_lexemes.csv
      sounds:
        path: french_v_sounds.csv
        schema:
          fields:
          - constraints:
              required: true
            description: Binary feature (1/0) indicating whether the segment is a consonant
            falseValues:
            - '0'
            name: consonantal
            title: Whether the segment is a consonant
            trueValues:
            - '1'
            type: boolean
    name: french
    citation: AuthorName (2025). french Verbal Paradigms dataset. Online.
    contributors:
    - role: author
      title: AuthorName
    id: http://dx.doi.org/S.179-276.SP
    keywords:
    - french
    - paradigms
    licenses:
    - name: CC-BY-SA-4.0
      path: https://creativecommons.org/licenses/by-sa/4.0/
      title: Creative Commons Attribution Share-Alike 4.0
    version: 1.0.2
    ```
    
To find the definitions and format of the column metadata, see the [fields descriptors](https://specs.frictionlessdata.io/table-schema/#field-descriptors) in the Frictionless specifications.

# Custom tables

Similarly, some metadata will be missing if using custom tables. In particular, one often needs to specify which column is an **identifier** (or **primary key**), and which columns refer to other ones. This is also done by specifying the schema of these tables in the config file. For example, imagine that in addition to lexemes, we have added a flexeme table, which provides a different partition of forms into paradigms. This is done through a `flexeme` column in the forms table, which refers to identifiers in the `flexeme` table. Thus, we need to add three things in the schemas.

In the forms schema, we need to define the column, as shown above, as well as the foreign key relation to the flexeme table:

```yaml title="excerpt of paralex-infos.yml" 
...
files:
 ...
  forms:
    path:
    - french_v_forms.csv
    - french_v_forms2.csv
    schema:
      foreignKeys:
      - field: flexeme
        reference:
          resource: flexemes
          field: flexeme_id
      fields:
      - name: flexeme
        title: reference to a flexeme identifier
        description: A flexeme to which a form belongs.
        type: string
        constraints:
          required: true
...
```

In the flexeme schema, we define the `flexeme_id` column (we would probably need to define more columns), and declare it as the identifier (primary key):

```yaml title="excerpt of paralex-infos.yml"
...
files:
  ...
  flexemes:
      path: french_v_flexemes.csv
      schema:
        primaryKey: flexeme_id
        fields:
        - name: flexeme_id
          title: identifier for a flexeme
          description: the flexeme id identifies a single flexeme
          type: string
          constraints:
            required: true
...
```


??? example "Rich metadata example with custom tables"
    The entire configuration is starting to get long:
    
    ```yaml title="paralex-infos.yml"
    title: french Verbal Paradigms
    languages_iso639: 
    - fra
    files:
      cells:
        path: french_v_cells.csv
      forms:
        path:
        - french_v_forms.csv
        - french_v_forms2.csv
        schema:
          foreignKeys:
          - field: flexeme
            reference:
              resource: flexemes
              field: flexeme_id
          fields:
          - name: flexeme
            title: reference to a flexeme identifier
            description: A flexeme to which a form belongs.
            type: string
            constraints:
              required: true
      features-values:
        path: french_v_features.csv
      lexemes:
        path: french_v_lexemes.csv
      sounds:
        path: french_v_sounds.csv
        schema:
          fields:
          - name: consonantal
            type: boolean
            title: Whether the segment is a consonant
            description: Binary feature (1/0) indicating whether the segment is a consonant
            trueValues:
            - '1'
            falseValues:
            - '0'
            constraints:
              required: true
      flexemes:
        path: french_v_flexemes.csv
        schema:
          primaryKey: flexeme_id
          fields:
          - name: flexeme_id
            title: identifier for a flexeme
            description: the flexeme id identifies a single flexeme
            type: string
            constraints:
              required: true
    citation: AuthorName (2025). french Verbal Paradigms dataset. Online.
    version: 1.0.2
    keywords:
    - french
    - paradigms
    id: http://dx.doi.org/S.179-276.SP
    contributors:
    - title: AuthorName
      role: author
    licenses:
    - name: CC-BY-SA-4.0
      title: Creative Commons Attribution Share-Alike 4.0
      path: https://creativecommons.org/licenses/by-sa/4.0/
    ```

# More custom manipulations

You can also write your own python script, calling `paralex.paralex_factory`, the argument of which reflect the structure of the config file: first a title, then a dict of tables, then optional arguments name, citation, contributors, id, keywords, licenses and version. The factory returns a `frictionless` `Package` object, which can then be written to disk. This is more flexible, as you can then modify the Package object as you like:
    
```python title="gen-metadata.py"
from paralex import paralex_factory

package = paralex_factory("french Verbal Paradigms", {"forms": {"path": "french_v_forms.csv"}}, languages_iso639=fra)
package.to_json("french.package.json")
```

# Managing paths

The paths to the tables provided in the YAML file or in the JSON file will be resolved as relative to the location of the `.package.json` file. For instance, in the following flat package structure, the path to the `forms` table in `french.yml` would simply be `french_v_forms.csv`:

```yaml
- french_package:
  - french.yml
  - french.package.json
  - french_v_forms.csv
```

In some specific situations, it might be required to explicitly set the location of the package metadata to correctly resolve relative paths. Similarly to `frictionless validate`, `paralex validate` can take an explicit `--basepath` argument:

    paralex validate french.package.json --basepath="french_package"

If the YAML file is stored in a different directory than the JSON file, the `--basepath` argument must also be used when generating the metadata to set the base directory. Relative links will be interpreted with reference to the basepath directory and not to the YAML file.

```yaml
- french_package:
  - french.package.json
  - french_v_forms.csv
  - src:
    - french.yml
```

The command below will use the `/french_package/src/french.yml` to generate the `/french_package/french.package.json` file. In both files, the path to the table is `french/french_v_forms.csv`.

    paralex meta src/french.yml --basepath="."

??? danger "Deprecation of the `basepath` keyword"

    Before version 2.0.0, the standard allowed an optional `basepath` keyword in the YAML file. As this use of `basepath` was not consistent with the frictionless standard, it has been deprecated. Although it is in most cases not necessary, the `--basepath` argument now provides the same results.

