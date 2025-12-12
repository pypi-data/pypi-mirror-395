Paradigm structures are analyses, and dataset authors have freedom in how they want to
formulate this analysis. Among the main problems are:

1. What is the inventory of paradigm cells ?
2. How should each cell be characterised?
3. What counts as a lexeme ?

# What is the inventory of paradigm cells ?

Data creators can provide labels of their choice, but
should use a cells and features table to document the meaning of these labels, and map
from these labels to existing standards and conventions.

# How should each cell be characterised ?

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

# What should count as a lexeme

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

# references

- Fradin, Bernard & Françoise Kerleroux. 2003. Troubles with lexemes. In Geert Booij, Janet DeCesaris, Angela Ralli & Sergio Scalise (eds.), Selected papers from the third Mediterranean Morphology Meeting, 177–196. Barcelona: IULA – Universitat Pompeu Fabra.
- Boyé, G., & Schalchli, G. (2016). The Status of Paradigms. In A. Hippisley & G. Stump  (Eds.), The Cambridge Handbook of Morphology (Cambridge Handbooks in Language and Linguistics, pp. 206-234). Cambridge: Cambridge University Press. DOI: [10.1017/9781139814720.009](https://doi.org/10.1017/9781139814720.009)
- Anna M. Thornton (2018). Troubles with flexemes. In Olivier Bonami, Gilles Boyé, Georgette Dal, Hélène Giraudo & Fiammetta Namer (eds.), The lexeme in descriptive and theoretical morphology, 303–321. Berlin: Language Science Press. DOI: [10.5281/zenodo.1407011](https://doi.org/10.5281/zenodo.1407011)