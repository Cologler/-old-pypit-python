# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

# all docs was copy from
# https://setuptools.readthedocs.io/en/latest/setuptools.html

from typing import Iterable

class CFGDataItem:
    def __init__(self, key, types: Iterable[str], group):
        self._key = key
        self._types = types
        self._group = group

    @property
    def key(self):
        return self._key

    @property
    def types(self):
        return self._types

_CFG_DATA_ITEMS = []
_CFG_DATA_ITEMS_MAP = {}

def get_metadata_declaration(key):
    return _CFG_DATA_ITEMS_MAP[key]

def declare_root(name, *items):
    for item in items:
        md = CFGDataItem(item['key'], item['type'], name)
        _CFG_DATA_ITEMS.append(md)
        _CFG_DATA_ITEMS_MAP[md.key] = md

def declare_item(key: str, type: str, **kwargs):
    types = (t.strip() for t in type.split(',')) # parse types
    kwargs['key'] = key
    kwargs['type'] = types
    return kwargs

declare_root(
    'metadata',
    declare_item(
        # value should be a path str (without `file:` prefix`).
        # for example: `description-file = README.md`
        key='desciption-file',
        type='list-comma'
    ),
    declare_item(
        key='name',
        type='str',
    ),
    declare_item(
        key='version',
        type='attr:, file:, str',
    ),
    declare_item(
        key='url',
        type='str',
    ),
    declare_item(
        key='download_url',
        type='str',
    ),
    declare_item(
        key='project_urls',
        type='dict',
    ),
    declare_item(
        key='author',
        type='str',
    ),
    declare_item(
        key='author_email',
        type='str',
    ),
    declare_item(
        key='maintainer',
        type='str',
    ),
    declare_item(
        key='maintainer_email',
        type='str',
    ),
    declare_item(
        key='classifiers',
        type='file:, list-comma',
    ),
    declare_item(
        key='license',
        type='file:, str',
    ),
    declare_item(
        key='description',
        type='file:, str',
    ),
    declare_item(
        key='long_description',
        type='file:, str',
    ),
    declare_item(
        key='long_description_content_type',
        type='str',
    ),
    declare_item(
        key='keywords',
        type='list-comma',
    ),
    declare_item(
        key='platforms',
        type='list-comma',
    ),
    declare_item(
        key='provides',
        type='list-comma',
    ),
    declare_item(
        key='requires',
        type='list-comma',
    ),
    declare_item(
        key='obsoletes',
        type='list-comma',
    ),
)

declare_root(
    'options',
    declare_item(
        key='zip_safe',
        type='bool',
    ),
    declare_item(
        key='setup_requires',
        type='list-semi',
    ),
    declare_item(
        key='install_requires',
        type='list-semi',
    ),
    declare_item(
        key='extras_require',
        type='section',
    ),
    declare_item(
        key='python_requires',
        type='str',
    ),
    declare_item(
        key='entry_points',
        type='file:, section',
    ),
    declare_item(
        key='use_2to3',
        type='bool',
    ),
    declare_item(
        key='use_2to3_fixers',
        type='list-comma',
    ),
    declare_item(
        key='use_2to3_exclude_fixers',
        type='list-comma',
    ),
    declare_item(
        key='convert_2to3_doctests',
        type='list-comma',
    ),
    declare_item(
        key='scripts',
        type='list-comma',
    ),
    declare_item(
        key='eager_resources',
        type='list-comma',
    ),
    declare_item(
        key='dependency_links',
        type='list-comma',
    ),
    declare_item(
        key='tests_require',
        type='list-semi',
    ),
    declare_item(
        key='include_package_data',
        type='bool',
    ),
    declare_item(
        key='packages',
        type='find:, list-comma',
    ),
    declare_item(
        key='package_dir',
        type='dict',
    ),
    declare_item(
        key='package_data',
        type='section',
    ),
    declare_item(
        key='exclude_package_data',
        type='section',
    ),
    declare_item(
        key='namespace_packages',
        type='list-comma',
    ),
    declare_item(
        key='py_modules',
        type='list-comma',
    ),
)
