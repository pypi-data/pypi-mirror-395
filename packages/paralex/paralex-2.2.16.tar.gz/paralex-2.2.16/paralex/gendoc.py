#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module generates standard files & documentation.
"""
import json
import re
from itertools import chain
from types import SimpleNamespace

import frictionless as fl
import pandas as pd
import seaborn as sns

# Our modules
from . import VERSION
from .markdown import to_markdown
from .meta import package_from_kwargs, gen_metadata
from .paths import docs_path, standard_path
from .explorer import _gather_dataset_info, _get_glottocode, unknown

import logging

log = logging.getLogger()


def _make_standard_package(*args, **kwargs):
    with (standard_path / "package_spec.json").open('r', encoding="utf-8") as flow:
        package_infos = json.load(flow)
        package_infos["version"] = VERSION

    with (standard_path / "columns_spec.json").open('r', encoding="utf-8") as flow:
        columns = json.load(flow)

    with (standard_path / "files_spec.json").open('r', encoding="utf-8") as flow:
        resources = json.load(flow)["resources"]

    new_resources = []
    for res in resources:
        # replace column names by their full definition
        if res["path"].endswith(".csv"):
            res["schema"]["fields"] = [dict(columns[f]) for f in res["schema"]["fields"]]

        if res["name"] == "forms":
            for col in res["schema"]["fields"]:
                if col["name"] in ["lexeme", "cell"]:
                    col["constraints"] = {"required": True}

        new_resources.append(fl.Resource(res))

    package = package_from_kwargs(resources=new_resources, **package_infos)

    package.to_json(str(standard_path / "paralex.package.json"))


def _build_stats(df, glottocode_data):
    include_path = docs_path / "includes"
    include_path.mkdir(parents=True, exist_ok=True)

    stats = {"summary_pie.md": _summary_family_pie,
             "summary_wanted_fam.md": _summary_wanted_fam,
             "summary_wanted_50.md": _summary_wanted_50,
             "summary_contributors.md": _summary_contributors,
             }

    for name, func in stats.items():
        md = func(df, glottocode_data)
        with (include_path / name).open("w") as f:
            f.write(md)


def _summary_contributors(df, *args, **kwargs):
    def sorter(word):
        word = word.strip()
        m = re.match(r"^.+? [A-Z][^.]", word)
        if not m:
            return word
        return word[m.span()[1] - 2:]

    authors = set(chain(*(c.split(";") for c in df["contributors"])))
    authors - {unknown}
    return "**Dataset contributors: **" + ", ".join(sorted(authors, key=sorter))


def _summary_wanted_50(df, glottolog_data):
    stats = pd.read_csv(docs_path / "language_stats.csv")
    stats_gl = glottolog_data[glottolog_data.Name.isin(stats.Language)].set_index('Name')[
        'Closest_ISO369P3code'].to_dict()
    stats['ISO 693'] = stats.Language.map(stats_gl)
    missing = stats[~stats['ISO 693'].isin(df.lang)].iloc[0:5]
    return missing.set_index("ISO 693").to_markdown()


def _summary_wanted_fam(df, glottolog_data):

    blacklist = {
        'book1242',
        'sign1238'}

    covered = set(df.family_id.unique())
    lang_labels = dict(glottolog_data.loc[:, ["ID", "Name"]].to_records(index=False))
    fams = glottolog_data.groupby('Family_ID').size().sort_values(ascending=False)
    fams = fams[~fams.index.isin(covered | blacklist)].iloc[0:5]
    fams.index = fams.index.map(lang_labels)
    fams.index.name = "Language family"
    fams.name = "Number of languages in Glottolog"
    md = fams.to_markdown()
    return md


def _summary_family_pie(df, glottocode_data):
    """Family distribution pie"""
    fams = df.groupby(['color', 'family']).apply(len)
    fams.name = "nb"
    fams = fams.to_frame().reset_index()
    idx = fams.family.to_list()
    values = fams.nb.to_list()
    color = fams.color.to_list()
    mermaid = """
<div style="height: 300px;">
  <canvas id="myChart"></canvas>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<script>
  const ctx = document.getElementById('myChart');

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: """ + str(idx) + """,
      datasets: [{
        backgroundColor: """ + str(color) + """,
        label: 'Number of datasets',
        data: """ + str(values) + """,
      }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
  });
</script>

"""
    # for key, value in family_pct.items():
    #     mermaid += f'\n    "{key}": {value}'
    return mermaid


def _build_json(df):
    geojson = {"type": "FeatureCollection", "features": []}

    for _, row in df.dropna(subset=['longitude', 'latitude']).iterrows():
        feature = {"type": "Feature",
                   "geometry": {"type": "Point",
                                "coordinates": [row['longitude'], row['latitude']]
                                }
                   }

        feature['properties'] = {key: row[key] for key in row.index.values[1:]
                                 if key not in ['longitude', 'latitude']}
        geojson['features'].append(feature)

    with (docs_path / 'result.geojson').open('w') as fp:
        json.dump(geojson, fp)


def _build_summaries(glottocode_data):
    """Builds all the summaries from the dataframe of datasets."""
    df = pd.read_csv(docs_path / 'known-datasets.csv')
    # Assign a color to each family
    nitems = df['family_id'].nunique()
    col = sns.color_palette("hls", nitems).as_hex()
    df['color'] = df.groupby(by='family_id').ngroup().apply(lambda x: col[int(x)] if not pd.isna(x) else None)

    _build_json(df)
    _build_stats(df, glottocode_data)


def _write_doc(*args, **kwargs):
    to_markdown(fl.Package(standard_path / "paralex.package.json"),
                docs_path / "specs.md")

    # generate json files for examples
    examples_dir = docs_path / "examples"
    for directory in examples_dir.glob("*/"):
        gen_metadata(SimpleNamespace(config=directory / "paralex-infos.yml", basepath=directory))
    glottocode_data = _get_glottocode()
    _gather_dataset_info(glottocode_data)
    _build_summaries(glottocode_data)
