#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import subprocess
from subprocess import DEVNULL

from .package_metadata import PackageMetadata
from .template import TEMPLATES

class SetupCli:
    def __init__(self, metadata: PackageMetadata):
        self._metadata = metadata
        self._name = metadata.name

    def clean(self):
        subprocess.call(['python', 'setup.py', 'clean'], stdout=DEVNULL)

    def build(self):
        subprocess.call(['python', 'setup.py', 'build'], stdout=DEVNULL)

    def install(self):
        ''' install from project. '''
        subprocess.call(['python', 'setup.py', 'install'], stdout=DEVNULL)

    def install_update(self):
        ''' install from project. before install, uninstall exists version. '''
        subprocess.call(['pip', 'uninstall', self._name], stdout=DEVNULL)
        self.install()

    def install_from_pypi(self):
        subprocess.call(['pip', 'install', self._name, '--upgrade'], stdout=DEVNULL)

    def uninstall(self):
        subprocess.call(['pip', 'uninstall', self._name], stdout=DEVNULL)

    def upload(self):
        ''' upload to pypi. '''
        subprocess.call(
            ['python', 'setup.py', 'register', 'sdist', 'bdist_egg', 'upload'],
            stdout=DEVNULL
        )

    def upload_use_proxy(self):
        subprocess.call(['pypitscript_upload_proxy.bat'], stdout=DEVNULL)

    def generate_scripts(self):
        TEMPLATES.generate_scripts(self._metadata)


class InitSetupCli(SetupCli):
    def update_version(self):
        self._metadata.update_version()
