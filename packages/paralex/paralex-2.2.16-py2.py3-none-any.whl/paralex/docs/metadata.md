
Metadata are any information about the dataset that are not directly part of the data.

General metadata about an entire dataset specify things like:

- Who are the authors
- What is the name of the dataset
- How should it be cited
- What other datasets it is related to or derived from
- What is its identifier (DOI)
- Under what license it is shared
- Relevant keywords

This information is usually provided in introductions or documentation files, in a
way that is easy to understand for humans. To make it
accessible automatically, it needs to be specified more formally. This is
what the `<dataset>.package.json` file in this standard is for (see [frictionless 
metadata](https://frictionlessdata.io/)).

Many other pieces of information are often left implicit, as it is easy for humans, given
enough context, to guess them. However, this is neither future-proof (we will lose
part of the context) nor machine-readable (software is terrible at picking up
informally expressed context). These piece of information are:

- What are the tables present in the dataset ?
- What are the relations between tables ?
- What are the columns present in the tables ?
- What do these columns mean ?
    - This can be documented through linking to specific ontologies and vocabularies.
      Eg. a "glottocode" column may link to language codes in glottolog, a 'UD' column may
      provide cell or feature definitions following the Universal Dependencies
      conventions.
- What should we expect to find in these columns ?
    - For example, what is the type of information present ? one column might only have
      numbers, another text, yet another only has binary true/false values, etc.
    - How are missing data expressed ? What does an empty cell mean ?
    - Are there constraints on these values ? For example, a minimum value for numbers,
       a set of characters used in phonological transcription, values which must be 
      unique to each row, or mandatory.
- Which column serves as identifiers ?
    - Identifiers are unique values which serve to refer unambiguously to a specific row 
      of a specific table.

To record this metadata in a standardised, formal way, we use the
[frictionless standard](https://specs.frictionlessdata.io/data-package/) to write it 
in a json file.
For
example, a json file expressing only information about data contributors might look
like this:

```json
{
  "contributors": [{
    "title": "Joe Bloggs",
    "email": "joe@bloggs.com",
    "path": "http://www.bloggs.com",
    "role": "author"
  }]
}
```

Because there is much more information to specify, metadata tends to be much longer,
and is not practical to write by hand. We provide a python package `paralex` which can
auto-generate metadata for you, because it has information (context !) about standard
tables and columns names. For more on how to use it, see the [tutorial](tutorial.md).
