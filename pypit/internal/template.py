#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys

from fsoopify import Path

class _Templates:
    def __init__(self):
        self._template_dir = Path(sys.argv[0]).dirname
        self._setup = self._open_text('setup.py')
        self._templates = {}
        self._add_template('install-from-pypi.bat')
        self._add_template('uninstall.bat')
        self._readonlys = {}
        self._add_readonly('install.bat')
        self._add_readonly('upload.bat')
        self._add_readonly('upload_proxy.bat')

    def _add_readonly(self, name):
        self._readonlys[name] = self._open_text(name)

    def _add_template(self, name):
        self._templates[name] = self._open_text(name)

    def _open_text(self, name):
        with open(os.path.join(self._template_dir, 'templates', name), 'r') as fp:
            return fp.read()

    @property
    def template_setup(self):
        return self._setup

    @property
    def setup(self):
        return self._setup

    def generate_setup_py(self, metadata, dest_path):
        setup_argument = metadata.to_setup_argument()
        with open(dest_path, 'w', encoding='utf-8') as fp:
            fp.write(self._setup.format(
                setup_argument=setup_argument,
                description=repr(metadata.description)
            ))

    def generate_scripts(self, metadata):
        prefix = 'pypitscript_'

        for name in self._templates:
            with open(prefix + name, 'w') as fp:
                fp.write(self._templates[name].format(name=metadata.name))

        for name in self._readonlys:
            with open(prefix + name, 'w') as fp:
                fp.write(self._readonlys[name])

TEMPLATES = _Templates()
