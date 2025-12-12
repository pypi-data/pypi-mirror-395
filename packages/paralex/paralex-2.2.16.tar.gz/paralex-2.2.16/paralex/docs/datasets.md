Typological studies require datasets that represent the diversity of the languages of the world. However, Paralex datasets, as is often the case with corpora, tend to be biased towards Indo-European languages. Many large language families are not even represented. If you have some language data that could extend the coverage of Paralex datasets, converting it to the standard would be an invaluable contribution.

## Accessing datasets

Most Paralex datasets are released on the Paralex Zenodo community. The Zenodo community allows to browse current datasets, retrieve the metadata and download the files.

[Download the datasets on Zenodo](https://zenodo.org/communities/paralex/){ .md-button }

The `paralex` package also provides a simple command line interface to browse and download datasets:

``` bash
paralex list # Returns all available datasets*
paralex get <ZENODO_ID> --output <PATH>  # Downloads the dataset with id ZENODO_ID to PATH
```

??? advice "Optional arguments"
    `list` accepts the following arguments:

    - `--iso <ISO>` (followed by iso codes) filters the list of datasets and displays only matching datasets.
    - `-o/--output <PATH>` saves the dataset list as a CSV table to `PATH`.
    - `-u/--update` forces update of all the metadata. The command takes longer to complete.

    `get` accepts the following arguments:

    - `-o/--output <PATH>` saves the dataset list as a CSV table to `PATH`.

## Existing datasets

### Coverage

<iframe src="../mapframe.html" height="650" width="100%" marginheight="0" frameborder="0" border="0"></iframe>

The chart below shows the current language family coverage of Paralex.

{% include "includes/summary_pie.md" %}

{% include "includes/summary_contributors.md" %}

## Missing languages

The table below lists the 5 largest language families (according to Glottolog) that are not represented at all in Paralex datasets.

{% include "includes/summary_wanted_fam.md" %}

The 5 largest languages with more than 50 millions of L1 speakers that are not covered in Paralex:

{% include "includes/summary_wanted_50.md" %}

*These statistics are automatically extracted from the [Paralex Zenodo community](https://zenodo.org/communities/paralex/). The source for the number of speakers is Ethnolog (2024).*
