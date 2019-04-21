import sys
from functools import partial
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from players import Player


qtCreatorFile = "tic_tac_ui.ui"
Ui_MainWindow, _ = uic.loadUiType(qtCreatorFile)


class TicTacMainWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.cells = [self.cell_0,
                      self.cell_1,
                      self.cell_2,
                      self.cell_3,
                      self.cell_4,
                      self.cell_5,
                      self.cell_6,
                      self.cell_7,
                      self.cell_8]

        self.player = None
        self.actionSetAsServer.triggered.connect(self.makeServerPlayer)
        self.actionSetAsClient.triggered.connect(self.makeClientPlayer)

        for cell in self.cells:
            cell.clicked.connect(partial(self.drawShape, cell))

    @pyqtSlot()
    def makeServerPlayer(self):
        self.player = Player("server")
        self.updateStatusBar()

    @pyqtSlot()
    def makeClientPlayer(self):
        self.player = Player("client")
        self.updateStatusBar()

    def updateStatusBar(self):
        self.statusbar.showMessage(str(self.player))

    @pyqtSlot()
    def drawShape(self, label):
        if self.player is not None and not label.hasShape:
            label.drawShape(self.player.shape)


if __name__ == '__main__':
    myApp = QApplication(sys.argv)
    game = TicTacMainWin()
    game.show()
    sys.exit(myApp.exec_())
