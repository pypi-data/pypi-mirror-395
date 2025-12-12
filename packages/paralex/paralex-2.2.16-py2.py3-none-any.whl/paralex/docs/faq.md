## What size should a lexicon be ?

The standard does not impose constraints on the size of the lexicon. The number of 
cells is dependent on the language and the analysis. The number of lexemes is dependent on the
language, part of speech, and available documentation. The number of forms in the end
is roughly the product of the number of cells and lexemes (though overabundance,
defective, and other variations can have an impact on this). The more lexemes
documented the better. In less documented languages, it might be useful to create a
lexicon with less than 100 lexemes, or a few hundred. In well-documented languages,
one might aim for a few thousand. Above this, it is useful to use frequency information to filter out or annotate very rare lexemes.

## Is it necessary to include all the information described in the standard?

Minimally, a valid paralex lexicon includes a `forms` table with just a few columns: `form_id`, `lexeme`, `cell`, and either `phon_form` or `orth_form`; as well as a `.package.json` metadata file. Adding tables for `sounds`, `cells` and `feature-values` is highly recommended in order to make the conventions used in the forms table explicit.

Furthermore, the standard provides optional ways to encode much richer lexicons (accounting for variation, overabundance, defectivity, frequency information, inflection classes, etc.).


## How should one choose a license ?

In choosing licenses, be very careful of respecting existing licenses of material used,
and to respect the [CARE](https://www.gida-global.org/care) principles where relevant. 
When possible, we recommend the usage of open licenses. Some tools exist to help 
choose a specific license, for example [choose a license . com](https://choosealicense.
com/), or the [Creative commons license chooser](https://creativecommons.org/choose/).

## Is it necessary to write python code to use the standard ?

To follow this standard, a dataset only needs to use frictionless metadata (the 
`package.json` file), fit the obligations in the [standard](standard.md) and use the 
[specifications](specs.md). One could perfectly well use other tools and programming 
languages to do this, relying on the default [`paralex.package.json`](https://gitlab.com/sbeniamine/paralex/-/blob/main/paralex/standard/paralex.package.json) which defines 
the standard specifications. 

Writing the metadata `json` file by hand is not a good solution: it is very boring, not a 
very human friendly format, and very easy to make mistakes. Thus, we provide a python package to help out.

We understand that not all dataset creators have someone in their team with the 
relevant expertise to make use of the python package. However, at the end of projects, it 
is common to contract web developers to create a showcase site for the dataset. Our 
suggestion is to use some of this budget to hire someone to do the (very little) 
coding, validation, and writing of tests for the data.

## What is a word ?

Rows of the `forms` table document word forms. But what is a word ? Do clitic 
pronouns, pre-verbs, converbs, etc. belong in the paradigm ? Again, this is a 
matter of analysis, and different choices might be valid for a same set of data. 
Dataset authors are responsible for these analytic choices, and should document them 
explicitly.

If choosing an extensive approach (eg. including material which other analyses might 
separate from the word), we recommend making use of the `segmented_orth_form` and 
`segmented_phon_form` or custom columns to mark the boundaries, making it possible for 
data users to filter them out as needed.

## How can I add notes or comments ?


In most tables, the standard specifies a "comments" column, which lets data creator 
provide full text, human-readable notes. However, these notes are not usable 
computationally. 

Whenever possible, we recommend to tease out any systematic comments using either tags 
(see details in the standard about the [forms table](standard.md/#forms), the [tags 
table](standard.md/#tags), and the [specs for tags](specs.md/#tags)) or separate, ad-hoc 
columns. This provides a more systematic set of annotation, which increases the value 
of the dataset and is useful in order to filter data. It facilitates selecting 
relevant slices of data for the purpose of future studies, as well as creating derived 
datasets.

It is **best to use tags** any time several forms are part of a series and would have 
the same comment. This includes rare forms, information about data quality, 
uncertainty and epistemic status, variations (for example dialectal, or register), 
types of defectivity (eg. pluralia tantum), etc. Tags can also be used in order to 
carry annotations present in the original source, for example  all forms marked with "?" 
in a dictionary could be tagged as `doubtful_in_source`.

The **comment column** should be used mostly for clarifications, notes on choices made for a specific row 
or for short notes about data treatment.

It is **best to use separate columns** in all other cases, such as reporting comments 
from sources, relating one entry to its sources (see 
how 
to handle [sources](standard.md/#sources)), or to entries in other databases (which should be 
linked using URIs and identifiers).

## How to code paradigm structure ?

Paradigm structures are analyses, and dataset authors have freedom in how they want to
formulate this analysis. Among the main problems are:

1. What is the inventory of paradigm cells ?
2. How should each cell be characterised?
3. What counts as a lexeme ?

### What is the inventory of paradigm cells ?

Data creators can provide labels of their choice, but
should use a cells and features table to document the meaning of these labels, and map
from these labels to existing standards and conventions.

### How should each cell be characterised ?

For long term usability, it is important to
account for paradigm structure choices in the documentation. A particularly tricky
case is that of overdifferentiation. For example, in English, one might want to
expand the
person/number combinations of verbs to match pronouns and define the paradigm of verbs
such as:

|                            | Present        | Preterite     |
|----------------------------|----------------|---------------|
| **first person singular**  | I eat          | I ate         |
| **second person singular** | you eat        | you ate       |
| **third person singular**  | he/she/it eats | he/she/it ate |  
| **first person plural**    | we eat         | we ate        |
| **second person plural**   | you eat        | you ate       |
| **third person plural**    | they eat       | they ate      |

| Imperative | Present participle | Past participle | Infinitive |
|------------|--------------------|-----------------|------------| 
| eat        | eating             | eaten           | to eat     |

However, for most verbs, it would be sufficient to stipulate:

| cell               | form   |
|--------------------|--------|
| present 3 singular | eats   |
| present others     | eat    |
| preterite          | ate    |
| past participle    | eaten  |
| present participle | eating |

This choice unfortunately has the consequence of requiring extra cells only for the
verb to be:

| cell                   | form  |
|------------------------|-------|
| present 1 singular     | am    |
| present 3 singular     | is    |
| present others         | are   |
| preterite 1/3 singular | was   |
| preterite others       | were  |
| past participle        | been  |
| present participle     | being |

We suggest preferring structures which allow for uniform paradigm shapes and
documenting these choices clearly. It is easier for users to go from such annotations
to a more minimal paradigm structure, than to do the opposite. For propositions about 
"morphomic" paradigm structures, see Boyé & Schalchli (2016).


- Boyé, G., & Schalchli, G. (2016). The Status of Paradigms. In A. Hippisley & G. Stump  (Eds.), The Cambridge Handbook of Morphology (Cambridge Handbooks in Language and Linguistics, pp. 206-234). Cambridge: Cambridge University Press. DOI: [10.1017/9781139814720.009](https://doi.org/10.1017/9781139814720.009)

### What should count as a lexeme

The creators of a dataset are free to produce the analysis which they
believe best fit their data. 

In some cases, a lexeme is entirely overabundant because it can take either of
several inflection classes or stems. In other terms, a same *lexeme* could be split in 
several *flexemes* (see Fradin & Kerleroux 2003, Thornton 2018). 

In this case, there are two main solutions:

- Either split these lexemes so that each lexeme identifier corresponds to a single 
  *flexeme*
- Or account for the two levels by maintaining a single lexeme; and adding a *flexeme* 
  table and flexeme identifiers.

**References**:

- Fradin, Bernard & Françoise Kerleroux. 2003. Troubles with lexemes. In Geert Booij, Janet DeCesaris, Angela Ralli & Sergio Scalise (eds.), Selected papers from the third Mediterranean Morphology Meeting, 177–196. Barcelona: IULA – Universitat Pompeu Fabra.
- Anna M. Thornton (2018). Troubles with flexemes. In Olivier Bonami, Gilles Boyé, Georgette Dal, Hélène Giraudo & Fiammetta Namer (eds.), The lexeme in descriptive and theoretical morphology, 303–321. Berlin: Language Science Press. DOI: [10.5281/zenodo.1407011](https://doi.org/10.5281/zenodo.1407011)

## How to code sounds ?

The sounds table documents the set of sounds used in transcription (the `phon_form` 
column of the `forms` table). Although it is best to use common conventions, it is 
often impossible to avoid language specific analytic choices in the sound inventory. 

### Which other databases should one link to in order to define sounds meaning ?

We suggest using valid BIPA (see [CLTS](https://clts.clld.org/)) sounds, providing 
references to CLTS's BIPA or to [PHOIBLE](https://phoible.org/).

### How to manage ambiguous notations ?

There are a variety of situations which lead to ambiguous notations, e.g. where one has a 
symbol "R" which might stand for either the sound "r" or "ɹ". Whenever possible, we 
recommend avoiding ambiguous sounds, as they  reduce the compatibility with other 
transcription systems. When using an ambiguous symbol is the only reasonable choice,
it is crucial to document precisely their meaning and avoid confusions.

Here are some specific cases:

#### Real variation (either free or conditionned)

If the intended meaning of "R" is that some speakers would pronounce "r" and some "ɹ", 
the recommended solution is to use both of these more precise, concrete sounds, 
provide distinct rows in the `forms` table with 
each, and tag them using a `variant` tag. A possible, but less satisfactory 
alternative is to consistently pick a single one (eg "r"), and ignore the variation.

#### Imprecise transcription

Sometimes, the data source gives an imprecise transcription, e.g. "R", but it is 
unclear whether "r" or "ɹ" are meant. This includes cases of reconstruction which are 
intentionally vague, uncertainties in field work data, or ambiguous data points where 
other forms do contain the precise symbol. In this case, 
keeping the imprecise symbol "R" is best. It might be difficult, then, to link it properly to 
other databases. The `label` and `comment` columns should clarify the meaning of the 
ambiguous symbol. If using distinctive features, usage of underspecified features 
(leaving some cells empty) may help in expressing the semantics of the symbol.  

#### Uninterpretable source

Sometimes, the data source gives a symbol, which was originally intended as 
precise, but one can not figure out which phoneme was meant. E.g. did "j" in a 
specific source mean IPA [y]"
or [j] ? Ideally, it is better to use a clearer source. But if it is impossible, 
then the best is to keep the original symbol (again, use the `name` and `comment` 
columns should clarify the situation). Indeed, interpreting as either "[y]" or "[j]" 
when unsure would add a layer of obscuration. 

## How should sources be credited ?

We recommend crediting sources at every level. This should be indicated as relevant:

- for relations which affect all or a large part of the data: In the metadata, using the [`sources`](https://datapackage.org/standard/data-package/#sources) key, and in the README.md or accompanying documentation, in full text.
- for relations which affect only some data points (rows): using a [sources table](standard.md#sources)

## How should I link to other resources ?

To maximise interoperability, we recommend to systematically link to other resources 
insofar as possible. This can usually be done with using identifiers from the other resources, whether tabular data, corpora, or other.

In particular, it is strongly recommended to use standard vocabularies for things like languages ([glottocodes](https://glottolog.org/) or [iso codes](https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes)
  ), cells and features ([universal dependencies](https://universaldependencies.org/u/overview/morphology.html), [unimorph schema](https://unimorph.github.io/schema/),  [leipzig glossing rules](https://www.eva.mpg.de/lingua/pdf/Glossing-Rules.pdf)), phonemes ([IPA](https://www.internationalphoneticassociation.org/content/full-ipa-chart), [BIPA](https://clts.clld.org/contributions/bipa)), etc. In the [CLDF standard](https://cldf.clld.org/), this corresponds to the third design principle: "*If entities can be referenced, e.g. languages through their Glottocode, this should be done rather than duplicating information like language names.*". 

In the cases where controlled vocabularies imperfectly cover your needs, it is very 
useful to document the choices made in the README.md or accompanying documentation. 
For example, when no glottocode was exactly correct, was the closest code used instead 
? Or was the value left empty ?

## How is this different from Unimorph ?

Paralex lexicons aim to fill a need for more flexible and precise annotation of 
morphological systems. While we recommend to also provide morphological cells 
using the UNIMORPH schema, many linguistic analyses, 
whether synchronic or diachronic, 
quantitative or qualitative, benefit from also expressing these in other annotation 
scheme, such as Universal Dependency, or language-specific tags. UNIMORPH 
lexicons provide orthographic inflected forms, which is crucial for any applications 
which make use of corpora. However, we find that for linguistic purposes, a phonemic 
or phonetic representation is also important. Furthermore, we provide 
conventions to add rich, linguistically relevant information such as variation (see the [tags 
table](standard.md#tags)), [frequency information](standard.md#frequency), glosses 
(see the [lexeme](standard.md#lexeme) table), comments or alternate notations at 
any level (forms, cells, features, lexemes, frequency, tags) and more.
In order to improve the 
FAIRness and CAREness of datasets, Paralex lexicons add rich 
[frictionless](https://frictionlessdata.io/) metadata and custom [data sheets](https://cacm.acm.org/magazines/2021/12/256932-datasheets-for-datasets/fulltext).

UNIMORPH lexicons can often serve as the basis for Paralex lexicons, with the main 
processing step being to transcribe the orthographic forms into some phonemic or 
phonetic notation; and to carefully add linguistically relevant information.
In the other direction, Paralex lexicons, if they provide an equivalent for each cell in the UNIMORPH schema, 
can easily be exported into valid UNIMORPH lexicons.


## How is this related to CLDF ?

The Paralex standard owes a lot to [CLDF](https://cldf.clld.org/): it is our attempt to apply to inflectional lexicons the data practices disseminated by the [Cross-Linguistic Linked Data project (CLLD)](https://clld.org/). Although the type of datasets, the analyses which can be made of them, and the details of the standard are distinct, Paralex follows the same design principles. Like CLDF datasets, Paralex lexicons are constituted of relational databases written as sets of csv files, and accompanied by metadata in json format. Both also refer (and delegate meaning) to other vocabularies such as Glottolog, CLTS, etc. 
