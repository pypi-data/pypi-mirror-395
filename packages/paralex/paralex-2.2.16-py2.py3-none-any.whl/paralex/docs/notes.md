
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
to handle [sources](sources.md)), or to entries in other databases (which should be 
linked using URIs and identifiers).