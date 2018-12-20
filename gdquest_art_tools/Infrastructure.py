from itertools import product, starmap
import os
import os.path as osp
from PIL import Image, ImageOps

from .Utils import kickstart
from .Utils.Export import sanitize, subRoot
from .Utils.Tree import pathFS


class WNode:
    def __init__(self, node):
        self.node = node

    def __bool__(self):
        return bool(self.node)

    @property
    def name(self):
        name = self.node.name()
        name = name.split()
        name = filter(lambda n: '=' not in n, name)
        name = '_'.join(name)
        return sanitize(name)

    @property
    def meta(self):
        d = '=', ','
        meta = self.node.name()
        meta = meta.strip()
        meta = meta.split()
        meta = map(lambda m: m.strip(), meta)
        meta = filter(lambda m: d[0] in m, meta)
        meta = map(lambda m: m.split(d[0]), meta)
        meta = {
            k: (list(map(lambda s: int(s), v.split(d[1]))) if k in 'sm' else v.split(d[1].lower()))
            for k, v in meta
        }  # yapf: disable
        meta.setdefault('e', ['png'])  # extension
        meta.setdefault('s', [100])  # scale
        meta.setdefault('m', [0])  # margin
        meta.setdefault('d', [''])  # path
        return meta

    @property
    def parent(self):
        return WNode(self.node.parentNode())

    @property
    def children(self):
        return [WNode(n) for n in self.node.childNodes()]

    @property
    def type(self):
        return self.node.type()

    @property
    def bounds(self):
        bounds = self.node.bounds()
        return bounds.x(), bounds.y(), bounds.width(), bounds.height()

    @property
    def size(self):
        bounds = self.node.bounds()
        return bounds.width(), bounds.height()

    def isExportable(self):
        return (self.isPaintLayer()
                or self.isGroupLayer()
                or self.isFileLayer()
                or self.isVectorLayer())  # yapf: disable

    def isMarked(self):
        return 'e=' in self.node.name()

    def isLayer(self):
        return 'layer' in self.type

    def isMask(self):
        return 'mask' in self.type

    def isPaintLayer(self):
        return self.type == 'paintlayer'

    def isGroupLayer(self):
        return self.type == 'grouplayer'

    def isFileLayer(self):
        return self.type == 'filelayer'

    def isFilterLayer(self):
        return self.type == 'filterlayer'

    def isFillLayer(self):
        return self.type == 'filllayer'

    def isCloneLayer(self):
        return self.type == 'clonelayer'

    def isVectorLayer(self):
        return self.type == 'vectorlayer'

    def isTransparencyMask(self):
        return self.type == 'transparencyMask'

    def isFilterMask(self):
        return self.type == 'filtermask'

    def isTransformMask(self):
        return self.type == 'transformmask'

    def isSelectionMask(self):
        return self.type == 'selectionmask'

    def isColorizeMask(self):
        return self.type == 'colorizemask'

    def dataToPIL(self):
        nd = self.node.duplicate()
        nd.setColorSpace('RGBA', 'U8', 'sRGB-elle-V2-srgbtrc')
        img = nd.projectionPixelData(*self.bounds).data()
        img = Image.frombytes('RGBA', self.size, img, 'raw', 'BGRA', 0, 1)
        return img

    def save(self):
        def toJPEG(img):
            newImg = Image.new('RGBA', img.size, 4 * (255,))
            newImg.alpha_composite(img)
            return newImg.convert('RGB')

        img = self.dataToPIL()
        path, ext, margin, scale = (self.meta['d'][0], self.meta['e'],
                                    self.meta['m'][0], self.meta['s'])
        path and os.makedirs(path, exist_ok=True)
        path = '{}_{}'.format(osp.join(path, self.name) if path else subRoot(pathFS(self)),
                              's{s:03d}.{e}')  # yapf: disable

        it = product(ext, scale)
        it = starmap(lambda e, s: (s, e, path.format(e=e, s=s)), it)
        it = starmap(lambda s, e, p: ([int(1e-2*wh*s) for wh in self.size], 100 - s != 0, e, p), it)
        it = starmap(lambda sWH, sDo, e, p: (img.resize(sWH, Image.LANCZOS)
                                             if sDo else img, e, p), it)
        it = starmap(lambda i, e, p: (ImageOps.expand(i, margin, (255, 255, 255, 0)), e, p), it)
        it = starmap(lambda i, e, p: (toJPEG(i) if e in ('jpg', 'jpeg') else i, p), it)
        it = starmap(lambda i, p: i.save(p), it)
        kickstart(it)

