
## DeAR

Beyond users and speakers, language data also needs to be planned in ways that are good for the dataset authors. Thus, we introduced the **DeAR** principles:

### **De**centralized

Data is decentralised with no single team or institution operating a central database. 
The standard serves as a format to **share** data and as a means for researchers to 
create interoperable data of high-quality. We wish to make the standard 
as easy to use as possible, and to useful tools to its users.


###  **A**utomated verification

Data is [tested automatically](tutorial.md#Validating)
against the descriptions in the metadata in order to guarantee data quality. Moreover,
data quality can be checked by writing
custom [tests](tutorial.md#Testing) (as is done in software development), which are run
after each change of the data. 

### **R**evisable pipelines

Dataset authors must be able to continuously update
data presentation, in particular websites, reflecting the evolving nature of data. This is achieved by generating those
publications automatically and directly from the standardized dataset. We will create automated tools
which can generate user-friendly views of the data (for example static
websites, publication ready pdfs, etc.). These can be run again at any point, so that 
it is easy to re-generate those from the data edited by the researchers.

Both principes **A** and **R** fit particularly well with the use of versioning
systems such as [git](https://git-scm.com/), where validation, testing and publishing can be done through
continuous development pipelines.
