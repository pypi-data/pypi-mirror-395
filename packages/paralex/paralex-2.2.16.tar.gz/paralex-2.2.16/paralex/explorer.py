#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides tool to read and download existing paralex data.
"""

import io
import json
from tqdm import tqdm
import tempfile
import zipfile
from pathlib import Path
import requests
import pandas as pd
import logging
from iso639 import Language, LanguageNotFoundError
from requests import request
# Our modules
from .paths import docs_path

log = logging.getLogger()
unknown = "*unknown*"


def _get_glottocode():
    glottolog_langs = "https://raw.githubusercontent.com/glottolog/glottolog-cldf/refs/tags/v5.1/cldf/languages.csv"
    glottocode = pd.read_csv(io.BytesIO(requests.get(glottolog_langs).content))
    return glottocode


def _save_record_files(record, directory, expected_files=None):
    """
    Save files from a Zenodo record.

    Arguments:
        record (dict): A Zenodo record.
        directory (str): Path to the directory where the files should be saved.
        expected_files: Set of file extensions to download. If None, downloads all files.
    """
    directory.mkdir(exist_ok=True, parents=True)
    files = []
    log.info('Downloading files from the Zenodo record.')
    for file in tqdm(requests.get(record["links"]["files"]).json()["entries"]):
        file_name = file["key"]
        file_link = file["links"]["content"]
        if file_name.endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(requests.get(file_link).content)) as zfile:
                zfile.extractall(directory)
                files.extend([f.filename for f in zfile.infolist()])
        elif (expected_files is None) or any(file_name.endswith(e) for e in expected_files):
            with (directory / file_name).open("wb") as f:
                f.write(requests.get(file_link).content)
                files.append(file_name)
    log.info('Files downloaded.')
    return files


def _get_zenodo_datasets():
    """
    Reads the list of available Paralex datasets from Zenodo.

    Returns:
        List[dict]: A list of JSON records.
    """
    log.info('Sending Zenodo request...')
    response = requests.get('https://zenodo.org/api/records',
                            params={'communities': 'paralex'})

    # TODO exit nicely in case of bad answer
    log.info('Received response from Zenodo')
    return response.json()["hits"]["hits"]


def _get_previous_data():
    """
    Tries to read the data from the last run.
    Exposed on the Paralex website.
    """

    ######### HACK TO GET LOCAL FILE
    # url = "http://localhost:8000/paralex/known-datasets.csv"
    url = "https://paralex-standard.org/known-datasets.csv"
    log.info('Fetching previous list of datasets.')
    try:
        df = pd.read_csv(url, index_col=0)
        return df
    except Exception as e:
        print(f"{e} occured while fetching {url}")
        return None


def _gather_dataset_info(glottolog_data, save=True, update=False):
    """
    Gets information on all datasets and stores in a DataFrame.

    Arguments:
        save (bool): Whether to save the dataframe as CSV
            or to return the object.
        update (bool): Whether to force update of the data.
    """
    old = _get_previous_data()
    records = _get_zenodo_datasets()
    data = []
    fields = ['id', 'permanent_id', 'name', 'lang', 'paralex_version', 'version', 'contributors', 'title', 'doi', 'comment']
    for record in records:
        rec_id = record['id']
        if (
                update
                or (old is None)
                or not (rec_id in old.index)
                or not ('permanent_id' in old.columns)):

            package_infos = _get_package_infos(record)

            ######### TEMPORARY HACK TO FAKE UPDATED DATASETS
            tmp_replacer = {"PrinParLat": ["lat"], "LatInfLexi": ["lat"], "LeFFI": ["ita"]}
            package_infos["lang"] = tmp_replacer.get(package_infos["name"], package_infos["lang"])
            ######### END TEMPORARY HACK TO FAKE UPDATED DATASETS

            data.append(package_infos)
        else:
            package_infos = old.loc[old.index == rec_id, :].reset_index().iloc[0].to_dict()
            package_infos = {key: value for key, value in package_infos.items() if key in fields}
            package_infos['lang'] = old.loc[old.index == rec_id, 'lang'].to_list()
            data.append(package_infos)
    data = pd.DataFrame(data).explode("lang").fillna(unknown).set_index('id')

    def get_language(lg):
        try:
            return Language.match(str(lg))
        except LanguageNotFoundError:
            log.warning(f"Language not found for key: {lg}")
            return None

    log.info('Matching language names.')
    data["language_norm"] = data["lang"].apply(get_language)
    glottolog_data["language_norm"] = glottolog_data["ISO639P3code"].apply(get_language)
    res = data.join(glottolog_data.set_index("language_norm").loc[:, ["Latitude", "Longitude", "Family_ID"]], "language_norm",
                    how="left")
    res['lang_name'] = res.language_norm.apply(lambda lang: lang.name if lang else unknown)
    # Normalize names
    res.columns = [c.lower() for c in res.columns]
    # Get family name
    lang_labels = dict(glottolog_data.loc[:, ["ID", "Name"]].to_records(index=False))
    res["family"] = res["family_id"].map(lang_labels)
    log.info('Finnished gathering datasets.')
    if save:
        res.to_csv(docs_path / "known-datasets.csv")
    else:
        return res


def _get_package_file(record):
    def load_json(filepath):
        try:
            with filepath.open(encoding="utf-8") as fp:
                return json.load(fp)
        except Exception as e:
            print(f"{e} occured at {filepath}")
        return {}

    def is_package_file(json):
        return json.get("profile", None) == "data-package"

    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = Path(tempdir)
        _save_record_files(record, tempdir, expected_files={".csv", ".json", ".md", ".bib"})  # Save all files to temp dir, unpacking zips

        # Search for json files
        files = list(tempdir.glob("*package.json"))
        if len(files) == 0:
            files = list(tempdir.glob("**/*.json"))

        # Find the package
        for file in files:
            md = load_json(file)
            if is_package_file(md):
                return md
    return None


def _get_package_infos(record):
    rec_id = record['id']
    pid = record['conceptrecid']
    doi = record["links"]["doi"]
    title = record["title"]
    log.info(f"Updating data for package '{title}'.")
    json_data = _get_package_file(record)
    if json_data is not None:
        return {"title": title,
                "id": rec_id,
                'permanent_id': pid,
                "doi": doi,
                "name": json_data.get("name", json_data.get("title", unknown)),
                "lang": json_data.get("languages_iso639", unknown),
                "version": json_data.get('version', unknown),
                "paralex_version": json_data.get("paralex-version", unknown),
                "contributors": ";".join(c["title"] for c in json_data["contributors"]),
                }

    return {"title": title,
            "id": rec_id,
            'permanent_id': pid,
            "doi": doi,
            "comment": "no valid metadata found"
            }


def list_datasets(args):
    """
    Provides a list of all Paralex datasets that are available
    """
    glottocode_data = _get_glottocode()
    df = _gather_dataset_info(glottocode_data, save=False, update = args.update)
    if args.iso:
        log.info('Returning datasets for ISO code %s only', args.iso)
        df = df[df.lang.isin(args.iso)]
    df = df[['permanent_id', 'doi', 'lang', 'lang_name', 'family', 'version', 'paralex_version']]
    if args.output:
        df.to_csv(args.output)
    print(df.to_markdown())

    log.info('You can download a specific dataset with `paralex get <ZENODO_ID>`')


def download_dataset(args):
    """
    Downloads a dataset and extracts the zip archive if necessary.
    """

    log.info('Fetching a list of files to download')
    out = args.output if args.output else f"{args.zenodo_id}/"
    headers = {"Content-Type": "application/json",
               "Accept": "application/vnd.inveniordm.v1+json"}
    try:
        response = request("GET", "https://zenodo.org/api/records/" + str(args.zenodo_id),
                           headers=headers)
        response.raise_for_status()
        _save_record_files(response.json(), Path(out))
    except requests.exceptions.RequestException as err:
        log.error(err)
