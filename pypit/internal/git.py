#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from fsoopify import FileInfo

from .utils import get_logger, lightgreen
from .model import ProjectInfo

GIT_IGNORES_VALUES = []
GIT_IGNORES_HEADER = '# pypit'

def configure_gitignore(proj_info: ProjectInfo):
    logger = get_logger()
    gitignore = FileInfo(proj_info.root_dir)

    if not gitignore.is_exists():
        logger.info(f'{lightgreen(gitignore)} does not exists')
        return

    gitignore_text = gitignore.read_text().splitlines()
    gitignore_set = set(gitignore_text)
    appends = []
    for line in GIT_IGNORES_VALUES:
        if line not in gitignore_set:
            appends.append(line)

    if appends:
        if GIT_IGNORES_HEADER in gitignore_set:
            raise NotImplementedError
        else:
            gitignore_text.append('')
            gitignore_text.append(GIT_IGNORES_HEADER)
            gitignore_text.extend(appends)

        gitignore.write_text('\n'.join(gitignore_text), append=False)
