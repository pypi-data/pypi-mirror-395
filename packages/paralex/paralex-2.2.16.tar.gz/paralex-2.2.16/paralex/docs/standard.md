!!! info

    The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

This document defines a common standard for sharing lexicons of morphological paradigms. While the specifications tend to be
rigid with respect to their formal aspects (how to format data and metadata), we understand that as
linguists, we are most interested in the parts of language that are complex to analyze,
and thus complex to code. Thus, the standard is more flexible regarding the exact
content of the data,
allowing linguists to make project-specific choices about content, while reaping other benefits of standardisation.

## Documentation

Datasets must be accompanied by human-readable documentation, justifying important
choices in the constitution of the dataset and guiding users in its interpretation. Minimally, a README.md
MUST be present. It is RECOMMENDED to also add a `data_sheet.md` file, following [the
template](https://gitlab.com/sbeniamine/paralex/-/blob/main/paralex/standard/data_sheet.md). More documentation
MAY be present if needed.

## Metadata

[Metadata](metadata.md) MUST be provided in [json](https://www.json.org/json-en.html),
following
the [frictionless](https://frictionlessdata.io/) standard, and in conformity with
the [specs](specs.md) (also readable directly in json: [paralex.package.json](https://gitlab.com/sbeniamine/paralex/-/blob/main/paralex/standard/paralex.package.json)).
See the [tutorial](tutorial.md) on how to generate metadata automatically.

At the highest level, we add a `languages_iso639` key, the value of which is a list of iso language codes.

The metadata is thus given as a json file. Here is what such a file might look like:

??? example "example of .json metadata file"
    ```json title=".package.json file"
        {%
        include "examples/minimal/paralex-min-chanter.package.json"
        %}
    ```

The metadata specify information about the dataset (such as its contributors, title,
relevant keywords, license, etc), and about what each table contains (its name, title,
path, relation to other tables, detailed list of columns, etc.). It serves both as
documentation, and as a tool to validate and manipulate the data.

For more information about what can be expressed by this metadata file, see the
[paralex specs](specs.md) and the [frictionless specs](https://specs.frictionlessdata.io/).

### Relation to other work

Frictionless provides a way to specify relations to other work, [using a `source` key](https://datapackage.org/standard/data-package/#sources), at the level of entire datasets.

For citing academic sources relevant for specific data points, one can instead add `source` columns, containing keys to a [sources](#sources) file.

## Data format

Paradigmatic lexicons are tabular datasets. **Paralex** lexicons MUST be provided in
[long form](long-form.md), written as csv (comma separated value) tables using utf-8 encoding.

!!! example

    === "Visual table"

        {{ read_csv('examples/minimal/forms.csv') }}

    === "CSV table"
        
        ~~~ csv title="forms.csv"
         {% include "examples/minimal/forms.csv" %}
        ~~~

## Files

Most of the data files expected are tables. A dataset MUST contain at least one [forms](#forms) table documenting
inflected forms. Usually, a single table is not sufficient to provide all relevant information.
The following tables SHOULD also be included:

* a [sounds](#sounds) table documents the inventory of sounds used in the transcription
* a [cells](#cells) table documents the inventory of feature-value combinations
  (_paradigm cells_) for which lexemes inflect.
* a [features-values](#features-values) table documents the inventory of grammatical features
  which
  compose the cells

Depending on the amount of information and granularity provided, the following files
MAY also be included:

* a [lexemes](#lexemes) table documents the inventory of lexemes for which inflected forms
  are given
* a [tags](#tags) table provides a way of grouping rows of a table together, in
  paricular sets of inflected forms. Tags can indicate epistemic status (generated
  form vs attested), series of overabundant or defectiveness forms, specific dialectal
  or sociolinguistic variants, etc.
* a [frequencies](#frequencies) table provides complex frequency information where it
  would be insufficient to use frequency columns on lexemes and forms tables.
* a [graphemes](#graphemes) table documents the inventory of graphemes used in the
  orthographic form
* a [sources](#sources) file in bibtex or biblatex format (`.bib`) documents sources used in any table in the `source` column.

Further tables MAY be added to your resource as needed, for example to document
languages, inflection classes, etc. The tables MAY be divided in several files to reduce their size.

The exact set of standard columns for each table is described in [the specification](specs.md).
The dataset MUST NOT use aliases or alternate column names for columns
described in the specification. It MAY use additional columns, which SHOULD strive to
follow existing conventions and use known vocabularies. The columns MAY be given in
any order, though as a convention, the identifier column (`form_id`, `sound_id`,
`cell_id`, etc) SHOULD be the first column of their table.

The tables within the dataset have a range of specific, formal relationships to one another. That is to say, they are all linked together via a relational model. That model is summarized below. View the simple/advanced diagrams to see less or more detail.

=== "Relations between tables: simple"
    ``` mermaid
    graph TD
        A[sounds.csv] --- B(forms.csv)
        F[graphemes.csv] --- B
        C[cells.csv] --- B
        D[tags.csv] --- B
        E[features-values.csv] --- C
        G[lexemes.csv] --- B
        H[frequencies.csv] --- C
        H --- B
        H --- G
        D --- G
        D --- H
    ```

    - The `phon_form` entries of the forms table are composed of identifiers in the sounds table
    - The `orth_form` entries of the forms table are composed of identifiers in the graphemes table
    - The `cell` entries of the forms table match identifiers in the cells table
    - IDs in the cells table are composed of identifiers in the features-values table
    - Entries in the `lexeme` column of the forms table match identifiers in the lexemes table
    - Entries in the `_tags` columns of the forms and lexemes table, separated by `|`, 
     match identifiers in the tags table
    - Entries in the frequencies tables may link to various other tables

=== "Relations between tables: advanced"

    ``` mermaid
    erDiagram
        sounds }|..|{ forms : "compose the phon_form"
        graphemes }|..|{ forms : "compose the orth_form"
        features-values }|..|{ cells : "compose the cell_id"
        cells ||--|{ forms : "is referenced by (foreign key)"
        lexemes ||--|{ forms : "is referenced by (foreign key)"
        tags }|..|{ forms : "reference (multiple values possible)"
        tags }|..|{ lexemes : "reference (multiple values possible)"
        tags }|..|{ frequencies : "reference (multiple values possible)"
        frequencies }|--|{ lexemes : "is referenced by (foreign key)"
        frequencies }|--|{ forms : "is referenced by (foreign key)"
        frequencies }|--|{ cells : "is referenced by (foreign key)"
        sounds {
            string sound_id
            string label
            string comment
            string CLTS_id
            string PHOIBLE_id
        }
        forms {
            string form_id
            string lexeme
            string cell
            string phon_form
            string orth_form
        }
        features-values {
            string value_id
            string label
            string feature
            integer canonical_order
        }
        lexemes {
            string lexeme_id
            string inflection_class
            string label
            string gloss
        }
        cells {
            string cell_id
            string unimorph
            string ud
            string comment
        }
        tags {
            string tag_id
            string type
            string comment
        }
        graphemes {
            string grapheme_id
            string comment
            integer canonical_order
        }

        frequencies {
            string freq_id
            number frequency
        }
    ```

    In this diagram:

    - Solid lines indicate the "foreign key" relationship: the `cell` column in forms
     must refer exactly to rows of the `cells` table, identified by their `cell_id`. The `
     lexeme` column in forms must refer exactly to rows of the `lexemes` table,
     identified by their `lexeme_id`.
    - Dotted lines indicate a vocabulary relationship: the `phon_form` column in forms
    must be composed of `sound_id`s from the `sounds` table, and the `cell_id` column in `cells`
    must be composed of `value_id`s from the `features-values` table.
    - Only four columns are shown for each table, see the [specs](specs.md) for the full column lists.

### Forms

Each row of the forms table documents a single inflected form.

The forms table MUST have at least the columns: `form_id`, `cell`, `lexeme` and
either a `phon_form` (phonological form), or `orth_form` (orthographic form). It
SHOULD have a `phon_form`. We do not impose any particular phonological or phonetic
analysis or sets of symbols, though datasets MUST follow some established convention.

The value of the `phon_form` MUST be a sequence of space-separated segments, e.g. not
`"dominoːrum"` but `"d o m i n oː r u m"`. If there is a `sounds` table, then all segments used in the `phon_form` MUST be documented by a row in `sounds`.

Values in the `cell` and `lexeme` columns MUST
correspond to identifiers in the cells and lexemes tables respectively if these tables
exist.

!!! example "forms table"

    Here are a few rows representing the latin nominal paradigm of the word DOMINUS (master):

    | form_id | lexeme  | cell   | phon_form          |
    |---------|---------|--------|--------------------|
    | f266    | dominus | abl.pl | d o m i n iː s     |
    | f1299   | dominus | abl.sg | d o m i n oː       |
    | f2325   | dominus | acc.pl | d o m i n oː s     |
    | f3359   | dominus | acc.sg | d o m i n u m      |
    | f4385   | dominus | dat.pl | d o m i n iː s     |
    | f5418   | dominus | dat.sg | d o m i n oː       |
    | f6444   | dominus | gen.pl | d o m i n oː r u m |
    | f7478   | dominus | gen.sg | d o m i n iː       |
    | f8504   | dominus | nom.pl | d o m i n iː       |
    | f9537   | dominus | nom.sg | d o m i n u s      |
    | f11596  | dominus | voc.sg | d o m i n e        |
    | f10563  | dominus | voc.pl | d o m i n iː       |

If a `frequency` column is present, the source
of the frequencies MUST be documented in the `README.md` or accompanying documentation. If
providing multiple frequency measurements, it is best to use a [separate frequencies table](#frequencies).

The table MAY have more columns, including those [described in  the specification](specs.md#forms-table).

#### Supra-segmental information in form transcriptions

Phonemic representations SHOULD include supra-segmentals
such as stress, length, tones. They MAY also provide syllable structure.

There are many ways to annotate supra-segmental information. The RECOMMENDED way to do so
is to mark supra-segmental information within the sequence of segments, as separate
characters or diacritics attached to the segment which bears them (or the nucleus of the affected syllable).

!!! example "suprasegmentals in `phon_form`"

    Here is an example for Nuer nominal plural, which involves breathy voice, length alternations, and tone.

    | form_id | lexeme  | cell   | phon_form |
    |---------|---------|--------|-----------|
    | f1      | ‘ant’   | nom.sg | c w ɔ̤́ x   |
    | f2      | ‘arrow’ | nom.sg | b ʌ̤̀ːː r   |
    | f3      | ‘bead’  | nom.sg | t ɪ̂ː k    |
    | f4      | ‘belt'  | nom.sg | l à̤ːː ɣ   |
    | f5      | ‘ant’   | nom.pl | c ṳ̌ːː ɣ   |
    | f6      | ‘arrow’ | nom.pl | b ʌ̤̀ːː r í̤ |
    | f7      | ‘bead’  | nom.pl | t j ɛ̂ x   |
    | f8      | ‘belt'  | nom.pl | l ʌ̤̌ː k    |

!!! note

    The choice of particular conventions is not constrained: you can choose
    to  write a high tone as `́`, `˦`, `1`, etc. However, a single dataset MUST adhere
    to a  single, coherent notational choice which SHOULD be documented through the sounds
    table and follow a formally specified standard, such as [CLTS BIPA](https://clts.clld.org/contributions/bipa).


#### Usage of tags

It is not uncommon for the cell of a paradigm to be associated with multiple variant
forms. There are several kinds of variation that we would not wish to conflate.
Accordingly, to mark forms which are related to each other in certain ways,
we use tags. Any tag defined in the [tags table](standard.md#tags)
can be used in the appropriate `*_tags` columns. Several tags can be used, in which case
they are
separated with a `|` (and no spaces). Their order is not meaningful.

Importantly, form variants MUST NOT be aggregated into a single entry such as
'learn{ed/t}' or 'learned~learnt'. Rather, each variant is represented in its own row
in the forms table and indexed with a tag identifier (see [why the long form ?](long-form.md)).

**overabundance** can lead to two rows for the same lexeme and
paradigm cell. Sometimes, overabundance is specific to a single lexeme. Sometimes,
however,
overabundant forms across cells of a single lexeme form coherent sets which share for
example the same stem, the same register, or more generally the same type of variation.
These forms can be linked together by a tag in the `overabundance_tag` column.


!!! example "Overabundance"

    === "In the forms table"
    
        | form_id | lexeme  | cell   | phon_form | overabundance_tag |
        |---------|---------|--------|-----------|-----------|
        | f1      | dream   | pst | d r ɛ m t   | irreg;t-form |
        | f2      | dream   | pst | d r iː m d   | d-form |
        | f3      | learn   | pst | l ɜː n d  | d-form |
        | f4      | learn   | pst | l ɜː n t  | t-form |
        | f5      | leap   | pst | l ɛ p t | irreg;t-form |
        | f6      | leap   | pst | l iː p t  | t-form |
        | f7      | sweat   | pst | s w ɛ t |  irreg |
        | f8      | sweat   | pst | s w ɛ t ɪ d  | d-form |

    === "In the tags table"
    
        | tag_id | tag_column_name   | comment |
        |-----------|---------|------------------|
        | irreg       | overabundance_tag | irregular form |
        | d-form          | overabundance_tag | past in  /d/ |
        | t-form          | overabundance_tag | past in  /t/ |


**defectiveness**: Defectiveness happens when some forms do not exist in a paradigm:
for example, what is the singular of the English word "scissors" ? There is none,
because this word exists only in the plural, it is a `plurale tantum`.

When this happens, simply leaving out rows is insufficient, as it is ambiguous between
defectiveness and missing data. Thus, defective forms MUST have their own rows, and SHOULD be
identified by identifiers in the `defectiveness_tag` column. Defective rows use this
column to
group together either all defective forms using a general label such as `defective`,
or sets of defective forms, according to some analysis or motivation, for example  
`pluralia_tantum`. Any relevant labels and groupings can be used, and MUST be defined
in the tags table. In most cases, defective forms will not have any defined or well-formed phonological or orthographic representation.

The `phon_form` of a defective entry MUST contain "#DEF#" (meaning defective).
It is possible for a defective form to still provide a well-formed phonological or
orthographic form (speakers could produce the form, it is just not used), using the
defectiveness_tag to label the row.

!!! example "Defectiveness: Latin pluralia_tantum"

    === "In the forms table"
    
        In this example, the form of the latin noun "pauci" have no well formed singular,
        as the word is a "pluralia tantum" (it is only used in the plural). The table still
        provides rows for each singular case, but the form is replaced by "#DEF#", and the
        `defectiveness_tag` column is marked for these forms with the type of defectivity,
        `pluralia_tantum`.
    
        | form_id | lexeme | cell   | phon_form       | defectiveness_tag |
        |---------|--------|--------|-----------------|----------------------|
        | f1122   | pauci  | abl.pl | p a w k iː s    |                      |
        | f1299   | pauci  | abl.sg | #DEF#           | pluralia_tantum      |
        | f2325   | pauci  | acc.pl | p aw k oː s     |                      |
        | f3359   | pauci  | acc.sg | #DEF#           | pluralia_tantum      |
        | f4385   | pauci  | dat.pl | p aw k iː s     |                      |
        | f5418   | pauci  | dat.sg | #DEF#           | pluralia_tantum      |
        | f6444   | pauci  | gen.pl | p aw k oː r u m |                      |
        | f7478   | pauci  | gen.sg | #DEF#           | pluralia_tantum      |
        | f8504   | pauci  | nom.pl | p aw k iː       |                      |
        | f9537   | pauci  | nom.sg | #DEF#           | pluralia_tantum      |
        | f10563  | pauci  | voc.pl | p a w k iː      |                      |
        | f11596  | pauci  | voc.sg | #DEF#           | pluralia_tantum      |

    === "In the tags table"
    
        | tag_id | tag_column_name   | comment |
        |-----------|---------|------------------|
        | pluralia_tantum       | defectiveness_tag | defective forms because the lexeme exist only in the plural |

**variants**: Dataset MAY account for observed variation across speakers by
providing multiple rows for the same lexeme and paradigm cell, each containing a
distinct phonemic forms, as well as an annotation in the form of a tag (`variants_tag`).

**epistemic status**: The column `epistemic_tag` MAY be used to indicate the
epistemic
status of a
row's form. Suggested levels are: `manually_checked`, `controversial`, `uncertain`,
`generated`, `attested`. Custom levels may be chosen.

**analytic choices**: If providing various analyses of the phonological form, the
forms file MUST have a separate row for each analysis, and the rows MUST be
annotated using the column `analysis_tag` to identify which are part of the same analytic set.

If providing two levels of abstraction for the `phon_form` (eg. one more
phonetic and one more phonemic), two rows should be present with distinct `phon_form`, one
annotated as `phonemic`, and one as `phonetic` in the `analysis_tag` column.

#### Segmented forms

Lexicons MAY provide segmentation information, using the `analysed_phon_form` and
`analysed_orth_form` columns. The
default segmentation marker should be `+` within word, and `#` for word boundary. If a
more complex set of
markers is
necessary, it MUST be documented
explicitly. If multiple segmentations are provided,
each alternative MUST constitute a separate row, and they MUST be annotated with tags
in order to distinguish each series of forms.

!!! example "segmented forms"

    Here is an example for the latin forms of dominus:
    
    |  form_id  |  lexeme   |  cell    | phon_form | analysed_phon_form |
    |-----------|-----------|----------|-----------------------|-----------------------|
    |  f266     |  dominus  |  abl.pl  | d o m i n iː s      | d o m i n + iː s      |
    |  f1299    |  dominus  |  abl.sg  | d o m i n oː        | d o m i n + oː        |
    |  f2325    |  dominus  |  acc.pl  | d o m i n oː s      | d o m i n + oː s      |
    |  f3359    |  dominus  |  acc.sg  | d o m i n u m       | d o m i n + u m       |
    |  f4385    |  dominus  |  dat.pl  | d o m i n iː s      | d o m i n + iː s      |
    |  f5418    |  dominus  |  dat.sg  | d o m i n oː        | d o m i n + oː        |
    |  f6444    |  dominus  |  gen.pl  | d o m i n oː r u m  | d o m i n + oː r u m  |
    |  f7478    |  dominus  |  gen.sg  | d o m i n iː        | d o m i n + iː        |
    |  f8504    |  dominus  |  nom.pl  | d o m i n iː        | d o m i n + iː        |
    |  f9537    |  dominus  |  nom.sg  | d o m i n u s       | d o m i n + u s       |
    |  f10563   |  dominus  |  voc.pl  | d o m i n iː        | d o m i n + iː        |
    |  f11596   |  dominus  |  voc.sg  | d o m i n e         | d o m i n + e         |

### Sounds

The sounds table describes the full inventory of sounds used in the transcriptions. In
the `phon_form`, these sounds are separated by spaces.

The sounds table MUST have at least an identifier column `sound_id`.

The sounds table is the result of analytic choices. In order to
detail the precise meaning of each sound in this particular dataset, the table SHOULD
have a column `label` indicating what the sound means in natural language, and SHOULD
provide ways to identify the sounds by linking to other resources (e.g. using the columns
`CLTS_id`,
`PHOIBLE_id`) or through other columns (for example, by defining a
language-specific set of distinctive features). It is best to
employ a
multiplicities of these strategies to maximize compatibility of datasets. Moreover,
this table MAY have a `comment` column to further annotate complex or unusual choices.

### Graphemes

The Graphemes table describes the full inventory of graphemes used in the orthographic
form column `orth_form` in the forms table. It MUST have at least an identifier column `grapheme_id`. It may have any other
columns, in particular a `label`, `comment` and a `canonical_order`.
It MAY have more columns, including those [described in  the specification](specs.md#graphemes).

Having this table ensures that orthographic forms will be checked automatically
during validation.

!!! example "Letters in French"

    | grapheme_id | comment | canonical_order |
    |-------------|---------|-----------------|
    | a           |         | 1               |
    | à           |         | 2               |
    | b           |         | 3               |
    | c           |         | 4               |
    | d           |         | 5               |
    | e           |         | 6               |
    | é           |         | 7               |
    | è           |         | 8               |
    | ê           |         | 9               |
    | f           |         | 10              |
    | g           |         | 11              |
    | h           |         | 12              |
    | i           |         | 13              |
    | ï           |         | 14              |
    | j           |         | 15              |
    | k           |         | 16              |
    | l           |         | 17              |
    | m           |         | 18              |
    | n           |         | 19              |
    | o           |         | 20              |
    | ô           |         | 21              |
    | p           |         | 22              |
    | q           |         | 23              |
    | r           |         | 24              |
    | s           |         | 25              |
    | t           |         | 26              |
    | u           |         | 27              |
    | v           |         | 28              |
    | w           |         | 29              |
    | x           |         | 30              |
    | y           |         | 31              |
    | z           |         | 32              |

### Cells

The cells table describes the full inventory of feature-value combinations for which
lexemes inflect. These are usually called _paradigm cells_ in morphology. Example of
paradigm cells are: "indicative present first person singular" (abbreviated ind.prs.1sg)
or
"nominative plural" (abbreviated nom.pl).

The cells table MUST have at least an identifier column `cell_id`.
It MAY have more columns, including those [described in  the specification](specs.md#cells).

If there is no `features-values` table, then the cells table MUST have at least one column mapping
the cells to a widely used vocabulary, such as unimorph, universal dependencies, GOLD,
etc. If there is a features-values table (properly linked to other vocabularies itself), then
linking cells to other vocabularies is only RECOMMENDED. If there are several competing
naming conventions for some cells, the authors may choose freely, but SHOULD provide
alternate names in another column to maximize understandability and make translation from
one convention to another as easy as possible.

We recognize that some vocabularies cannot account for specific phenomena (for
example, when order is distinctive due to affix stacking, but a particular vocabulary
does not distinguish between gen.du and du.gen).
Dataset authors are free to pick any existing, formal vocabulary which they deem expressive
enough. If none exist, it is strongly RECOMMENDED to raise the issue with the people maintaining
these vocabularies, and they MAY provide imperfect mappings to the best
vocabulary available. They MUST comment the issue in the documentation.

Identifiers for the cells, `cell_id`, MUST be feature values in **lowercase**,
separated by
dots, as in: "nom.sg" for nominative singular (this follows the Leipzig Glossing Rule
convention). If there is a features-values table, all of the feature values composing
these
identifiers MUST be documented as separate rows in the features-values table.


This allows considerable flexibility in using ad-hoc cells, while ensuring compositional
labels (made of features-values), and encouraging transparent semantics (linking to other
vocabularies).

Choosing and labelling paradigm cells is often a tricky matter, with considerable
disagreement in the literature. Whatever choices are made in this regard, they
SHOULD be explicitly documented.

!!! example

    | cell_id | ud            | POS | unimorph |
    |---------|---------------|-----|----------|
    | nom.pl  | NOUN:Nom+Plur | noun   | N;NOM;PL |
    | nom.sg  | NOUN:Nom+Sing | noun   | N;NOM;SG |
    | voc.pl  | NOUN:Voc+Plur | noun   | N;VOC;PL |
    | voc.sg  | NOUN:Voc+Sing | noun   | N;VOC;SG |
    | acc.pl  | NOUN:Acc+Plur | noun   | N;ACC;PL |
    | acc.sg  | NOUN:Acc+Sing | noun   | N;ACC;SG |
    | gen.pl  | NOUN:Gen+Plur | noun   | N;GEN;PL |
    | gen.sg  | NOUN:Gen+Sing | noun   | N;GEN;SG |
    | dat.pl  | NOUN:Dat+Plur | noun   | N;DAT;SG |
    | dat.sg  | NOUN:Dat+Sing | noun   | N;DAT;PL |
    | abl.pl  | NOUN:Abl+Plur | noun   | N;ABL;PL |
    | abl.sg  | NOUN:Abl+Sing | noun   | N;ABL;SG |

### Features-values

The features-values table MUST have at least a feature identifier `value_id`, a
feature `label` (the full
feature value in lowercase, e.g. nominative or past), and a `feature` dimension (e.g.
case or tense).
It MAY have more columns, including those [described in  the specification](specs.md#features-values). Linking to
other resources from this table is RECOMMENDED.

Feature identifiers are feature-values. They MUST be lowercase.


!!! example "Feature values table for latin nouns"

    | value_id | label      | feature | POS | canonical_order |
    |------------|------------|-----------|-----|-----------------|
    | nom        | nominative | case      | noun   | 1               |
    | voc        | vocative   | case      | noun   | 2               |
    | acc        | accusative | case      | noun   | 3               |
    | gen        | genitive   | case      | noun   | 4               |
    | dat        | dative     | case      | noun   | 5               |
    | abl        | ablative   | case      | noun   | 6               |
    | sg         | singular   | case      | noun   | 1               |
    | pl         | plural     | case      | noun   | 2               |

While using case to distinguish feature values (eg. S for subject but s for singular)
is not allowed, we recommend to provide mappings in the
features table and cells table which provide mappings to other conventions, in particular
those used in specific sources:

!!! example "Feature values table with subject and singular"

    | value_id | label      | feature | POS | value-Author2020 |
    |------------|------------|-----------|-----|-----------------|
    | sbj        | subject | function      | verb   | S               |
    | sg        | singular   | number      | noun   | s               |

The meaning of these extra columns can be documented in the metadata.

### Lexemes

The lexemes table MUST have at least a lexeme identifier `lexeme_id`. It documents any information
which is valid for entire lexemes.
It MAY have more columns, including those [described in  the specification](specs.md#lexemes). Additional columns MAY be added.

If a `frequency` column is present, the source
of the frequencies MUST be documented in the README.md or accompanying documentation. If
providing multiple frequency measurements, it is best to use a [separate frequencies table](#frequencies).


In cases where a lexeme may take either of two inflection classes or stems, and has a
full paradigm for each, it is preferable to divide it into two separate lexemes (or
[_flexemes_](#paradigm-structure)). This choice MUST be described in the documentation.

!!! example "Two rows of a lexeme  table for latin nouns"

    | lexeme_id | label   | inflection_class | POS | meaning | frequency |
    |-----------|---------|------------------|-----|---------|-------------|
    | dominus   | dominus | 2                | noun   | master  |   10000     |
    | rosa      | rosa    | 1                | noun   | rose    |   6000      |

### Tags



The tags table MUST have at least a tag identifier `tag_id`, a reference to the column
in which they occur (`tag_column_name`) and a comment. Tags are mainly used in the
forms table but can also be used in the lexeme and frequency tables as needed. The
standard pre-defines the tag column names `analysis_tag`, `defectiveness_tag`,
`epistemic_tag`, `variants_tag`, `overabundance_tag`. More custom tag names can be added,
and
they
MUST end in `_tag`.

It MAY have more columns, including those [described in  the specification](specs.md#tags).

!!! example "A few rows of a possible tags table for English verbs"

    | tag_id | tag_column_name   | comment |
    |-----------|---------|------------------|
    | uk_dialect   | variants_tag | variant majoritarily used in UK English              |
    | us_dialect      | variants_tag    |  variant majoritarily used in US English   |
    | irreg       | overabundance_tag | irregular form |
    | d-form          | overabundance_tag | past in -ed pronounced /d/ |
    | t-form          | overabundance_tag | past in -ed pronounced /t/ |

Note that one can not deduce information for rows which are *not* marked by tags. For
example, if some rows of the forms table are marked as `uk_dialect`, some as
`us_dialect`, and some are not marked, it is not possible to know where these unmarked
forms are used. Thus, it is RECOMMENDED to be more explicit and always provide (and
use) non-marked or default tags:


!!! example "Tags including non-marked situations"

    | tag_id | tag_column_name   | comment |
    |-----------|---------|------------------|
    | uk_specific   | variants_tag | variant majoritarily used in UK English              |
    | us_specific      | variants_tag    |  variant majoritarily used in US English   |
    | all_dialects | variants_tag | forms which are not specific to a particular English dialect |

### Frequencies

Sometimes, having frequencies in columns in the forms, lexeme, or even cells
tables is not satisfactory. Possible reasons for this are:

- There are multiple sources of frequencies (either multiple corpora in which they were
  measured, or multiple sources providing frequencies directly) or methods through
  which they were measured.
- Frequencies were measured for units distinct from those that constitute rows in
  other tables: eg. combinations of <lexeme, cell> which ignore orthographic or
  phonological variants documented in the forms table.

In that case, a dataset MAY provide a separate frequency table.

Frequencies tables MAY have a variety of shapes, as frequency can be measured or
aggregated at
various levels. They MUST link to relevant table(s) using at least one column with
identifiers from another table. For example, this could be:

- Frequency of a lexeme (`lexeme` column linking to `lexeme_id` in the lexemes table)
- Frequency of a cell (`cell` column linking to `cell_id` in the cells table)
- Frequency of a specific form row (`form` column linking to `form_id` in the
  forms table)
- Frequency for a cell/lexeme combination, regardless of the phonological variant (two
  identifier columns),
- etc.

Each row MUST represent a single frequency value from a single source.

In this first example, frequencies are associated to specific rows from the forms
table. Note that multiple sources for a same data point lead to separate rows:

!!! example "Imaginary frequencies for possible variant forms, associated to forms"

    | freq_id | form | value | source |
    |------|------------|-------|--------|
    | 9929 | eat_prs_us | 3888 | source1 |
    | 9930 | eat_prs_uk | 4900 | source2 |
    | 9931 | eat_prs_uk | 3000 | source1 |


In the second example, frequencies are provided for lexeme/cell combinations (which
might lead to multiple rows in the forms table):

!!! example "Imaginary frequencies associated to lexemes and cells"

    | freq_id | lexeme | cell | value | source |
    |------|--------|------|-------|--------|
    | 9929 | eat    | prs  | 3888 | source1 |
    | 9930 | eat | prs  | 4900 | source2 |

Note that for frequency, `0` means non-attested in the dataset used, whereas an empty
cell means that the frequency for this form was never evaluated.

### Sources

A `sources` file containing bibtex references MAY be added. The `source` columns of the tables MUST contain bibtex keys, which MUST be referenced in a `sources.bib` file. 

The `source` columns are mostly used when specific data points (forms, lexemes, frequencies, etc) come from different sources,
such that the dataset authors need to specify the source of each data point.
They SHOULD NOT be used to provide the same single source for every data point (in that case the source is rather the source of the entire dataset and MUST be referenced in the JSON metadata).

