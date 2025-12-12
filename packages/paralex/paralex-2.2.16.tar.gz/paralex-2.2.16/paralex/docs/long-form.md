Paradigmatic lexicons document the inflected forms of words, such as the conjugations of verbs and the declensions of nouns. Most of the descriptions below assume, for simplicity, that you are documenting a single part of speech of a single language. However, the standard extends naturally to multiple parts of speeches and languages.

A paradigm is the set of all the inflected forms of a word (or _lexeme_). For example, see this paradigm for the latin noun "rosa" ('rose'):

|                | singular | plural  |
|----------------|----------|---------|
| **nominative** | rosa     | rosae   |
| **vocative**   | rosa     | rosae   |
| **accusative** | rosam    | rosās   |
| **genitive**   | rosae    | rosārum |
| **dative**     | rosae    | rosīs   |
| **ablative**   | rosā     | rosīs   |

A few vocabulary terms are useful to refer to the elements constitutive of a paradigm:

- The two tables above are filled with orthographic **forms**, such as "rosa" or "rosārum".

- The column and row headers are labelled with grammatical **feature values** such as 
  "singular",  and "nominative", which combine into **cells** such as "nominative 
  singular". Cells are the morpho-syntactic feature-value combinations for which words 
  inflect.

- All of these forms belong to the same word, or **lexeme**. Lexemes are the abstract 
  units which group together all the inflected forms of a same word. They are usually 
  referred to by a label which is often their citation form. For Latin nouns, that is 
  the nominative ROSA. This label is sometimes called **lemma**. It is usually 
  written in small capitals.

A paradigm can be written as a (set of) table(s) in a variety of formats. When 
discussing a single lexeme, authors often prefer tables similar to the one presented 
above, as they make the multidimensional structure of the paradigm easy to 
visualize. This is a good format for presenting data to the human eye, but has draw 
backs as a data storage and sharing format, notably:

1. To describe multiple lexemes, we need as many tables as we have lexemes.
2. It does not allow us to specify more information about each form (How is it pronounced?
   How frequent is it? etc.) conveniently.

## Wide format

 The wide format, also commonly used, provides the lemma label and the set of cells as 
 column headers, and each paradigm as a row. In morphology, it is also called a **plat** 
 (Stump & Finkel 
 2013). Using a plat addresses the first  problem above, since multiple lexemes can be 
 given as separate rows of a same table. 
 See for example these two paradigms for the latin nouns ROSA and DOMINUS.

 | lemma label | nom.sg  | voc.sg | acc.sg  | gen.sg | dat.sg | abl.sg | nom.pl | voc.pl | acc.pl  | gen.pl    | dat.pl  | abl.pl  |
|-------------|---------|--------|---------|--------|--------|--------|--------|--------|---------|-----------|---------|---------|
| ROSA        | rosa    | rosa   | rosam   | rosae  | rosae  | rosā   | rosae  | rosae  | rosās   | rosārum   | rosīs   | rosīs   |
| DOMINUS     | dominus | domine | dominum | dominī | dominō | dominō | dominī | dominī | dominōs | dominōrum | dominīs | dominīs |

 Unfortunately, it does not address the second problem above (providing more 
 information about each form), and it adds an extra issue:

1. In wide format, lines can get very long when there are many paradigm cells (a common 
occurence in the worlds' languages), which is hard to read for both humans (who do not enjoy scrolling horizontally) and machines (for which loading a very long line in memory is costly).
{: value='3' }

The same table is sometimes seen pivoted (with lexemes in columns and cells in rows), 
without any impact on problems (2) and (3).

## Long format

The long format, illustrated below, addresses all the above problems:


| cell   | lexeme  | orth_form |
|--------|---------|-----------|
| nom.sg | rosa    | rosa      |    
| voc.sg | rosa    | rosa      |   
| acc.sg | rosa    | rosam     |   
| gen.sg | rosa    | rosae     |  
| dat.sg | rosa    | rosae     |  
| abl.sg | rosa    | rosā      |   
| nom.pl | rosa    | rosae     |  
| voc.pl | rosa    | rosae     |  
| acc.pl | rosa    | rosās     |   
| gen.pl | rosa    | rosārum   |   
| dat.pl | rosa    | rosīs     |   
| abl.pl | rosa    | rosīs     |   
| nom.sg | dominus | dominus   |
| voc.sg | dominus | domine    |
| acc.sg | dominus | dominum   |
| gen.sg | dominus | dominī    |
| dat.sg | dominus | dominō    |
| abl.sg | dominus | dominō    |
| nom.pl | dominus | dominī    |
| voc.pl | dominus | dominī    |
| acc.pl | dominus | dominōs   |
| gen.pl | dominus | dominōrum |
| dat.pl | dominus | dominīs   |
| abl.pl | dominus | dominīs   |


In long format, each row documents a specific *form* of a specific *lexeme*, inflected 
for a specific *cell*. Thus, rows are minimally triplets. Having files with many lines 
is not a problem (computers being able to read them one by one). Any extra information 
about forms can be documented by simply adding more columns.  This makes it a good 
format for storing and exchanging data. Since this format is very explicit, it is easy 
to automatically generate tables in other formats for human visualisation.


To read more on the reasons to adhere to the long format for tabular linguistic data, refer to the [CLDF](https://cldf.clld.org/) paper:  

Forkel, Robert, Johann-Mattis List, Simon J. Greenhill, Christoph Rzymski, Sebastian Bank, Michael Cysouw, Harald Hammarström, Martin Haspelmath, Gereon A. Kaiping & Russell D. Gray. 2018. [Cross-linguistic data formats, advancing data sharing and re-use in comparative linguistics](https://www.nature.com/articles/sdata2018205). Scientific Data 5. 180205. doi:[10.1038/sdata.2018.205](https://www.doi.org/10.1038/sdata.2018.205)