"""
GDquest Art Tools
-----------------
A collection of tools to improve Krita's workflow for game artists, graphic designers,
and everyone, really! 😉
"""
import os.path as osp
from functools import partial
from krita import DockWidget, DockWidgetFactory, DockWidgetFactoryBase, Krita
from PyQt5.QtWidgets import (QPushButton, QStatusBar, QLabel, QLineEdit, QHBoxLayout,
                             QVBoxLayout, QWidget)

from .Infrastructure import WNode
from .Utils import kickstart, flip
from .Utils.Tree import iterPre

KI = Krita.instance()
ERROR_MSG = 'ERROR: only RGBA & 8bit depth supported!'
ERROR_TIMEOUT = 8000
DONE_TIMEOUT = 5000


def ensureRGBAU8(doc, statusBar):
    ensured = doc.colorModel() == 'RGBA' and doc.colorDepth() == 'U8'
    if not ensured:
        statusBar.showMessage(ERROR_MSG, ERROR_TIMEOUT)
    return ensured


def exportAllLayers(statusBar):
    doc = KI.activeDocument()
    if not ensureRGBAU8(doc, statusBar):
        return

    root = doc.rootNode()
    root = WNode(root)

    dirname = osp.dirname(doc.fileName())
    it = filter(lambda n: n.isExportable() and n.isMarked(), iterPre(root))
    it = map(partial(flip(WNode.save), dirname), it)
    kickstart(it)

    statusBar.showMessage('Exported all layers.', DONE_TIMEOUT)


def exportSelectedLayers(statusBar):
    doc = KI.activeDocument()
    if not ensureRGBAU8(doc, statusBar):
        return

    dirname = osp.dirname(doc.fileName())
    nodes = KI.activeWindow().activeView().selectedNodes()
    it = map(WNode, nodes)
    it = map(partial(flip(WNode.save), dirname), it)
    kickstart(it)

    statusBar.showMessage('Exported selected layers.', DONE_TIMEOUT)


def renameLayers():
    print('test')


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
        renameLabel = QLabel('Rename')
        renameLineEdit = QLineEdit()
        renameButton = QPushButton('Rename')
        statusBar = QStatusBar()

        vboxlayout = QVBoxLayout()
        vboxlayout.addWidget(exportLabel)
        vboxlayout.addWidget(exportAllLayersButton)
        vboxlayout.addWidget(exportSelectedLayersButton)
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

        exportSelectedLayersButton.released.connect(partial(exportSelectedLayers, statusBar))
        exportAllLayersButton.released.connect(partial(exportAllLayers, statusBar))
        renameLineEdit.returnPressed.connect(renameLayers)
        renameButton.released.connect(renameLayers)

    def canvasChanged(self, canvas):
        pass


def registerDocker():
    docker = DockWidgetFactory(
        'pykrita_gdquest_art_tools',
        DockWidgetFactoryBase.DockRight,
        GameArtTools
    )
    KI.addDockWidgetFactory(docker)

