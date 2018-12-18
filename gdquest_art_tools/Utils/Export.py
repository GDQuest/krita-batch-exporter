import os
import re
from itertools import chain

from . import kickstart
from .Tree import iterPre, pathFS
from ..Config import config


def subRoot(path):
    patF, patR = config['rootPat'], config['outDir']
    return re.sub(patF, patR, path, count=1)


def iterDirs(node):
    it = iterPre(node)
    it = filter(lambda n: n.isGroupLayer(), it)
    it = filter(lambda n:
                any(i.isExportable()
                    for i in chain(*map(lambda c: iterPre(c), n.children))),
                it)
    it = map(pathFS, it)
    it = map(subRoot, it)
    return it


def makeDirs(node):
    it = iterDirs(node)
    it = map(lambda d: os.makedirs(d, exist_ok=True), it)
    kickstart(it)

