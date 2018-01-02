#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from input_picker import pick_bool

INPUT_METHOD_TABLE = {}
def register(t):
    def _(fn):
        INPUT_METHOD_TABLE[t] = fn
        return fn
    return _

@register(bool)
def input_bool(oldval):
    return pick_bool(defval=oldval, use_bool_style=True)

