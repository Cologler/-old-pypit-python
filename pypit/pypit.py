#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys
import traceback
import json
import subprocess
from m2r import convert as md2rst
from fsoopify import Path, FileInfo
from setuptools import find_packages
from input_picker import pick_bool, pick_item, Stop, Help

class QuickExit(Exception): pass

class Templates:
    def __init__(self):
        self._template_dir = Path(sys.argv[0]).dirname
        self._setup = self._open_text('setup.py')
        self._build = self._file('build.bat')
        self._install = self._file('install.bat')
        self._upload = self._file('upload.bat')
        self._upload_proxy = self._file('upload_proxy.bat')
        self._uninstall = self._open_text('uninstall.bat')

    def _open_text(self, name):
        with open(os.path.join(self._template_dir, 'templates', name), 'r') as fp:
            return fp.read()

    def _file(self, name):
        return FileInfo(os.path.join(self._template_dir, 'templates', name))

    @property
    def setup(self):
        return self._setup

    @property
    def build(self):
        return self._build

    @property
    def upload(self):
        return self._upload

    @property
    def upload_proxy(self):
        return self._upload_proxy

    @property
    def install(self):
        return self._install

    @property
    def uninstall(self):
        return self._uninstall

TEMPLATES = Templates()

class PackageMetadata:
    def __init__(self):
        self.version = '0.1.0.0'
        self.description = ''
        self.name = ''
        self.keywords = []
        self.author = ''
        self.author_email = ''
        self.url = ''
        self.license = ''
        self.entry_points = {}
        self.zip_safe = False
        self.include_package_data = True
        self.classifiers = []
        # requires
        self.setup_requires = []
        self.install_requires = []
        self.tests_require = []

    def repr_dict(self):
        reprm = {}
        for k in self.__dict__:
            reprm[k] = repr(self.__dict__[k])
        return reprm

    def update_install_requires(self):
        def detect_and_update(path):
            if os.path.isfile(path):
                with open(path, 'r') as fp:
                    lines = str(fp.read()).splitlines()
                    lines = [l for l in lines if l.strip()]
                    self.install_requires = lines
                return True
        for name in ['requirements.txt', 'requires.txt']:
            if detect_and_update(name):
                print('[INFO] updated install_requires from file <{}>.'.format(name))
                return
        print('[INFO] does not has any requires modules.')

    def update_optional(self):
        print('[USER] do you want to update other optional arguments ?')
        if not pick_bool():
            return

    @classmethod
    def required_strip(cls, name):
        value = ''
        while not value.strip():
            value = input('[USER] please input the package {} (cannot be empty): '.format(name))
        return value.strip()

    @classmethod
    def required_different_strip(cls, name, oldval):
        value = ''
        while not value.strip() or value.strip() == oldval:
            value = input('[USER] please input the package {} (cannot be empty or `{}`): '.format(name, oldval))
        return value.strip()

    @classmethod
    def optional_strip(cls, name, defval):
        value = input('[USER] please input the package {} (keep it empty to use `{}`): '.format(name, defval))
        if value.strip():
            return value.strip()
        return defval

    @classmethod
    def parse(cls, path):
        if not os.path.isfile(path):
            return None

        metadata = PackageMetadata()

        with open(path, 'r') as fp:
            try:
                content = json.load(fp)
            except json.decoder.JSONDecodeError:
                raise QuickExit('[ERROR] <{}> is not a valid json file. try delete it for continue.'.format(path))

        metadata.__dict__.update(content)

        metadata.version = cls.required_different_strip('version', metadata.version)

        return metadata

    @classmethod
    def create(cls, path):
        metadata = PackageMetadata()

        packages = find_packages(where=Path(path).dirname)
        if packages:
            metadata.name = cls.optional_strip('name', packages[0])
        else:
            metadata.name = cls.required_strip('name')

        metadata.version = cls.optional_strip('version', metadata.version)

        metadata.author = cls.required_strip('author')
        metadata.author_email = cls.required_strip('author email')
        metadata.url = cls.required_strip('url')

        return metadata

    def save(self, path):
        with open(path, 'w') as fp:
            json.dump(self.__dict__, fp, indent=2)

    def to_setup_argument(self):
        lines = []
        for k in self.__dict__:
            v = repr(self.__dict__[k])
            lines.append('    {} = {},'.format(k, v))
        return '\n'.join(lines)


def get_rst_doc():

    def resolve_desc(name, converter):
        if os.path.isfile(name):
            print('[INFO] resolve description from {}.'.format(name))
            with open(name) as fp:
                content = fp.read()
                return content if converter is None else converter(content)

    rst_doc = resolve_desc('README.rst', None) or resolve_desc('README.md', md2rst)

    if rst_doc is None:
        print('[INFO] no description found.')
        return ''

    assert isinstance(rst_doc, str)

    # append history

    def resolve_history(name, converter):
        if os.path.isfile(name):
            print('[INFO] append history from {}.'.format(name))
            with open(name) as fp:
                content = fp.read()
                return content if converter is None else converter(content)

    history = resolve_history('HISTORY.rst', None) or resolve_history('HISTORY.md', md2rst)

    if history is None:
        print('[INFO] no history found.')
    else:
        rst_doc = rst_doc + '\n\n' + history,

    return rst_doc


def copy_files(metadata: PackageMetadata):
    with open('uninstall.bat', 'w') as fp:
        fp.write(TEMPLATES.uninstall.format(name=metadata.name))

    if not os.path.isfile(TEMPLATES.build.path.name):
        TEMPLATES.build.copy_to(TEMPLATES.build.path.name)
    if not os.path.isfile(TEMPLATES.install.path.name):
        TEMPLATES.install.copy_to(TEMPLATES.install.path.name)
        TEMPLATES.upload.copy_to(TEMPLATES.upload.path.name)
        TEMPLATES.upload_proxy.copy_to(TEMPLATES.upload_proxy.path.name)

def pypit(projdir: str):
    projdir = os.path.abspath(projdir)
    if not os.path.isdir(projdir):
        raise QuickExit('<{}> is not a dir.'.format(projdir))

    os.chdir(projdir)

    path_metadata = '__pypit_metadata__.json'

    metadata = PackageMetadata.parse(path_metadata) or PackageMetadata.create(path_metadata)
    metadata.update_install_requires()
    metadata.update_optional()
    metadata.save(path_metadata)

    setup_argument = metadata.to_setup_argument()
    with open('setup.py', 'w') as fp:
        fp.write(TEMPLATES.setup.format(
            setup_argument=setup_argument,
            description=repr(metadata.description)
        ))

    rstdoc = get_rst_doc()
    with open('__pypit_desc__.rst', 'w') as fp:
        fp.write(rstdoc)

    copy_files(metadata)

    subprocess.call(TEMPLATES.build.path.name, stdout=subprocess.DEVNULL)
    with open(os.path.join(metadata.name + '.egg-info', 'SOURCES.txt')) as fp:
        print('[INFO] manifest files:')
        for line in fp.read().splitlines():
            print('  ' + line)

    print('[USER] install now?')
    if pick_bool(False):
        print('[INFO] begin install ...')
        os.system(TEMPLATES.install.path.name)

    print('[USER] upload now?')
    if pick_bool(False):
        print('[INFO] begin upload ...')
        os.system(TEMPLATES.upload_proxy.path.name)

    print('[DONE] all job finished.')


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        if len(argv) == 1:
            return pypit('.')
        if len(argv) == 2:
            return pypit(argv[1])
        raise NotImplementedError
    except Stop:
        print('User stop application.')
    except QuickExit as qe:
        print(qe)
    except Exception:
        traceback.print_exc()
        input()

if __name__ == '__main__':
    main()
