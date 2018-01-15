#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from collections import namedtuple

License = namedtuple('License', ['name', 'keys'])

LICENSES = [
    License(
        'Apache License 2.0',
        ['apache']),
    License(
        'GNU General Public License v3.0', ['GPLv3']),
    License(
        'MIT License',
        ['MIT']),
    License(
        'BSD 2-clause "Simplified" License',
        ['BSD2']),
    License(
        'BSD 3-clause "New" or "Revised" License',
        ['BSD3']),
    License(
        'Eclipse Public License 1.0',
        ['EPL']),
    License(
        'GNU Affero General Public License v3.0',
        ['AGPLv3']),
    License(
        'GNU General Public License v2.0',
        ['GPLv2']),
    License(
        'GNU Lesser General Public License v2.1',
        ['LGPLv2.1']),
    License(
        'GNU Lesser General Public License v3.0',
        ['LGPLv3']),
    License(
        'Mozilla Public License 2.0',
        ['MPL']),
    License(
        'The Unlicense',
        []),
]

LICENSES_TABLE = {}

for lic in LICENSES:
    LICENSES_TABLE[lic.name.lower()] = lic
    for k in lic.keys:
        LICENSES_TABLE[k.lower()] = lic

LICENSES_LIST = [lic.name for lic in LICENSES]

def try_parse_license(text):
    lic_ = LICENSES_TABLE.get(text.lower().replace('license', '').strip())
    if lic_ is not None:
        return lic_.name
