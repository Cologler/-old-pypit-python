#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import io
import subprocess
from subprocess import PIPE

from .package_metadata import PackageMetadata
from .template import TEMPLATES
from .utils import logger, green, red

class SetupCli:
    def __init__(self, metadata: PackageMetadata):
        self._metadata = metadata
        self._name = metadata.name

    def _run(self, cmds, *, quiet=False):
        prefix = '>>>'.rjust(13).ljust(14)
        h_output = False
        h_error = False

        with subprocess.Popen(cmds, stdout=PIPE, stderr=PIPE) as process:
            if not quiet:
                for line in io.TextIOWrapper(process.stdout, encoding='utf-8'):
                    line = line.strip()
                    if line:
                        if not h_output:
                            logger.info('output: ')
                            h_output = True
                        print(prefix + green(line))

            for line in io.TextIOWrapper(process.stderr, encoding='utf-8'):
                line = line.strip()
                if line:
                    if not h_error:
                        logger.error('output: ')
                        h_error = True
                    print(prefix + red(line))

    def clean(self, *, quiet=False):
        self._run(['python', 'setup.py', 'clean'], quiet=quiet)

    def build(self, *, quiet=False):
        self._run(['python', 'setup.py', 'build'], quiet=quiet)

    def install(self):
        '''install from project.'''
        self._run(['python', 'setup.py', 'install'])

    def install_update(self):
        '''install from project. before install, uninstall exists.'''
        self.uninstall()
        self.install()

    def install_from_pypi(self):
        '''install/upgrade from pypi.'''
        self._run(['pip', 'install', self._name, '--upgrade'])

    def uninstall(self):
        self._run(['pip', 'uninstall', self._name])

    def upload(self):
        '''upload to pypi.'''
        self._run(['python', 'setup.py', 'register', 'sdist', 'bdist_egg', 'upload'])

    def upload_use_proxy(self):
        # cache env
        k_http = 'HTTP_PROXY'
        k_https = 'HTTPS_PROXY'
        ks = (k_http, k_https)
        cache = {}
        for k in ks:
            cache[k] = os.environ.get(k)

        # set env
        os.environ[k_http] = 'http://127.0.0.1:1082'
        os.environ[k_https] = 'https://127.0.0.1:1082'
        self.upload()

        # rollback env
        for k in ks:
            if cache[k] is None:
                os.environ.pop(k)
            else:
                os.environ[k] = cache[k]

    def generate_scripts(self):
        TEMPLATES.generate_scripts(self._metadata)
