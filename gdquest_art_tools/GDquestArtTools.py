"""
GDquest Art Tools
-----------------
A collection of tools to improve Krita's workflow for game artists, graphic designers,
and everyone, really! 😉
"""
from krita import DockWidget, DockWidgetFactory, DockWidgetFactoryBase, Krita
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget

from .Infrastructure import WNode
from .Utils import kickstart
from .Utils.Tree import iterPre
from .Utils.Export import makeDirs


KI = Krita.instance()


def exportAllLayers():
    root = WNode(KI.activeDocument().rootNode())
    makeDirs(root)
    it = filter(lambda n: n.isExportable(), iterPre(root))
    it = map(lambda n: n.save(), it)
    kickstart(it)


def exportSelectedLayers():
    root = WNode(KI.activeDocument().rootNode())
    makeDirs(root)
    it = map(WNode, KI.activeWindow().activeView().selectedNodes())
    it = map(lambda n: n.save(), it)
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
    docker = DockWidgetFactory('pykrita_gdquest_art_tools',
                               DockWidgetFactoryBase.DockRight,
                               GameArtTools)
    KI.addDockWidgetFactory(docker)

