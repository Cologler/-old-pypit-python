#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import logging

import colorama

logging.basicConfig(
    level=logging.DEBUG,
    format='[{levelname}] {name}: {message}',
    style='{'
)

def get_logger():
    ''' return logger from `logging.getLogger('pypit')`. '''
    return logging.getLogger('pypit')

logger = get_logger()

# init colorama
colorama.init()

def yellow(text):
    ''' wrap text as colored text. '''
    return colorama.Fore.YELLOW + text + colorama.Fore.RESET

def lightgreen(text):
    ''' wrap text as colored text. '''
    return colorama.Fore.LIGHTGREEN_EX + text + colorama.Fore.RESET
