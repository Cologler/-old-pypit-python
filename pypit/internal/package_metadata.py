#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
from setuptools import find_packages

from fsoopify import FileInfo, SerializeError, Path
from input_picker import pick_bool, pick_item

from .error import QuickExit
from .utils import logger, yellow
from .input_helper import INPUT_METHOD_TABLE
from .template import TEMPLATES

class PackageMetadata:

    def __init__(self):
        # metadata
        self.name = ''
        self.version = '0.1.0.0'
        self.description = ''
        self.keywords = []
        self.author = ''
        self.author_email = ''
        self.url = ''
        self.license = ''
        self.classifiers = []
        # package
        self.scripts = []
        self.entry_points = {}
        self.zip_safe = False
        self.include_package_data = True
        # requires
        self.setup_requires = []
        self.install_requires = []
        self.tests_require = []

    def repr_dict(self):
        reprm = {}
        for k in self.__dict__:
            reprm[k] = repr(self.__dict__[k])
        return reprm

    # auto update

    _AUTO_UPDATERS = []

    @classmethod
    def register_auto_updater(cls, fn):
        cls._AUTO_UPDATERS.append(fn)
        return fn

    def auto_update(self):
        ''' auto update from project. '''
        for updater in self._AUTO_UPDATERS:
            updater(self)

    def update_optional(self):
        print(yellow('[?]'), 'do you want to update any optional arguments ?')
        if not pick_bool(defval=False):
            return
        types_map = {
            'zip_safe': bool,
            'include_package_data': bool,
            'license': None,
            'entry_points': None,
            'scripts': None,
        }
        source = list(types_map.keys())
        idx = pick_item(source)
        if idx == -1:
            return
        name = source[idx]
        func = INPUT_METHOD_TABLE.get(name) or INPUT_METHOD_TABLE.get(types_map[name])
        assert func is not None, ''
        oldval = getattr(self, name)
        newval = func(
            metadata=self,
            defval=oldval,
            name=name,
        )
        if newval is not None:
            setattr(self, name, newval)
            logger.info('{} already set to <{}>.'.format(name, newval))
        return self.update_optional()

    def update_version(self):
        self.version = self.input_str('version', strip=True, can_empty=False, not_str=self.version)

    @classmethod
    def input_str(cls, name, strip=True, can_empty=False, not_str=None):
        diff = []
        if not can_empty:
            diff.append('')
        if not_str:
            diff.append(not_str)
        opt = ' (cannot be {})'.format(' or '.join([x or 'empty' for x in diff])) if diff else ''
        msg = yellow('[?] please input the package {}{}: '.format(name, opt))
        value = ''
        while True:
            print(msg, end='')
            value = input()
            value = value.strip() if strip else value
            if value not in diff:
                return value

    @classmethod
    def optional_strip(cls, name, defval):
        print(yellow('[?] please input the package {} (keep it empty to use `{}`): '.format(name, defval)), end='')
        value = input()
        if value.strip():
            return value.strip()
        return defval

    @classmethod
    def parse(cls, path):
        fileinfo = FileInfo(path)
        if not fileinfo.is_file():
            logger.debug('no exists metadata found.')
            return None

        metadata = PackageMetadata()

        fileinfo.load('json')
        try:
            content = fileinfo.load('json')
        except SerializeError:
            raise QuickExit('[ERROR] <{}> is not a valid json file. try delete it for continue.'.format(path))

        metadata.__dict__.update(content)

        return metadata

    @classmethod
    def create(cls, path):
        metadata = PackageMetadata()

        packages = find_packages(where=Path(path).dirname or '.')
        if packages:
            metadata.name = cls.optional_strip('name', packages[0])
        else:
            metadata.name = cls.input_str('name')

        metadata.version = cls.optional_strip('version', metadata.version)

        metadata.author = cls.input_str('author')
        metadata.author_email = cls.input_str('author email')
        metadata.url = cls.input_str('url')

        return metadata

    def save(self, path):
        ''' save template to file so we can get it next time. '''
        fileinfo = FileInfo(path)
        fileinfo.dump('json', self.__dict__, kwargs={
            'indent':2
        })

    def generate_setup_py(self, path):
        return TEMPLATES.generate_setup_py(self, path)

    def to_setup_argument(self):
        lines = []
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                lines.append('    {} = {},'.format(k, repr(v)))
        return '\n'.join(lines)
