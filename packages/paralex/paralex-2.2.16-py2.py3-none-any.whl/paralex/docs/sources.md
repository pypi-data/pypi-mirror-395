
## How should sources be credited ?

We recommend crediting sources at every level. This should be indicated as relevant:

- for relations which affect all or a large part of the data:
    - In the metadata, using [`related_identifiers`](standard.md#Relation_to_other_work).
    - In the README.md or accompanying documentation, by stating explicitly this relation
- for relations which affect only some rows:
    - In the data itself, using the `source` columns, with identifiers which refer to the original 
    resource
    - By providing a bibtex file containing entries for each academic source. The `source` columns can then directly refer to the bibtex keys.

## How should I link to other resources ?

To maximise interoperability, we recommend to systematically link to other resources 
insofar as possible. This can usually be done with using identifiers from the other resources, whether tabular data, corpora, or other.

In particular, it is strongly recommended to use standard vocabularies for things like languages ([glottocodes](https://glottolog.org/) or [iso codes](https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes)
  ), cells and features ([universal dependencies](https://universaldependencies.org/u/overview/morphology.html), [unimorph schema](https://unimorph.github.io/schema/),  [leipzig glossing rules](https://www.eva.mpg.de/lingua/pdf/Glossing-Rules.pdf)), phonemes ([IPA](https://www.internationalphoneticassociation.org/content/full-ipa-chart), [BIPA](https://clts.clld.org/contributions/bipa)), etc. In the [CLDF standard](https://cldf.clld.org/), this corresponds to the third design principle: "*If entities can be referenced, e.g. languages through their Glottocode, this should be done rather than duplicating information like language names.*". 

In the cases where controlled vocabularies imperfectly cover your needs, it is very 
useful to document the choices made in the README.md or accompanying documentation. 
For example, when no glottocode was exactly correct, was the closest code used instead 
? Or was the value left empty ?
