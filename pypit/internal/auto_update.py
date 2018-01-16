#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os

from .utils import logger
from .package_metadata import PackageMetadata
from .data_licenses import try_parse_license

# pylint: disable=C0103
register = PackageMetadata.register_auto_updater

@register
def update_install_requires(self: PackageMetadata):
    def detect_and_update(path):
        if os.path.isfile(path):
            with open(path, 'r') as fp:
                lines = str(fp.read()).splitlines()
                lines = [l for l in lines if l.strip()]
                self.install_requires = lines
            return True

    for name in ['requirements.txt', 'requires.txt']:
        if detect_and_update(name):
            logger.info(f'updated install_requires from file <{name}>.')
            return

    logger.info('does not found any requires modules. try put them in `requirements.txt`.')

@register
def update_license(self: PackageMetadata):
    if self.license:
        # only update empty license
        return

    def detect_and_update(path):
        if os.path.isfile(path):
            with open(path, 'r') as fp:
                lines = str(fp.read()).splitlines()
                if lines:
                    first_line = lines[0].strip()
                    lic = try_parse_license(first_line)
                    if lic is not None:
                        self.license = lic
            return True

    for name in ['LICENSE', 'LICENSE.txt']:
        if detect_and_update(name):
            logger.info(f'updated license from file <{name}>.')
            return

    logger.info('does not found any license file.')
