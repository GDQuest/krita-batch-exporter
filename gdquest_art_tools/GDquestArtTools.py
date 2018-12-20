"""
GDquest Art Tools
-----------------
A collection of tools to improve Krita's workflow for game artists, graphic designers,
and everyone, really! 😉
"""
import os
from krita import DockWidget, DockWidgetFactory, DockWidgetFactoryBase, Krita
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget

from .Infrastructure import WNode
from .Utils import kickstart
from .Utils.Tree import iterPre, pathFS, makeDirs
from .Utils.Export import subRoot

KI = Krita.instance()


def exportAllLayers():
    root = KI.activeDocument().rootNode()
    root = WNode(root)
    makeDirs(root)
    it = filter(lambda n: n.isExportable() and n.isMarked(), iterPre(root))
    it = map(WNode.save, it)
    kickstart(it)


def exportSelectedLayers():
    def export(n):
        os.makedirs(subRoot(pathFS(n.parent)), exist_ok=True)
        n.save()

    nodes = KI.activeWindow().activeView().selectedNodes()
    it = map(WNode, nodes)
    it = map(export, it)
    kickstart(it)


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
        exportAllLayersButton = QPushButton('All Layers', uiContainer)
        exportAllLayersButton.released.connect(exportAllLayers)

        exportSelectedLayersButton = QPushButton('Selected Layers', uiContainer)
        exportSelectedLayersButton.released.connect(exportSelectedLayers)

        uiContainer.setLayout(QVBoxLayout())
        uiContainer.layout().addWidget(exportLabel)
        uiContainer.layout().addWidget(exportAllLayersButton)
        uiContainer.layout().addWidget(exportSelectedLayersButton)

        self.setWidget(uiContainer)

    def canvasChanged(self, canvas):
        pass


def registerDocker():
    docker = DockWidgetFactory(
        'pykrita_gdquest_art_tools',
        DockWidgetFactoryBase.DockRight,
        GameArtTools
    )
    KI.addDockWidgetFactory(docker)

