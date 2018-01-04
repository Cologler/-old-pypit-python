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
from subprocess import DEVNULL
from m2r import convert as md2rst
from fsoopify import Path
from setuptools import find_packages
from input_picker import pick_bool, pick_item, pick_method, Stop

from _utils import (
    logger,
    yellow
)
from input_helper import INPUT_METHOD_TABLE

class QuickExit(Exception):
    pass


NORM_TABLE = {
    ord('-'): '_'
}


class Templates:
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
    def setup(self):
        return self._setup

    def copy_to(self, metadata):
        setup_argument = metadata.to_setup_argument()
        with open('setup.py', 'w') as fp:
            fp.write(self._setup.format(
                setup_argument=setup_argument,
                description=repr(metadata.description)
            ))

        prefix = 'pypitscript_'

        for name in self._templates:
            with open(prefix + name, 'w') as fp:
                fp.write(self._templates[name].format(name=metadata.name))

        for name in self._readonlys:
            with open(prefix + name, 'w') as fp:
                fp.write(self._readonlys[name])


TEMPLATES = Templates()

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
                logger.info('updated install_requires from file <{}>.'.format(name))
                return
        logger.info('does not found any requires modules.')

    def update_optional(self):
        print(yellow('[?] do you want to update other optional arguments ?'))
        if not pick_bool(defval=False):
            return
        types_map = {
            'zip_safe': bool,
            'include_package_data': bool,
            'license': None,
            'entry_points': None
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
        if not os.path.isfile(path):
            logger.debug('no exists metadata found.')
            return None

        metadata = PackageMetadata()

        with open(path, 'r') as fp:
            try:
                content = json.load(fp)
            except json.decoder.JSONDecodeError:
                raise QuickExit('[ERROR] <{}> is not a valid json file. try delete it for continue.'.format(path))

        metadata.__dict__.update(content)

        metadata.version = cls.input_str('version', strip=True, can_empty=False, not_str=metadata.version)

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
        with open(path, 'w') as fp:
            json.dump(self.__dict__, fp, indent=2)

    def to_setup_argument(self):
        lines = []
        for k in self.__dict__:
            v = repr(self.__dict__[k])
            lines.append('    {} = {},'.format(k, v))
        return '\n'.join(lines)


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


def get_rst_doc():

    def resolve_desc(name, converter):
        if os.path.isfile(name):
            logger.info('resolve description from {}.'.format(name))
            with open(name) as fp:
                content = fp.read()
                return content if converter is None else converter(content)

    rst_doc = resolve_desc('README.rst', None) or resolve_desc('README.md', md2rst)

    if rst_doc is None:
        logger.info('no description found.')
        return ''

    assert isinstance(rst_doc, str)

    # append history

    def resolve_history(name, converter):
        if os.path.isfile(name):
            logger.info('[INFO] append history from {}.'.format(name))
            with open(name) as fp:
                content = fp.read()
                return content if converter is None else converter(content)

    history = resolve_history('HISTORY.rst', None) or resolve_history('HISTORY.md', md2rst)

    if history is None:
        print('[INFO] no history found.')
    else:
        rst_doc = rst_doc + '\n\n' + history,

    return rst_doc

def build_proj(setup_cli):
    setup_cli.clean()
    setup_cli.build()
    name = setup_cli._name.translate(NORM_TABLE)
    with open(os.path.join(name + '.egg-info', 'SOURCES.txt')) as fp:
        print('[INFO] manifest files:')
        for line in fp.read().splitlines():
            print('  ' + line)

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

    TEMPLATES.copy_to(metadata)

    rstdoc = get_rst_doc()
    with open('__pypit_desc__.rst', 'w') as fp:
        fp.write(rstdoc)

    setup_cli = SetupCli(metadata)
    build_proj(setup_cli)

    while True:
        print(yellow('[?] want to execute any action ?'))
        method = pick_method(setup_cli)
        if method is not None:
            logger.info('begin {} ...'.format(method.__name__))
            method()
            logger.info('{} finished ...'.format(method.__name__))
        else:
            print('[DONE] all job finished.')
            return


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        if len(argv) == 1:
            return pypit('.')
        if len(argv) == 2:
            return pypit(argv[1])
        logger.error('unknown arguments.')
    except Stop:
        logger.info('User stop application.')
    except QuickExit as qe:
        logger.info(str(qe))
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    main()
