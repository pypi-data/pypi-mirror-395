#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides paths to various subfolders
"""
from pathlib import Path

standard_path = (Path(__file__).parent / "standard/").resolve()
templates_path = (Path(__file__).parent / "templates/").resolve()
docs_path = (Path(__file__).parent / "docs/").resolve()