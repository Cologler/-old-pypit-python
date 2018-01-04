#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import re
import glob
from setuptools import find_packages
from input_picker import pick_bool, pick_item
from fsoopify import DirectoryInfo, FileInfo

from _utils import (
    yellow, green,
    logger
)

INPUT_METHOD_TABLE = {}
def register(t):
    def _(fn):
        INPUT_METHOD_TABLE[t] = fn
        return fn
    return _

@register(bool)
def input_bool(defval, **kwargs):
    return pick_bool(defval=defval, use_bool_style=True)

@register(str)
def input_str(name, **kwargs):
    msg = yellow('[?] please input the package {}: '.format(name))
    print(msg, end='')
    value = input()
    return value.strip()

@register('license')
def input_license(**kwargs):
    ls = [
        'Apache License 2.0',
        'GNU General Public License v3.0',
        'MIT License',
        'BSD 2-clause "Simplified" License',
        'BSD 3-clause "New" or "Revised" License',
        'Eclipse Public License 1.0',
        'GNU Affero General Public License v3.0',
        'GNU General Public License v2.0',
        'GNU Lesser General Public License v2.1',
        'GNU Lesser General Public License v3.0',
        'Mozilla Public License 2.0',
        'The Unlicense'
    ]
    msg = yellow('[?] please pick a license from list:')
    print(msg, end='')
    index = pick_item(ls, defidx=2)
    if index == -1:
        return ''
    else:
        return ls[index]


@register('entry_points')
def input_entry_points(**kwargs):
    '''
    return a dict like `{ 'console_scripts': ['funniest-joke=funniest.command_line:main'], }`.
    '''
    filelist = []
    packages_names = find_packages()
    for packroot in packages_names:
        root_dir = DirectoryInfo(packroot)
        for f in [x for x in root_dir.list_items(depth=100) if isinstance(x, FileInfo)]:
            if not f.path.ext.equals('.py'):
                continue
            path = str(f.path)
            filelist.append(path)

    def find_default_on_files(items):
        for wkname in ('cli.py', 'main.py',):
            lwkn = os.sep + wkname
            for i, x in enumerate(items):
                if x.endswith(lwkn):
                    return i

    if not filelist:
        logger.error('no python files was founds.')
        return

    print(yellow('[?] please select a file that contains entry points:'))
    idx = pick_item(filelist, defidx=find_default_on_files(filelist))
    if idx == -1:
        return

    filepath = filelist[idx]
    content = FileInfo(filepath).read_alltext()
    matches = re.findall('^def ([^(]+)\\(.+$', content, flags=re.M) # func names

    def find_default_on_funcs(items):
        for wkname in ('cli', 'main',):
            for i, x in enumerate(items):
                if x == wkname:
                    return i

    if not matches:
        logger.error('no python files was founds from {}.'.format(green(filepath)))
        return

    print(yellow('[?] please select a func from the .py file:'))
    idx = pick_item(matches, defidx=find_default_on_funcs(matches))
    if idx == -1:
        return
    funcname = matches[idx]

    msg = yellow('[?] please input the entry points name (default is {})'.format(green(packages_names[0])))
    print(msg, end='')
    entry_points = input().strip() or packages_names[0]

    return {
        'console_scripts': ['{entry_points}={filepath}:{funcname}'.format(
            entry_points=entry_points,
            filepath=filepath.replace(os.sep, '.'),
            funcname=funcname,
        )]
    }
