#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import logging
import colorama

# init logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[{levelname}] {name}: {message}',
    style='{'
)
logger = logging.getLogger('pypit')

# init colorama
colorama.init()

def yellow(text):
    ''' wrap text as colored text. '''
    return colorama.Fore.YELLOW + text + colorama.Fore.RESET

