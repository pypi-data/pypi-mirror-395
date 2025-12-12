This workflow tutorial takes you through the steps in order to create a paralex lexicon.

!!! info "Hints and tips"

    - In case you want to start a new dataset from a sample Paralex repository containing most of the files described below, have a look at our [blank dataset](https://finnic-morpho.gitlab.io/paralexmodel/) on GitLab.
    - If you are not familiar with `git` or [GitLab](https://gitlab.com/) and want to use these services as described below, you can find several [good tutorials](https://swcarpentry.github.io/git-novice/) on the internet. Using git is **not** required to conform to the Paralex standard.

## Creating the dataset

Creating the data is of course the hardest task. You have full freedom to do this in whatever way feels most practical or convenient for you and your team.
This might mean editing csv files directly in LibreOffice Calc or Microsoft Excel,
manipulating raw data using a programming language like R or Python, relying on some sort of database manager with a graphical interface, or anything else you can think of.
Before publication, you need to be able to export each table in `csv` format with a
utf-8 character encoding.


A minimal valid paralex dataset (which fulfills only the MUST statements of the standard) comprises a forms table which documents forms, and some metadata. [Here's a compliant example](https://gitlab.com/sbeniamine/paralex/-/tree/main/paralex/docs/examples/minimal).

To fulfill all the SHOULDs, a dataset only needs to add a few tables (sounds, feature-values, cells), as well as a data sheet.

The set of pre-defined tables are described in the [description of the standard](standard.md) and the [specs](specs.md).  Any additional
ad-hoc tables and columns can be added as necessary.

If you provide many lexemes and cells, the forms table can grow very big. In such a case, the [frictionless specification](https://specs.frictionlessdata.io/data-resource/#data-in-multiple-files) allows any tables to be separated in several files, provided that they have the exact same structure.  [Here's a compliant example of a minimal dataset with multiple files for the forms tables](https://gitlab.com/sbeniamine/paralex/-/tree/main/paralex/docs/examples/multipath)

## Metadata quick start

A package requires [metadata](metadata.md). In our case, this is a [frictionless]((https://frictionlessdata.io/) compliant `json` file, with a name conventionally ending in *.package.json*. A "paralex package" is the set of all your tables, documentation, and metadata.

First, install `paralex`. This can be done from the command line, for example as follows:

```bash title="Installing paralex"
pip3 install paralex
```

Second, specify some basic metadata by creating a `yaml` configuration file:

```yaml title="paralex-infos.yml"
title: French Verbal Paradigms
contributors:
  - title: 'author name'
languages_iso639: 
  - fra
files:
  forms:
    path: "french_v_forms.csv"
name: french
```

This configuration file provides a title for your paralex dataset, a short name (in lowercase), and a single table for forms, with the path to the file holding that csv table. 

Third, use `paralex` to generate the metadata, and write it to `french.package.json`, by executing:

```bash title="Generating metadata"
paralex meta paralex-infos.yml
```

This is enough to obtain a well formed paralex dataset, although it is possible to generate more [advanced metadata](advanced-metadata.md)

## Ensuring high quality data

### Frictionless validation

The metadata generated above, and saved in the json file `french.package.json` can now be used to [validate the dataset using frictionless](https://frictionlessdata.io/software/#software-toolkit). Frictionless should have been installed as a dependency when you installed `paralex`. You can now run:

```bash title="Checking against the metadata"
frictionless validate french.package.json
```

This will check that all the tables exist and are well formed, and that columns
contain the types and contents declared by the metadata file, and that any constraints
on columns (such as being a value from a specific set of predefined values, being
unique, being obligatory, having maximum or minimum values, etc) are respected. Note that
the following requirements will also be checked for:

- All identifiers MUST be unique, that is to say, no two rows in their table has the
  same value in `form_id`, `cell_id`, `lexeme_id`, `feature_id`, or `sound_id`.
- All values in the `cell` column of the forms MUST correspond to an identifier in
  `cell_id` of the `cells` table if it exists;
- All values in the `lexeme` column of the forms MUST correspond to an identifier
  in `lexeme_id` of the `lexemes` table if it exists
- If there is a `sounds` table, then the `phon_form` in `forms` MUST be
  composed
  only of sound identifiers and spaces.
- If there is a `cells` table and a `features` table, then the `cell_id` in `cells`
  MUST be composed only of feature identifiers found in `feature_id`, separated by dots, following the Leipzig glossing rules convention.

### Paralex validation

To check that the dataset is in fact a paralex lexicon, you can use the `paralex validate` command as follows:

```bash title="Checking against the standard itself"
paralex validate french.package.json
```

This attempts to check all of the MUST and SHOULD statements from the [standard](standard.md). 

### Testing

Some more constraints can be expressed in the package metadata, see the [frictionless doc on constraints](https://specs.frictionlessdata.io/table-schema/#constraints) and [advanced metadata](advanced-metadata.md).

For more custom checks, we recommend writing
*tests* in the programming language of your choice.

### Continuous pipelines

Validation and testing can be setup to run each time the data changes, if you track your data using git and push it either to gitlab or github.

=== "Pipelines with gitlab"
    
    With gitlab, create a plain text file called `.gitlab-ci.yml`, with the following content:

    ``` yaml title=".gitlab-ci.yml"
    image: python:3.8
    
    validate:
      stage: test
      script:
        - pip install frictionless paralex
        - frictionless validate *.package.json
        - paralex validate *.package.json
    ```

=== "Pipelines with github"
    
    With github, create a plain text file (yaml formatted) in a 
    folder `.github/workflows/`, called for example `validation.yml`, with the following content:

    ``` yaml title=".github/workflows/validation.yml"
    name: Validate
    
    on:
      push:
        branches: [ "main" ]
    
    jobs:
      validate:
        name: Validation
        runs-on: ubuntu-latest
        strategy:
          fail-fast: false
    
        steps:
          - uses: actions/checkout@v3
          - name: Set up Python 3.11
            uses: actions/setup-python@v3
            with:
              python-version: 3.11
          - name: Install dependencies
            run: |
              python -m pip install --upgrade pip
              pip install frictionless paralex
          - name: validate
            run: |
              frictionless validate *.package.json
              paralex validate *.package.json
    ```

## Publishing

### The raw data files

We recommend publishing the completed dataset as an online repository, such as on github or gitlab.

The repository should contain all the relevant files: 

- the data, in the form of csv tables
- the metadata, in the form of a json file (this is a frictionless _package_ file)
- the documentation files, at the minimum a README.md file
- a license file
- the config file `paralex-infos.yml` or the metadata python script `gen-metadata.py`
- the tests if they exist
- when relevant, possible, legal, and practical: a link to any automated process used to generate the data, or any related repository used to generate it.

When using git, a simple way to do this is the `git archive` command. For example, the following command will create a zip archive for a repository at the current revision (HEAD):

```shell
git archive -o french_verbs.zip HEAD
```

Only files versionned with git will be included, but they will all be included. To exclude some files, use a [`.gitattributes` file](https://git-scm.com/docs/gitattributes). Here is an example:

```gitexclude title=".gitattributes"
.zenodo.json       export-ignore
.gitlab-ci.yml     export-ignore
.gitattributes     export-ignore
.gitignore     export-ignore
mkdocs.yml     export-ignore
```

### Revisable, automatically generated sites

You can use [mkdocs-paralex](https://pypi.org/project/mkdocs-paralex-plugin/) to generate a website automatically using [mkdocs](https://www.mkdocs.org/). This software is currently in beta mode: it is not stable and might have critical bugs. If you find any, please make issues or write us an email.

Your repository needs to have pipelines and pages enabled. 

First, create a configuration file for [mkdocs](https://www.mkdocs.org/user-guide/), compatible with [mkdocs-material](https://squidfunk.github.io/mkdocs-material/). 

It needs a special `paralex` section, with minimally a `paralex_package_path` (to the json file), lists of feature labels to use to separate tables, rows and columns. It can contain 

``` yaml title="mkdocs.yml"
site_name: "My site name"
docs_dir: docs
plugins:
  - paralex:
      paralex_package_path: "<name>.package.json"
      layout_tables:
        - mood
      layout_rows:
        -  person/number
      layout_columns:
        - tense
repo_url: https://gitlab.com/<user>/<repo>
```

If your lexicon is massive, the generated site might exceed the free hosting capacity on gitlab or github. You can then add two more keys under the paralex section. If `sample_size` is set, the corresponding number of lexemes will be selected, and the site will only show that sample. If `frequency_sample` is set to `true`, then the chosen lexemes will be the most frequent.

``` yaml title="mkdocs.yml"
site_name: "My site name"
docs_dir: docs
plugins:
  - paralex:
      paralex_package_path: "<name>.package.json"
      sample_size: 5000
      frequency_sample: true
      layout_tables:
        - mood
      layout_rows:
        -  person/number
      layout_columns:
        - tense
repo_url: https://gitlab.com/<user>/<repo>
```

To generate the site, add a pipeline file:

=== "gitlab pages"
    
    With gitlab, create a plain text file called `.gitlab-ci.yml`, with the following content. The site will then be served at `https://<username>.gitlab.io/<repository-name>`. For more on gitlab pages, see [the gitlab pages docs](https://docs.gitlab.com/ee/user/project/pages/). 

    ``` yaml title=".gitlab-ci.yml"
    image: python:3.8

    pages:
      stage: deploy
      script:
        - mkdir -p docs/
        - pip install pandas mkdocs>=1.1.2 mkdocs-material mkdocs_paralex_plugin
        - mkdocs build -d public/ --strict --verbose
      artifacts:
        paths:
          - public/
      only:
        - master
    ```

=== "github pages"
    
    With github, create a plain text file (yaml formatted) in a folder `.github/workflows/`, called for example `pages.yml`. 
    You need to activate github pages through actions in the repository setting on the github site.
    The site will then be served at `https://<username>.github.io/<repository-name>`. 
    For more on github pages, see [the github pages docs](https://docs.github.com/en/pages). 

    ``` yaml title=".github/workflows/pages.yml"
    name: Pages
    
    on:
      push:
        branches: [ "main" ]
        
    permissions:
      contents: read
      pages: write
      id-token: write

    jobs:
      build:
        name: Deploy site
        runs-on: ubuntu-latest
        steps:
          - name: Checkout main
            uses: actions/checkout@v3
          - name: Set up Python 3.11
            uses: actions/setup-python@v3
            with:
              python-version: 3.11
          - name: Install dependencies
            run: |
              python -m pip install --upgrade pip
              pip install pandas mkdocs>=1.1.2 mkdocs-material mkdocs_paralex_plugin
          - name: Setup Pages
            id: pages
            uses: actions/configure-pages@v5
          - name: Build with mkdir
            run: |
              mkdir -p docs/
              mkdocs build -d public/ --strict --verbose
          - name: Upload artifact
            uses: actions/upload-pages-artifact@v3
            with:
              path: ./public
    
      deploy:
        environment:
          name: github-pages
          url: ${{ steps.deployment.outputs.page_url }}
        runs-on: ubuntu-latest
        needs: build
        steps:
          - name: Deploy to GitHub Pages
            id: deployment
            uses: actions/deploy-pages@v4
    ```

Here are some examples of such generated sites:

- [Eesthetic: Estonian N and V](https://sbeniamine.gitlab.io/estonianparadigms/)
- [Aravelex: Arabic V](https://sbeniamine.gitlab.io/aravelex)
- [VeLePo: European Portuguese V](https://sbeniamine.gitlab.io/europeanportugueseverbs/)
- [Vlexique: French V](https://sbeniamine.gitlab.io/vlexique)
- [Ngkolmpu](https://maecarroll.github.io/Ngkolmpu-Paralex/) (github pages)


## Archiving

We recommend archiving the data by creating a record on some archival service, for
example [zenodo](https://zenodo.org/). A good practice would be to set up automatic
archives for new versions. This can be done natively from github, or can be done using
[gitlab2zenodo](https://pypi.org/project/gitlab2zenodo/).

To have a DOI generated by zenodo in the metadata, first make a draft deposit, filling in the metadata, and checking the box for pre-registering a DOI. Then copy this DOI, add it to your README.md file and your metadata, generate an archive, and upload this to zenodo before publishing the record.

To have your dataset officially listed as a paralex lexicon, add it to the [Paralex zenodo community](https://zenodo.org/communities/paralex/)

