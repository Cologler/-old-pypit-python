#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys
import traceback
from input_picker import pick_method, Stop

from internal.error import QuickExit
from internal.utils import (
    logger,
    yellow,
    chdir
)
from internal.package_metadata import PackageMetadata
from internal.setupcli import NamedSetupCli, SetupCli
from internal.doc import generate_rst_doc


NORM_TABLE = {
    ord('-'): '_'
}

def build_proj(setup_cli):
    setup_cli.clean(quiet=True)
    setup_cli.build(quiet=True)
    name = setup_cli._name.translate(NORM_TABLE)
    with open(os.path.join(name + '.egg-info', 'SOURCES.txt')) as fp:
        print('[INFO] manifest files:')
        for line in fp.read().splitlines():
            print(' ' * 8 + line)

def pypit(projdir: str):
    path_metadata = '__pypit_metadata__.json'

    metadata = PackageMetadata.parse(path_metadata) or PackageMetadata.create(path_metadata)
    metadata.auto_update()
    metadata.update_optional()
    metadata.save(path_metadata)
    metadata.generate_setup_py('setup.py')

    generate_rst_doc()

    setup_cli = NamedSetupCli(metadata.name)
    build_proj(setup_cli)

    while True:
        print(yellow('[?]'), 'want to execute any action ?')
        method = pick_method(setup_cli)
        if method is not None:
            logger.info(f'begin {method.__name__} ...')
            method()
            logger.info(f'{method.__name__} finished ...')
        else:
            print('[DONE] all job finished.')
            return

def pypit_cli(cmd):
    setup_cli = SetupCli()
    if cmd in dir(setup_cli):
        method = getattr(setup_cli, cmd)
        logger.info(f'begin {method.__name__} ...')
        method()
        logger.info(f'{method.__name__} finished ...')
    else:
        print(f'unknown command <{cmd}>')
        print(f'available commands:')
        for cmd in dir(setup_cli):
            if not cmd.startswith('_'):
                print(f'    {cmd}')

def ensure_isdir(path):
    if not os.path.isdir(path):
        logger.error(f'<{path}> is not a dir.')
        return exit()

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:

        path, cmd = None, None
        if len(argv) == 1:
            path = '.'
        elif len(argv) == 2:
            if os.path.isdir(argv[1]):
                path = argv[1]
            else:
                path = '.'
                cmd = argv[1]
        elif len(argv) == 3:
            path, cmd = argv[1:]
        elif len(argv) > 3:
            logger.error('unknown arguments.')
            return
        path = os.path.abspath(path)
        ensure_isdir(path)
        with chdir(path):
            return pypit(path) if cmd is None else pypit_cli(cmd)

    except Stop:
        logger.info('User stop application.')
    except QuickExit as qe:
        logger.info(str(qe))
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    main()
