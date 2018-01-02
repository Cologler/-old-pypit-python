#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from input_picker import pick_bool

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
