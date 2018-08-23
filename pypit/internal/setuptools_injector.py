# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys
from types import ModuleType
import importlib.util
import contextlib

import setuptools

@contextlib.contextmanager
def inject_setuptools():
    datas = []
    class FakeSetuptools(ModuleType):
        def __init__(self):
            super().__init__('setuptools')
        def setup(self, **attrs):
            datas.append(attrs)
        def __getattr__(self, name):
            def other(*args, **kwargs):
                return None
            return other
    sys.modules['setuptools'] = FakeSetuptools()
    yield datas
    sys.modules['setuptools'] = setuptools

def run_code(path):
    spec = importlib.util.spec_from_file_location('<name>', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

def get_setup_attrs(path):
    with inject_setuptools() as attrs_list:
        run_code(path)
    assert len(attrs_list) == 1
    return attrs_list[0]
