Our standard aims to meet the FAIR and CARE principles, and adds a few of our own, the DeAR principles. Paralex was inspired by the [
Cross-Linguistic Data Formats
(CLDF)](https://cldf.clld.org/) standard, and adheres to a similar philosophy and the same the design principles.

## FAIR

The [FAIR principles](https://www.go-fair.org/fair-principles/) are meant to ensure that datasets are both readable by machines
and by humans across sub-fields, disciplines and time. Here is a very short summary of the FAIR principles and how this standard aims to meet them:

###  **F**indable

Data must have a persistent global identifier (F1), be described by rich metadata (F2) which include the identifier (F3), and be indexed in searchable resources (F4).

- F1: Use Digital Object Identifiers, generated either by your institution or a repository. We suggest using [zenodo](https://zenodo.org/) for this and archiving.
- F2/F3: Add [json](https://en.wikipedia.org/wiki/JSON) metadata, following the [frictionless](http://frictionlessdata.io/) standard. The metadata
  refer to the DOIs.
- F4: Archive the dataset [on zenodo](https://zenodo.org/), on your institutional repository and/or on any repository of your choice. 

### **A**ccessible

The data and metadata can be reached using the identifier, and metadata persist even if the data is not accessible anymore. This is mostly achieved by using DOIs, and ensuring long term archiving.

### **I**nteroperable

Use a formal, accessible, shared, broadly applicable language for knowledge representation (I1), use FAIR vocabularies (I2) and refer to other (meta)data (I3).

- I1: We write the metadata in [json](https://en.wikipedia.org/wiki/JSON), the tables in [csv](https://frictionlessdata.io/blog/2018/07/09/csv/), and respect the [frictionless](frictionlessdata.io/) standard
- I2: The standard documents our conventions and columns, providing a FAIR vocabulary.
- I2/I3: The standard comes with built-in linking to other resources and encourages references to other resources and linking to other vocabularies such as [gold ontology](http://linguistics-ontology.org/gold),  [unimorph schema](https://unimorph.github.io/schema/), [universal dependency tagset](https://universaldependencies.org/u/overview/morphology.html), [CLTS' BIPA](https://clts.clld.org/contributions/bipa), [glottocodes](https://glottolog.org/), [ISO codes for languages](https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes), etc.

###**R**eusable

Data should be well described (R1) so that they can be re-used and combined in other contexts. This standard's main aim is to ensure that the data is richly and consistently described.


Because the FAIR principles make sure the data is widely shared and reused, and usable computationally, they focus on **data users**. However, two more group of people are relevant when producing language datasets.

## CARE

The [CARE Principles for Indigenous Data Governance](https://www.gida-global.org/care) focus on the interests of the language communities whose languages are described by our datasets. They are meant to be compatible with FAIR principles. These are not principles that can be fullfilled simply by adhering to a formal standard, but rather require careful planning and engagement with language communities. In short, they state:

### *C*ollective Benefit:

> "Data ecosystems shall be designed and function in ways that enable Indigenous Peoples to derive benefit from the data."

In the case of language data, native speakers should ideally be involved in the creation and authorship of resources, and the data should be made available in ways that are useful for language communities (such as the creation of pedagogical supports, dictionaries or grammar books).

### **A**uthority to control

Indigenous people must have control over how data is shared and how their culture is represented and identified. In particular, we should use endonyms and only distribute data openly with the consent of language communities.

### **R**esponsibility

Be accountable to how the data is used in favor of Indigenous people.

### **E**thics

> "Indigenous Peoples’ rights and wellbeing should be the primary concern at all stages of the data life cycle and across the data ecosystem."

- Ensure your data does not stigmatize Indigenous People and cultures, explicitly assess harms and benefits.
- Describe limitations, provenances, and purposes of the data
- Ensure long term preservation

The principles invite us to question how language communities can benefit from our work, and to consider that even as authors of datasets, it is not **our** data.
