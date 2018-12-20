import os.path as osp
import re
from ..Config import config


def subRoot(path):
    patF, patR = config['rootPat'], config['outDir']
    return re.sub(patF, patR, path, count=1)


def sanitize(path):
    ps = path.split(osp.sep)
    ps = map(lambda p: re.sub(config['sym'], '_', p), ps)
    ps = osp.sep.join(ps)
    return ps

