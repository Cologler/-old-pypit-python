# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

class KeyValuePair:
    def __init__(self, key):
        self.key = key
        self.value = None

class Section:
    def __init__(self, name):
        self._name = name.split('.')
        self._items = []

    @property
    def name(self):
        return self._name

    @property
    def items(self):
        return self._items

class CFGFile:
    def __init__(self):
        self._sections = []

    @property
    def sections(self):
        return self._sections

class LineReader:
    def __init__(self, src):
        self._lines = src.splitlines()
        self._index = 0

    def end(self) -> bool:
        return self._index >= len(self._lines)

    def readline(self) -> str:
        '''read and move'''
        line = self._lines[self._index]
        self._index += 1
        return line

    def viewline(self) -> str:
        return self._lines[self._index]

def loadstr(text: str):
    reader = LineReader(text)
    cfg_file = CFGFile()
    section = None
    while not reader.end():
        line = reader.readline()
        if line.startswith('['):
            assert line.endswith(']')
            section = Section(line[1:-1])
            cfg_file.sections.append(section)
        elif line.strip(): # not empty
            name, value = line.split('=', 2)
            assert len(line) == 2
            kvp = KeyValuePair(name.strip())
            section.items.append(kvp)
            value = value.strip()
            if value:
                kvp.value = value
            else:
                kvp.value = []
                while not reader.end() and reader.viewline().startswith(' '):
                    next_line = reader.readline()
                    kvp.value.append(next_line.strip())
    return cfg_file
