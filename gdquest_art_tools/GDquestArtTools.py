"""
GDquest Art Tools
-----------------
A collection of tools to improve Krita's workflow for game artists, graphic designers,
and everyone, really! 😉
"""
import os
import os.path as osp
from functools import partial
from krita import DockWidget, DockWidgetFactory, DockWidgetFactoryBase, Krita
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget

from .Infrastructure import WNode
from .Utils import kickstart, flip
from .Utils.Tree import iterPre, pathFS
from .Utils.Export import exportPath, makeDirs

KI = Krita.instance()


def exportAllLayers():
    doc = KI.activeDocument()
    root = doc.rootNode()
    root = WNode(root)
    dirname = osp.dirname(doc.fileName())
    makeDirs(root, dirname)
    it = filter(lambda n: n.isExportable() and n.isMarked(), iterPre(root))
    it = map(partial(flip(WNode.save), dirname), it)
    kickstart(it)


def exportSelectedLayers():
    def export(n, dirname=''):
        os.makedirs(exportPath(pathFS(n.parent), dirname), exist_ok=True)
        n.save(dirname)

    dirname = osp.dirname(KI.activeDocument().fileName())
    nodes = KI.activeWindow().activeView().selectedNodes()
    it = map(WNode, nodes)
    it = map(partial(flip(export), dirname), it)
    kickstart(it)


def renameLayers():
    print('test')


class GameArtTools(DockWidget):
    TITLE = 'GDquest Art Tools'

    def __init__(self):
        super().__init__()
        KI.setBatchmode(True)
        self.setWindowTitle(self.TITLE)
        self.createInterface()

    def createInterface(self):
        uiContainer = QWidget(self)

        exportLabel = QLabel('Export')
        exportAllLayersButton = QPushButton('All Layers')
        exportSelectedLayersButton = QPushButton('Selected Layers')
        renameLabel = QLabel('Rename')
        renameLineEdit = QLineEdit()
        renameButton = QPushButton('Rename')

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

        uiContainer.setLayout(vboxlayout)
        self.setWidget(uiContainer)

        exportSelectedLayersButton.released.connect(exportSelectedLayers)
        exportAllLayersButton.released.connect(exportAllLayers)
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

