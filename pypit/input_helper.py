#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from input_picker import pick_bool, pick_item

from _utils import yellow

INPUT_METHOD_TABLE = {}
def register(t):
    def _(fn):
        INPUT_METHOD_TABLE[t] = fn
        return fn
    return _

@register(bool)
def input_bool(**kwargs):
    return pick_bool(defval=kwargs['defval'], use_bool_style=True)

@register(str)
def input_str(**kwargs):
    msg = yellow('[?] please input the package {}: '.format(kwargs['name']))
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
