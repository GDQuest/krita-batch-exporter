import os.path as osp
import re
from ..Config import CONFIG


def exportPath(cfg, path, dirname=''):
    return osp.join(dirname, subRoot(cfg, path))


def subRoot(cfg, path):
    patF, patR = cfg['rootPat'], CONFIG['outDir']
    return re.sub(patF, patR, path, count=1)


def sanitize(path):
    ps = path.split(osp.sep)
    ps = map(lambda p: re.sub(CONFIG['sym'], '_', p), ps)
    ps = osp.sep.join(ps)
    return ps
