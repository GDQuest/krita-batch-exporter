from .Config import config
from .Utils.Export import subRoot
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
        return name

    @property
    def meta(self):
        meta = self.node.name()
        meta = meta.split()
        meta = filter(lambda m: '=' in m, meta)
        return meta

    @property
    def extension(self):
        ext = filter(lambda m: 'e=' in m, self.meta)
        ext = ''.join(ext)
        ext = ext.split('=')
        ext = ext[-1]
        ext = ext.lower()
        return ext

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
        return self.extension in config['supportedExtensions']

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

    def save(self):
        nd = self.node.duplicate()
        name = subRoot(pathFS(self)), self.extension or 'png'
        nd.save('.'.join(name), *self.size)

