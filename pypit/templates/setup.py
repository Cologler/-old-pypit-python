#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
from setuptools import setup, find_packages

DESCRIPTION = {description}

long_description = None

if os.path.isfile('README.md'):
    with open('README.md') as f:
        long_description = f.read()

long_description = long_description or DESCRIPTION

setup(
    name = {name},
    version = {version},
    description = DESCRIPTION,
    long_description = long_description or DESCRIPTION,
    classifiers = [],
    keywords = {keywords},
    author = {author},
    author_email = {author_email},
    url = {url},
    license = {license},
    packages = find_packages(),
    include_package_data = True,
    zip_safe = {zip_safe},
    install_requires = {install_requires},
    entry_points = {entry_points},
)
