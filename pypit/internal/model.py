#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

class ProjectInfo:
    def __init__(self, root_dir):
        self._root_dir = root_dir

    @property
    def root_dir(self):
        return self._root_dir
