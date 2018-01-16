#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
from m2r import convert as md2rst

from .utils import logger

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
            logger.info(f'append history from {name}.')
            with open(name) as fp:
                content = fp.read()
                return content if converter is None else converter(content)

    history = resolve_history('HISTORY.rst', None) or resolve_history('HISTORY.md', md2rst)

    if history is None:
        logger.info('no history found.')
    else:
        rst_doc = rst_doc + '\n\n' + history,

    return rst_doc

def generate_rst_doc():
    rstdoc = get_rst_doc()
    with open('__pypit_desc__.rst', 'w') as fp:
        fp.write(rstdoc)
