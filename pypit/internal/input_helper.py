#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import re
from setuptools import find_packages
from input_picker import pick_bool, pick_item
from fsoopify import DirectoryInfo, FileInfo, Path

from .utils import (
    yellow, lightgreen,
    logger
)
from .data_licenses import LICENSES_LIST

INPUT_METHOD_TABLE = {}
def register(t):
    def _(fn):
        INPUT_METHOD_TABLE[t] = fn
        return fn
    return _

def _pick_more(field_name) -> bool:
    ''' ask whether user want to pick more item. '''
    print(yellow('[?]') + ' did you want to pick more {}:'.format(lightgreen(field_name)))
    return pick_bool(defval=False)

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
    ls = LICENSES_LIST
    msg = yellow('[?]') + 'please pick a license from list:'
    print(msg, end='')
    index = pick_item(ls, defidx=2)
    if index == -1:
        return ''
    else:
        return ls[index]


def _list_python_scripts(pack_root):
    filelist = []
    root_dir = DirectoryInfo(pack_root)
    for f in [x for x in root_dir.list_items(depth=100) if isinstance(x, FileInfo)]:
        if not f.path.ext.equals('.py'):
            continue
        path = str(f.path)
        filelist.append(path)
    return filelist


@register('scripts')
def input_scripts(defval, **kwargs):
    '''
    return a list of .py file.
    each files will be copy to python script directory and make it available for general use.
    '''
    filelist = []
    for package in [x.path.name for x in DirectoryInfo('.').list_items() if isinstance(x, DirectoryInfo)]:
        filelist.extend(_list_python_scripts(package))

    if not filelist:
        logger.error('no python files was founds.')
        return

    if defval:
        filelist = [x for x in filelist if x not in defval]

    def pick():
        print(yellow('[?]'), 'please pick a file that will be copy to python script directory:')
        idx = pick_item(filelist)
        if idx == -1:
            return

        defval.append(filelist.pop(idx))
        return _pick_more('scripts')

    while pick():
        pass

    return defval


@register('entry_points')
def input_entry_points(defval: dict, **kwargs):
    '''
    return a dict like `{ 'console_scripts': ['funniest-joke=funniest.command_line:main'], }`.

    same as:

    ``` py
    from funniest.command_line import main
    main()
    ```
    '''
    console_scripts = defval.setdefault('console_scripts', list)

    filelist = []
    packages_names = find_packages()
    for package in packages_names:
        filelist.extend(_list_python_scripts(package))

    def find_default_on_files(items):
        for wkname in ('cli.py', 'main.py',):
            lwkn = os.sep + wkname
            for i, x in enumerate(items):
                if x.endswith(lwkn):
                    return i

    if not filelist:
        logger.error('no python files was founds.')
        return

    def pick():
        print(yellow('[?]'), 'please pick a file that contains entry points:')
        idx = pick_item(filelist, defidx=find_default_on_files(filelist))
        if idx == -1:
            return

        filepath = filelist[idx]
        content = FileInfo(filepath).read_text()
        matches = re.findall('^def ([^(]+)\\(.+$', content, flags=re.M) # func names

        def find_default_on_funcs(items):
            for wkname in ('cli', 'main',):
                for i, x in enumerate(items):
                    if x == wkname:
                        return i

        if not matches:
            logger.error('no python files was founds from {}.'.format(lightgreen(filepath)))
            return

        print(yellow('[?]'), 'please pick a func from {}:'.format(lightgreen(Path(filepath).name)))
        idx = pick_item(matches, defidx=find_default_on_funcs(matches))
        if idx == -1:
            return
        funcname = matches[idx]

        msg = yellow('[?]')
        msg += 'please input the entry points name (default is {})'.format(
            lightgreen(packages_names[0])
        )
        print(msg, end='')
        entry_points = input().strip() or packages_names[0]

        module_name = filepath[:-3].replace(os.sep, '.') # remove `.py` and more

        script = '{entry_points}={module_name}:{funcname}'.format(
            entry_points=entry_points,
            module_name=module_name,
            funcname=funcname,
        )
        if script not in console_scripts:
            console_scripts.append(script)
        return _pick_more('entry_points')

    while pick():
        pass

    return defval

@register('version')
def input_version(defval: dict, **kwargs):

    msg = yellow('[?]')
    msg += ' please input the package version'
    msg += f' (cannot be empty and {lightgreen(defval)}): '

    while True:
        print(msg, end='')
        value = input()
        value = value.strip()
        if value not in ('', defval):
            return value
