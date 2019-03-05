"""
GDquest Art Tools
-----------------
A collection of tools to improve Krita's workflow for game artists, graphic designers,
and everyone, really! 😉
"""
import os.path as osp
from functools import partial
from krita import DockWidget, DockWidgetFactory, DockWidgetFactoryBase, Krita
from PyQt5.QtWidgets import (
    QPushButton,
    QStatusBar,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QWidget
)

from .Config import CONFIG
from .Infrastructure import WNode
from .COATools import COAToolsFormat
from .Utils import kickstart, flip
from .Utils.Tree import iterPre

KI = Krita.instance()


def ensureRGBAU8(doc):
    ensured = doc.colorModel() == 'RGBA' and doc.colorDepth() == 'U8'
    if not ensured:
        raise ValueError('only RGBA 8-bit depth supported!')


def exportAllLayers(cfg, statusBar):
    msg, timeout = cfg['done']['msg'].format('Exported all layers.'), cfg['done']['timeout']
    try:
        doc = KI.activeDocument()
        ensureRGBAU8(doc)

        root = doc.rootNode()
        root = WNode(cfg, root)

        dirName = osp.dirname(doc.fileName())
        it = filter(lambda n: n.isExportable() and n.isMarked(), iterPre(root))
        it = map(partial(flip(WNode.save), dirName), it)
        kickstart(it)
    except ValueError as e:
        msg, timeout = cfg['error']['msg'].format(e), cfg['error']['timeout']
    statusBar.showMessage(msg, timeout)


def exportSelectedLayers(cfg, statusBar):
    msg, timeout = cfg['done']['msg'].format('Exported selected layers.'), cfg['done']['timeout']
    try:
        doc = KI.activeDocument()
        ensureRGBAU8(doc)

        dirName = osp.dirname(doc.fileName())
        nodes = KI.activeWindow().activeView().selectedNodes()
        it = map(partial(WNode, cfg), nodes)
        it = map(partial(flip(WNode.save), dirName), it)
        kickstart(it)
    except ValueError as e:
        msg, timeout = cfg['error']['msg'].format(e), cfg['error']['timeout']
    statusBar.showMessage(msg, timeout)

def exportCOATools(cfg, statusBar):
    msg, timeout = cfg['done']['msg'].format('Exported selected layers.'), cfg['done']['timeout']
    try:
        doc = KI.activeDocument()
        ensureRGBAU8(doc)

        coat_format = COAToolsFormat(cfg, statusBar)
        dirName = osp.dirname(doc.fileName())
        nodes = KI.activeWindow().activeView().selectedNodes()

        # By convention all selected nodes should be Group Layers
        for n in nodes:
            wn = WNode(cfg, n)
            if not wn.isGroupLayer():
                raise ValueError(wn.name,'is not a Group Layer')

        it = map(partial(WNode, cfg), nodes)
        it = map(lambda n: coat_format.collect(n), it)
        kickstart(it)
        coat_format.save(dirName)
    except ValueError as e:
        msg, timeout = cfg['error']['msg'].format(e), cfg['error']['timeout']
    statusBar.showMessage(msg, timeout)


def renameLayers(cfg, statusBar, lineEdit):
    msg, timeout = cfg['done']['msg'].format('Renaming successful!'), cfg['done']['timeout']
    try:
        nodes = KI.activeWindow().activeView().selectedNodes()
        it = map(partial(WNode, cfg), nodes)
        it = map(partial(flip(WNode.rename), lineEdit.text()), it)
        kickstart(it)
    except ValueError as e:
        msg, timeout = cfg['error']['msg'].format(e), cfg['error']['timeout']
    statusBar.showMessage(msg, timeout)


class GameArtTools(DockWidget):
    title = 'GDquest Art Tools'

    def __init__(self):
        super().__init__()
        KI.setBatchmode(True)
        self.setWindowTitle(self.title)
        self.createInterface()

    def createInterface(self):
        uiContainer = QWidget(self)

        exportLabel = QLabel('Export')
        exportAllLayersButton = QPushButton('All Layers')
        exportSelectedLayersButton = QPushButton('Selected Layers')
        exportSelectedCOAToolsLayersButton = QPushButton('Selected as coa_tools')
        renameLabel = QLabel('Update Layer Meta/Name')
        renameLineEdit = QLineEdit()
        renameButton = QPushButton('Update')
        statusBar = QStatusBar()

        vboxlayout = QVBoxLayout()
        vboxlayout.addWidget(exportLabel)
        vboxlayout.addWidget(exportAllLayersButton)
        vboxlayout.addWidget(exportSelectedLayersButton)
        vboxlayout.addWidget(exportSelectedCOAToolsLayersButton)
        vboxlayout.addWidget(renameLabel)
        vboxlayout.addWidget(renameLineEdit)

        hboxlayout = QHBoxLayout()
        hboxlayout.addStretch()
        hboxlayout.addWidget(renameButton)

        vboxlayout.addLayout(hboxlayout)
        vboxlayout.addStretch()
        vboxlayout.addWidget(statusBar)

        uiContainer.setLayout(vboxlayout)
        self.setWidget(uiContainer)

        exportSelectedLayersButton.released.connect(
            partial(exportSelectedLayers,
                    CONFIG,
                    statusBar)
        )
        exportAllLayersButton.released.connect(partial(exportAllLayers, CONFIG, statusBar))
        exportSelectedCOAToolsLayersButton.released.connect(partial(exportCOATools, CONFIG, statusBar))
        renameLineEdit.returnPressed.connect(
            partial(renameLayers,
                    CONFIG,
                    statusBar,
                    renameLineEdit)
        )
        renameButton.released.connect(partial(renameLayers, CONFIG, statusBar, renameLineEdit))

    def canvasChanged(self, canvas):
        pass


def registerDocker():
    docker = DockWidgetFactory(
        'pykrita_gdquest_art_tools',
        DockWidgetFactoryBase.DockRight,
        GameArtTools
    )
    KI.addDockWidgetFactory(docker)
