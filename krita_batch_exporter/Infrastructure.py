import os
import re
from collections import OrderedDict
from functools import partial
from itertools import groupby, product, starmap, tee

from krita import Krita
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor, QImage, QPainter

from .Utils import flip, kickstart
from .Utils.Export import exportPath, sanitize
from .Utils.Tree import pathFS

KI = Krita.instance()


def nodeToImage(wnode):
    """
    Returns an QImage 8-bit sRGB
    """
    [x, y, w, h] = wnode.bounds
    return QImage(wnode.node.thumbnail(w, h))


def expand_and_format(img, margin=0, is_jpg=False):
    """
    Draws the image in a white background with the required format.
    It's done in a single function, to avoid creating extra images
    """
    if not margin and not is_jpg:
        return img
    corner = QSize(margin, margin)
    white = QColor(255, 255, 255) if is_jpg else QColor(255, 255, 255, 0)
    canvas = QImage(
        img.size() + corner * 2, QImage.Format_RGB32 if is_jpg else QImage.Format_ARGB32
    )
    canvas.fill(white)
    p = QPainter(canvas)
    p.drawImage(margin, margin, img)
    return canvas


class WNode:
    """
    Wrapper around Krita's Node class, that represents a layer.
    Adds support for export metadata and methods to export the layer
    based on its metadata.
    See the meta property for a list of supported metadata.
    """

    def __init__(self, cfg, node):
        self.cfg = cfg
        self.node = node

    def __bool__(self):
        return bool(self.node)

    @property
    def name(self):
        a = self.cfg["delimiters"]["assign"]
        name = self.node.name()
        name = name.split()
        name = filter(lambda n: a not in n, name)
        name = "_".join(name)
        return sanitize(name)

    @property
    def meta(self):
        a, s = self.cfg["delimiters"].values()
        meta = self.node.name().strip().split(a)
        meta = starmap(lambda fst, snd: (fst[-1], snd.split()[0]), zip(meta[:-1], meta[1:]))
        meta = filter(lambda m: m[0] in self.cfg["meta"].keys(), meta)
        meta = OrderedDict((k, v.lower().split(s)) for k, v in meta)
        meta.update({k: list(map(int, v)) for k, v in meta.items() if k in "ms"})
        meta.setdefault("c", self.cfg["meta"]["c"])  # coa_tools
        meta.setdefault("e", self.cfg["meta"]["e"])  # extension
        meta.setdefault("m", self.cfg["meta"]["m"])  # margin
        meta.setdefault("p", self.cfg["meta"]["p"])  # path
        meta.setdefault("s", self.cfg["meta"]["s"])  # scale
        return meta

    @property
    def path(self):
        return self.meta["p"][0]

    @property
    def coa(self):
        return self.meta["c"][0]

    @property
    def parent(self):
        return WNode(self.cfg, self.node.parentNode())

    @property
    def children(self):
        return [WNode(self.cfg, n) for n in self.node.childNodes()]

    @property
    def type(self):
        return self.node.type()

    @property
    def position(self):
        bounds = self.node.bounds()
        return bounds.x(), bounds.y()

    @property
    def bounds(self):
        bounds = self.node.bounds()
        return bounds.x(), bounds.y(), bounds.width(), bounds.height()

    @property
    def size(self):
        bounds = self.node.bounds()
        return bounds.width(), bounds.height()

    def hasDestination(self):
        return "d=" in self.node.name()

    def isExportable(self):
        return (
            self.isPaintLayer() or self.isGroupLayer() or self.isFileLayer() or self.isVectorLayer()
        )  # yapf: disable

    def isMarked(self):
        return "e=" in self.node.name()

    def isLayer(self):
        return "layer" in self.type

    def isMask(self):
        return "mask" in self.type

    def isPaintLayer(self):
        return self.type == "paintlayer"

    def isGroupLayer(self):
        return self.type == "grouplayer"

    def isFileLayer(self):
        return self.type == "filelayer"

    def isFilterLayer(self):
        return self.type == "filterlayer"

    def isFillLayer(self):
        return self.type == "filllayer"

    def isCloneLayer(self):
        return self.type == "clonelayer"

    def isVectorLayer(self):
        return self.type == "vectorlayer"

    def isTransparencyMask(self):
        return self.type == "transparencyMask"

    def isFilterMask(self):
        return self.type == "filtermask"

    def isTransformMask(self):
        return self.type == "transformmask"

    def isSelectionMask(self):
        return self.type == "selectionmask"

    def isColorizeMask(self):
        return self.type == "colorizemask"

    def rename(self, pattern):
        """
        Renames the layer, scanning for patterns in the user's input trying to preserve metadata.
        Patterns have the form meta_name=value,
        E.g. s=50,100 to tell the tool to export two copies of the layer at 50% and 100% of its size
        This function will only replace or update corresponding metadata.
        If the rename string starts with a name, the layer's name will change to that.
        """
        patterns = pattern.strip().split()
        a = self.cfg["delimiters"]["assign"]

        patterns = map(partial(flip(str.split), a), patterns)

        success, patterns = tee(patterns)
        success = map(lambda p: len(p) == 2, success)
        if not all(success):
            raise ValueError("malformed pattern.")

        key = lambda p: p[0] in self.cfg["meta"].keys()
        patterns = sorted(patterns, key=key)
        patterns = groupby(patterns, key)

        newName = self.node.name()
        for k, ps in patterns:
            for p in ps:
                how = (
                    "replace"
                    if k is False
                    else "add"
                    if p[1] != "" and "{}{}".format(p[0], a) not in newName
                    else "subtract"
                    if p[1] == ""
                    else "update"
                )
                pat = (
                    p
                    if how == "replace"
                    else (r"$", r" {}{}{}".format(p[0], a, p[1]))
                    if how == "add"
                    else (
                        r"\s*({}{})[\w,]+\s*".format(p[0], a),
                        " " if how == "subtract" else r" \g<1>{} ".format(p[1]),
                    )
                )
                newName = re.sub(pat[0], pat[1], newName).strip()
        self.node.setName(newName)

    def save(self, dirname=""):
        """
        Transform Node to a QImage
        processes the image, names it based on metadata, and saves the image to the disk.
        """
        img = nodeToImage(self)
        meta = self.meta
        margin, scale = meta["m"], meta["s"]
        extension, path = meta["e"], meta["p"][0]

        dirPath = (
            exportPath(self.cfg, path, dirname)
            if path
            else exportPath(self.cfg, pathFS(self.parent), dirname)
        )
        os.makedirs(dirPath, exist_ok=True)

        def append_name(path, name, scale, margin, extension):
            """
            Appends a formatted name to the path argument
            Returns the full path with the file
            """
            meta_s = self.cfg["meta"]["s"][0]
            out = os.path.join(path, name)
            out += "_@{}x".format(scale / 100) if scale != meta_s else ""
            out += "_m{:03d}".format(margin) if margin else ""
            out += "." + extension
            return out

        it = product(scale, margin, extension)
        # Below: scale for scale, margin for margin, extension for extension
        it = starmap(
            lambda scale, margin, extension: (
                scale,
                margin,
                extension,
                append_name(dirPath, self.name, scale, margin, extension),
            ),
            it,
        )
        it = starmap(
            lambda scale, margin, extension, path: (
                [int(1e-2 * wh * scale) for wh in self.size],
                100 - scale != 0,
                margin,
                extension,
                path,
            ),
            it,
        )
        it = starmap(
            lambda width_height, should_scale, margin, extension, path: (
                img.smoothScaled(*width_height) if should_scale else img,
                margin,
                extension,
                path,
            ),
            it,
        )
        it = starmap(
            lambda image, margin, extension, path: (
                expand_and_format(image, margin, is_jpg=extension in ("jpg", "jpeg")),
                path,
            ),
            it,
        )
        it = starmap(lambda image, path: image.save(path), it)
        kickstart(it)

    def saveCOA(self, dirname=""):
        img = nodeToImage(self)
        meta = self.meta
        path, extension = "", meta["e"]

        dirPath = (
            exportPath(self.cfg, path, dirname)
            if path
            else exportPath(self.cfg, pathFS(self.parent), dirname)
        )
        os.makedirs(dirPath, exist_ok=True)
        ext=extension[0]
        path = "{}{}".format(os.path.join(dirPath, self.name), ".{e}")
        path = path.format(e=ext)
        if ext in ("jpg", "jpeg"):
            img = expand_and_format(img, is_jpg=True)
        img.save(path)

        return path

    def saveCOASpriteSheet(self, dirname=""):
        """
        Generate a vertical sheet of equaly sized frames
        Each child of self is pasted to a master sheet
        """
        images = self.children
        tiles_x, tiles_y = 1, len(images)  # Length of vertical sheet
        image_width, image_height = self.size  # Target frame size
        sheet_width, sheet_height = (image_width, image_height * tiles_y)  # Sheet dimensions

        sheet = QImage(sheet_width, sheet_height, QImage.Format_ARGB32)
        sheet.fill(QColor(255, 255, 255, 0))
        painter = QPainter(sheet)

        p_coord_x, p_coord_y = self.position
        for count, image in enumerate(images):
            coord_x, coord_y = image.position
            coord_rel_x, coord_rel_y = coord_x - p_coord_x, coord_y - p_coord_y

            painter.drawImage(
                coord_rel_x, image_height * count + coord_rel_y, nodeToImage(image),
            )

        meta = self.meta
        path, extension = "", meta["e"]

        dirPath = (
            exportPath(self.cfg, path, dirname)
            if path
            else exportPath(self.cfg, pathFS(self.parent), dirname)
        )
        os.makedirs(dirPath, exist_ok=True)
        path = "{}{}".format(os.path.join(dirPath, self.name), ".{e}")
        path = path.format(e=extension[0])
        if extension in ("jpg", "jpeg"):
            sheet = expand_and_format(sheet, is_jpg=True)
        sheet.save(path)

        return path, {"tiles_x": tiles_x, "tiles_y": tiles_y}
