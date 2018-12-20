import os.path as osp
import sys
sys.path.append(osp.abspath(osp.join(osp.dirname(__file__), 'Dependencies')))
from .GDquestArtTools import registerDocker  # noqa

registerDocker()

