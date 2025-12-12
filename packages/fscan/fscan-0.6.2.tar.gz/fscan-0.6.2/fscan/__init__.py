# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Evan Goetz (2023)
#
# This file is part of fscan

try:
    from ._version import version as __version__
except ModuleNotFoundError:
    try:
        import setuptools_scm
        __version__ = setuptools_scm.get_version(fallback_version='?.?.?')
    except (ModuleNotFoundError, TypeError, LookupError):
        __version__ = '?.?.?'

__author__ = "Evan Goetz <evan.goetz@ligo.org>"
__credits__ = [
    "Ansel Neunzert <ansel.neunzert@ligo.org>",
    "Sudhagar Suyamprakasam <sudhagar.suyamprakasam@ligo.org>",
]
