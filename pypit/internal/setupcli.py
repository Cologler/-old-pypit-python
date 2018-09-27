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
from .utils_pypi import get_package_url

class SetupCli:
    def _run(self, cmds, *, quiet=False):
        prefix = '>>>'.rjust(13).ljust(14)
        h_output = False
        h_error = False

        logger.info(f'eval commands: {repr(cmds)}')

        with subprocess.Popen(cmds, stdout=PIPE, stderr=PIPE) as process:
            if not quiet:
                for line in io.TextIOWrapper(process.stdout, encoding='utf-8'):
                    if line:
                        if not h_output:
                            logger.info('output: ')
                            h_output = True
                        print(prefix + green(line), end='')

            for line in io.TextIOWrapper(process.stderr, encoding='utf-8'):
                if line:
                    if line.endswith('\r'):
                        line = line[:-1]
                    if not h_error:
                        logger.error('output: ')
                        h_error = True
                    print(prefix + red(line), end='')

    def clean(self, *, quiet=False):
        self._run(['python', 'setup.py', 'clean'], quiet=quiet)

    def build(self, *, quiet=False):
        self._run(['python', 'setup.py', 'build'], quiet=quiet)

    def install(self):
        '''install from project.'''
        self._run(['python', 'setup.py', 'install'])

    def publish(self):
        '''
        publish to pypi.
        '''
        #self._run(['python', 'setup.py', 'register', 'sdist', 'bdist_egg', 'upload'])
        self._run(['python', 'setup.py', 'sdist', 'bdist_wheel', 'upload'])

    def publish_use_proxy(self):
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
        self.publish()

        # rollback env
        for k in ks:
            if cache[k] is None:
                os.environ.pop(k)
            else:
                os.environ[k] = cache[k]


class NamedSetupCli(SetupCli):
    def __init__(self, package_name: str):
        super().__init__()
        self._name = package_name

    def install_update(self):
        '''install from project. before install, uninstall exists.'''
        self.uninstall()
        self.install()

    def install_from_pypi(self):
        '''install/upgrade from pypi.'''
        self._run(['pip', 'install', self._name, '--upgrade'])

    def uninstall(self):
        self._run(['pip', 'uninstall', self._name, '-y'])

    def browse(self):
        '''
        open browser for view the package on pypi.
        '''
        import webbrowser
        webbrowser.open(get_package_url(self._name))
