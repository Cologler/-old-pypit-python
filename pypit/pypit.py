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
    yellow
)
from internal.package_metadata import PackageMetadata
from internal.setupcli import SetupCli
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
            print('  ' + line)

def pypit(projdir: str):
    projdir = os.path.abspath(projdir)
    if not os.path.isdir(projdir):
        raise QuickExit('<{}> is not a dir.'.format(projdir))

    os.chdir(projdir)

    path_metadata = '__pypit_metadata__.json'

    metadata = PackageMetadata.parse(path_metadata) or PackageMetadata.create(path_metadata)
    metadata.auto_update()
    metadata.update_optional()
    metadata.save(path_metadata)
    metadata.generate_setup_py('setup.py')

    generate_rst_doc()

    setup_cli = SetupCli(metadata)
    build_proj(setup_cli)

    while True:
        print(yellow('[?]'), 'want to execute any action ?')
        method = pick_method(setup_cli)
        if method is not None:
            logger.info('begin {} ...'.format(method.__name__))
            method()
            logger.info('{} finished ...'.format(method.__name__))
        else:
            print('[DONE] all job finished.')
            return


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        if len(argv) == 1:
            return pypit('.')
        if len(argv) == 2:
            return pypit(argv[1])
        logger.error('unknown arguments.')
    except Stop:
        logger.info('User stop application.')
    except QuickExit as qe:
        logger.info(str(qe))
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    main()
