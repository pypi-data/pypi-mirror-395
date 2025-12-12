#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides templates to render paralex metadata as markdown files.
"""
from pathlib import Path
from importlib import resources
import shutil
from .paths import templates_path
from contextlib import ExitStack, contextmanager

@contextmanager
def customTemplates(*files):
    flf = resources.files("frictionless")

    with ExitStack() as stack:

        replacements = [(templates_path / f,
                     stack.enter_context(resources.as_file(flf / f"assets/templates/{f}")),
                     stack.enter_context(resources.as_file(flf / f"assets/templates/{f}.tmp")))
                        for f in files]
        for custom, prev, tmp in replacements:
            shutil.copyfile(prev, tmp)
            shutil.copyfile(custom, prev)

        yield

        for custom, prev, tmp in replacements:
            shutil.copyfile(tmp, prev)
            Path(tmp).unlink()

def to_markdown(package, output_filename, title=None):
    yaml_lines = ["warning: This file was automatically generated, do NOT EDIT"]
    if title is not None:
        yaml_lines +=  ["title: "+title]
    yaml_lines= "\n    " + "\n    ".join(yaml_lines)

    with customTemplates("field.md", "package.md", "resource.md"):
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write("---"+yaml_lines+"\n---\n\n\n")
            f.write(package.to_markdown())
