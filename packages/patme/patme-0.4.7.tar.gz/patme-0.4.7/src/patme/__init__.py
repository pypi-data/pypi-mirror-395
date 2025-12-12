# Copyright (C) 2020 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
Utilities for software builds, documentation, cluster interaction, calling fem tools, logging, exceptions and simple geometric and mechanical operations.

"""
from importlib import metadata
from pathlib import Path

import tomlkit

name = Path(__file__).parent.name


def getPyprojectMeta(initPath):
    """Returns project data from pyproject.toml

    :param initPath: path to the packages main __init__.py file
    :return: dict with entries from tool.poetry in pyproject.toml
    """
    with open(Path(Path(initPath).parents[2], "pyproject.toml")) as pyproject:
        file_contents = pyproject.read()

    contents_dict = tomlkit.parse(file_contents)
    try:
        return contents_dict["project"]
    except:
        return contents_dict["tool"]["poetry"]


try:
    # package is installed
    version = metadata.version(name)
    programDir = str(Path(__file__).parent)
except metadata.PackageNotFoundError:
    # package is not installed, read pyproject.toml
    try:
        # We have the full GitLab repository
        pkgMeta = getPyprojectMeta(__file__)
        version = str(pkgMeta["version"])
        programDir = str(Path(__file__).parents[3])
    except FileNotFoundError:
        # We have only the source code
        version = str("version not provided")
        programDir = str(Path(__file__).parent)


# Variables
epsilon = 1e-8
