
The sounds table documents the set of sounds used in transcription (the `phon_form` 
column of the `forms` table). Although it is best to use common conventions, it is 
often impossible to avoid language specific analytic choices in the sound inventory. 

## Which other databases should one link to in order to define sounds meaning ?

We suggest using valid BIPA (see [CLTS](https://clts.clld.org/)) sounds, providing 
references to CLTS's BIPA or to [PHOIBLE](https://phoible.org/).

## How to manage ambiguous notations ?

There are a variety of situations which lead to ambiguous notations, e.g. where one has a 
symbol "R" which might stand for either the sound "r" or "ɹ". Whenever possible, we 
recommend avoiding ambiguous sounds, as they  reduce the compatibility with other 
transcription systems. When using an ambiguous symbol is the only reasonable choice,
it is crucial to document precisely their meaning and avoid confusions.

Here are some specific cases:

### Real variation (either free or conditionned)

If the intended meaning of "R" is that some speakers would pronounce "r" and some "ɹ", 
the recommended solution is to use both of these more precise, concrete sounds, 
provide distinct rows in the `forms` table with 
each, and tag them using a `variant` tag. A possible, but less satisfactory 
alternative is to consistently pick a single one (eg "r"), and ignore the variation.

### Imprecise transcription

Sometimes, the data source gives an imprecise transcription, e.g. "R", but it is 
unclear whether "r" or "ɹ" are meant. This includes cases of reconstruction which are 
intentionally vague, uncertainties in field work data, or ambiguous data points where 
other forms do contain the precise symbol. In this case, 
keeping the imprecise symbol "R" is best. It might be difficult, then, to link it properly to 
other databases. The `label` and `comment` columns should clarify the meaning of the 
ambiguous symbol. If using distinctive features, usage of underspecified features 
(leaving some cells empty) may help in expressing the semantics of the symbol.  

### Uninterpretable source

Sometimes, the data source gives a symbol, which was originally intended as 
precise, but one can not figure out which phoneme was meant. E.g. did "j" in a 
specific source mean IPA [y]"
or [j] ? Ideally, it is better to use a clearer source. But if it is impossible, 
then the best is to keep the original symbol (again, use the `name` and `comment` 
columns should clarify the situation). Indeed, interpreting as either "[y]" or "[j]" 
when unsure would add a layer of obscuration. 