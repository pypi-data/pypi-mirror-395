#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Handles command line interface
"""
import argparse
from .gendoc import _make_standard_package, _write_doc
from .validate import paralex_validation
from .meta import gen_metadata
from .explorer import list_datasets, download_dataset
import logging

logging.basicConfig(level=logging.INFO)


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands',
                                       description='Valid subcommands')

    # Subparser to build the standard
    make_std = subparsers.add_parser("make_standard",
                                     help='Builds the Paralex standard.')
    make_std.set_defaults(func=_make_standard_package)
    make_doc = subparsers.add_parser("make_doc")
    make_doc.set_defaults(func=_write_doc)

    # Subparser to validate a package
    validate = subparsers.add_parser("validate",
                                     help='Validates a Paralex package against a JSON file.')
    validate.add_argument("package", help="JSON description of the package to validate")
    validate.add_argument('--basepath', type=str,
                          help='Basepath for the package to validate.')
    validate.set_defaults(func=paralex_validation)

    # Subparser to generate metadata
    meta = subparsers.add_parser("meta",
                                 help='Generates a JSON descriptor from a YAML file.')
    meta.add_argument("config", help="YAML description of the package to describe.")
    meta.add_argument('--basepath', type=str,
                      help='Basepath for the generated .package.json file.')
    meta.set_defaults(func=gen_metadata)

    # Subparser to gather dataset info
    gather = subparsers.add_parser("list",
                                   help='Lists all available Paralex datasets.')
    gather.add_argument("--iso", action="extend", nargs="+", type=str, help="Language codes to catch.")
    gather.add_argument("-o", '--output', type=str, help="Output file. Saves the data to a CSV file.")
    gather.add_argument("-u", '--update', help="Force update of all the dataset metadata.",
                        action="store_true", default=False)
    gather.set_defaults(func=list_datasets)

    # Subparser to download a dataset
    get = subparsers.add_parser("get",
                                help='Downloads a Paralex dataset.')
    get.add_argument("zenodo_id", type=str, help="Zenodo ID of the dataset to download.")
    get.add_argument("-o", '--output', type=str, help="Output folder. Defaults to working directory")
    get.set_defaults(func=download_dataset)
    return parser.parse_args()


logo = r"""
 &&&&&&&&&&&&&&&&&
&                 &      /#######                              /##
&  ---  ---  ---  &     | ##__  ##                            | ##
&  ---  ---  ---  &     | ##  \ ## /######   /######  /###### | ##  /######  /##   /##
&  ---  ---  ---  &     | #######/|____  ## /##__  ##|____  ##| ## /##__  ##|  ## /##/
&                 &     | ##____/  /#######| ##  \__/ /#######| ##| ######## \  ####/
 &&&&&&&&&&&&&&   &     | ##      /##__  ##| ##      /##__  ##| ##| ##_____/  >##  ##
               &  &     | ##     |  #######| ##     |  #######| ##|  ####### /##/\  ##
                 &&     |__/      \_______/|__/      \_______/|__/ \_______/|__/  \__/

"""


def main():
    args = parse_args()
    if len(args.__dict__) == 0:
        print(logo + 'Please type "paralex --help" to display available commands.')
    else:
        args.func(args)
