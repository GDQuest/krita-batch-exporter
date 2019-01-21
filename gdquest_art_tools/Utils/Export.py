import os
import os.path as osp
import re
from . import kickstart
from .Tree import iterDirs
from ..Config import config


def exportPath(path, dirname=''):
    return osp.join(dirname, subRoot(path))


def subRoot(path):
    patF, patR = config['rootPat'], config['outDir']
    return re.sub(patF, patR, path, count=1)


def sanitize(path):
    ps = path.split(osp.sep)
    ps = map(lambda p: re.sub(config['sym'], '_', p), ps)
    ps = osp.sep.join(ps)
    return ps


def makeDirs(node, dirname=''):
    it = iterDirs(node)
    it = map(exportPath, it)
    it = map(lambda d: osp.join(dirname, d), it)
    it = map(lambda d: os.makedirs(d, exist_ok=True), it)
    kickstart(it)

