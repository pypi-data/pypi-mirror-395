#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module manipulates frictionless metadata.
"""
import collections.abc
import inspect
import json
import yaml
import logging
import re
from collections import defaultdict
from pathlib import Path
import frictionless as fl

from .utils import read_table_from_paths
from . import standard_path, VERSION

relations = ["isCitedBy", "cites", "isSupplementTo", "isSupplementedBy", "isContinuedBy", "continues", "isDescribedBy",
             "describes", "hasMetadata", "isMetadataFor", "isNewVersionOf", "isPreviousVersionOf", "isPartOf",
             "hasPart", "isReferencedBy", "references", "isDocumentedBy", "documents", "isCompiledBy", "compiles",
             "isVariantFormOf", "isOriginalFormof", "isIdenticalTo", "isAlternateIdentifier", "isReviewedBy", "reviews",
             "isDerivedFrom", "isSourceOf", "requires", "isRequiredBy", "isObsoletedBy", "obsoletes"]
resource_name_pattern = re.compile(r'^([-a-z0-9._/])+$')


def gen_metadata(args):
    with open(args.config, 'r') as infile:
        config = yaml.safe_load(infile)

    if args.basepath:
        basepath = Path(args.basepath)
    elif "basepath" in config.keys():
        # Keeping this for backward compatibility.
        logging.warning("Specifying the basepath in the config file is deprecated. Use the --basepath argument instead.")
        basepath = Path(config['basepath'])
    else:
        logging.warning("No basepath was passed. Using the YAML config file location.")
        basepath = Path(args.config).parent
    config['basepath'] = str(basepath.resolve())
    path = basepath.resolve() / f"{config['name']}.package.json"

    package = paralex_factory(**config)
    logging.info('Writing the package definition to %s', path)
    package.to_json(path)


def _to_pattern(iterable, sep="", diacritics=None):
    iterable = sorted(iterable, key=len, reverse=True)
    items = "|".join(iterable)
    if diacritics is None or not diacritics:
        char = f"({items})"
    else:
        diacs = "|".join(diacritics)
        char = f"(({diacs})*({items})({diacs})*)"

    if sep == "":
        return f"{char}+"
    else:
        return f"{char}({sep}{char})*"


def _get_default_package(basepath=""):
    """ Instantiate a default paralex frictionless package

    This uses the paralex json file, removing specific instance information
    (version, name, contributors, related_identifiers).

    Returns (fl.Package): a default package for paralex lexicons

    """
    default_to_remove = ["version", "name", "contributors"]
    default = json.load((standard_path / "paralex.package.json").open("r", encoding="utf-8"))

    # Remove default dummy values in package
    for key in default_to_remove:
        del default[key]
    return fl.Package(default, basepath=basepath)


def default_update(specific, default):
    """ Update a default package with specific information.

    The behaviour is as follows:
        - For the "Fields" list, append any extra column from default
         which are not already specified in the specific information
        - Otherwise for all mappings: recursively update
        - Otherwise add information from default if it does not exist in specific.

    Args:
        specific (dict): specific information (user specified)
        default (dict): default information (from paralex standard)

    Returns:
        a dictionary of the default information, updated with the specific information.

    """
    for k, v in default.items():
        if isinstance(v, list) and k == "fields":
            cols = specific.get(k, [])
            specific[k] = cols + list(filter(lambda c: c not in cols, v))
        if isinstance(v, collections.abc.Mapping):
            specific[k] = default_update(specific.get(k, {}), v)
        elif specific.get(k, None) is None:
            specific[k] = v
    return specific


def package_from_kwargs(basepath=False, **kwargs):
    """
    Arguments:
        basepath (str): Absolute path where the metadata file will be stored.

    Returns:
        frictionless package
    """
    if not basepath:
        logging.warning('No basepath was passed, assuming current location.')
        basepath = str(Path().resolve())

    # Separate kwargs between pre-defined ones and custom ones
    defined = {x.name: kwargs[x.name] for x in fl.Package.__attrs_attrs__ if x.name in kwargs}
    custom = {k: kwargs[k] for k in kwargs if k not in defined}
    p = fl.Package(**defined, basepath=basepath)
    p.custom.update(custom)
    return p


def paralex_factory(title, files=None, tables=None, **kwargs):
    """ Generate frictionless metadata for this paralex lexicon.

    Use the default package, fillin-in user specified information.
        Keeps only existing tables,
        updates foreign keys and table relations according to which tables are
        declared.

    Args:
        title (str): a title for the package
        files (dict): dictionary of file names to resource information
        tables (dict): deprecated, see `files`
        **kwargs:

    Returns:

    """
    ## Update package infos
    kwargs["title"] = title
    if files is None:
        if tables is None:
            raise ValueError("Paralex package must have some files (tables, etc).")
        files = tables
        logging.warning("Deprecated ! As of Paralex v.2.0.8,"
                        " the `tables` keyword is deprecated in config files, "
                        "and replaced by `files`.")

    # Get a frictionless package instantiated from the standard json
    default_package = _get_default_package()
    default_package_infos = default_package.to_dict()
    del default_package_infos["resources"]
    default_update(kwargs, default_package_infos)
    p = package_from_kwargs(**kwargs)

    ## Update resources infos
    default_resources = set(default_package.resource_names)
    resources = set(files)
    added_resources = resources - default_resources
    missing_resources = default_resources - resources

    for res in resources:
        if resource_name_pattern.match(res) is None:
            suggested = re.sub("[^-a-z0-9._/]", "", res.lower())
            raise ValueError(f"Table name {repr(res)} is invalid. "
                             "\nTable names can only contain '-', '_', '.', "
                             "numbers or lowercase latin letters. "
                             f"Try instead something like:\n\tparalex_factory({title}, "
                             "{"
                             f" ... '{suggested}': {files[res]} ... "
                             "} ... )")
        res_metadata = files[res]
        res_metadata["name"] = res

        # Grabbing just the first path, assuming resources are homogeneous !
        path = res_metadata["path"]
        path = path[0] if isinstance(path, list) else path

        if res in added_resources:
            logging.warning(f"Adding a table which is not "
                            f"specified in the standard: {repr(res)}.\n\t"
                            f"Did you mean one of: `{'`, `'.join(missing_resources)}`?")
        else:
            default_table = default_package.get_resource(res)
            default_update(res_metadata, default_table.to_dict())

        if path.endswith(".csv"):
            table_contents = read_table_from_paths(res_metadata["path"], p)
            cols = list(table_contents.columns)

            def foreign_key_exists(key_spec):
                table_ref = key_spec["reference"]["resource"]
                col_names = key_spec["fields"]
                return table_ref in resources and all(c in cols for c in col_names)

            ## Adjust foreign keys according to existing tables
            fkeys = list(filter(foreign_key_exists,
                                res_metadata.get("schema", {}).get("foreignKeys", [])))
            if fkeys:
                res_metadata["schema"]["foreignKeys"] = fkeys
            elif "schema" in res_metadata and "foreignKeys" in res_metadata["schema"]:
                del res_metadata["schema"]["foreignKeys"]

            # Remove standard columns which are not present
            if "schema" in res_metadata:
                new_table_fields = list(res_metadata["schema"]["fields"])
                for field in res_metadata["schema"]["fields"]:
                    if field["name"] not in cols:
                        new_table_fields.remove(field)
                res_metadata["schema"]["fields"] = new_table_fields

        r = fl.Resource(res_metadata, detector=fl.Detector(schema_sync=True))

        p.add_resource(r)

    ## Set Foreign keys for tags

    taggable_tables = {"forms", "lexeme", "frequencies"} & resources

    for tab_name in taggable_tables:
        res = p.get_resource(tab_name)
        tag_cols = {col for col in res.schema.field_names
                    if col.endswith("_tag")}
        if tag_cols:
            if "tags" not in resources:
                logging.warning(f"You have tag columns ({', '.join(tag_cols)}) "
                                f"in table {tab_name},"
                                f"but no tags table.")
            else:
                by_tag = defaultdict(list)
                for r in p.get_resource("tags").read_rows():
                    by_tag[r["tag_column_name"]].append(r["tag_id"])
                for col in tag_cols:
                    if col not in by_tag:
                        logging.warning(f"No tags defined for column {col} in table {tab_name}. "
                                        f"Please edit the tags table.")
                    else:
                        col_def = res.schema.get_field(col)
                        constraints = col_def.constraints
                        constraints["pattern"] = _to_pattern(by_tag[col], sep="\\|")
                        col_def.constraints = constraints

    forms_table = p.get_resource("forms")

    # Set pattern for orth_form
    if {"graphemes", "forms"} <= resources \
            and forms_table.schema.has_field("orth_form"):
        graphemes = [r["grapheme_id"] for r in p.get_resource("graphemes").read_rows()]
        form = forms_table.schema.get_field("orth_form")
        constraints = getattr(form, "constraints")
        constraints["pattern"] = _to_pattern(graphemes, sep="")
        form.constraints = constraints

    # Set pattern for phon_form
    if {"sounds", "forms"} <= resources \
            and forms_table.schema.has_field("phon_form"):
        seg = []
        supra_seg = []
        for row in p.get_resource("sounds").read_rows():
            s = row["sound_id"]
            if s.startswith("#") or s.endswith("#"):
                continue
            if row.get("tier", "segmental") == "segmental":
                seg.append(s)
            else:
                supra_seg.append(s)
        form = forms_table.schema.get_field("phon_form")
        constraints = form.constraints
        constraints["pattern"] = _to_pattern(seg, diacritics=supra_seg, sep=" ")

    # Set pattern for cells identifiers (combinations of features)
    if {"cells", "features-values"} <= resources:
        features = [r["value_id"] for r in p.get_resource("features-values").read_rows()]
        cell_id = p.get_resource("cells").schema.get_field("cell_id")
        constraints = cell_id.constraints
        constraints["pattern"] = _to_pattern(features, sep=r"\.")

    p.infer()
    p.custom["paralex-version"] = VERSION

    p.resources.sort(key=lambda x: (x.format, x.name))
    return p
