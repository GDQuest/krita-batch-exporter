"""
A collection of tools to improve Krita's workflow for game artists, graphic designers, and everyone, really! 😉
"""
from krita import *
from PyQt5.QtWidgets import QWidget
from .tools.layers_export_selected import *

class GameArtTools(DockWidget):
    TITLE = "Game Art Tools"

    def __init__(self):
        super().__init__()
        self.exportTools = LayerExportSelected()

        self.setWindowTitle(self.TITLE)
        self.createInterface()


    def createInterface(self):
        uiContainer = QWidget(self)

        exportDocumentButton = QPushButton("Export Document", uiContainer)
        exportDocumentButton.clicked.connect(self.exportTools.exportDocument)

        exportSelectedButton = QPushButton("Export Selected", uiContainer)
        exportSelectedButton.clicked.connect(self.exportTools.exportSelected)

        uiContainer.setLayout(QVBoxLayout())
        uiContainer.layout().addWidget(exportDocumentButton)
        uiContainer.layout().addWidget(exportSelectedButton)

        self.setWidget(uiContainer)

    def canvasChanged(self, canvas):
        pass



def register_docker():
    docker = DockWidgetFactory('pykrita_game_art_tools',
                            DockWidgetFactoryBase.DockRight,
                            GameArtTools)
    Krita.instance().addDockWidgetFactory(docker)

register_docker()
