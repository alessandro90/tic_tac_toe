import sys
from functools import partial
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QThread
from players import Player
from connections import ConnectionInitializer

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

        self.connected = False
        self.player = Player()
        self.actionSetAsServer.triggered.connect(self.makeServerPlayer)
        self.actionSetAsClient.triggered.connect(self.makeClientPlayer)

        self.connectionThread = QThread()
        self.connectionThread.start()
        self.connectionInitializer = ConnectionInitializer(self.player)
        self.connectionInitializer.moveToThread(self.connectionThread)
        self.connectionInitializer.connectionEstablished.connect(
            self.setConnected)

        self.actionConnect.triggered.connect(
            lambda: self.connectionInitializer.start.emit())

        for cell in self.cells:
            cell.clicked.connect(partial(self.drawShape, cell))

    @pyqtSlot()
    def setConnected(self):
        self.connected = True

    @pyqtSlot()
    def makeServerPlayer(self):
        self.player.setRole("server")
        self.updateStatusBar()

    @pyqtSlot()
    def makeClientPlayer(self):
        self.player.setRole("client")
        self.updateStatusBar()

    def updateStatusBar(self):
        self.statusbar.showMessage(str(self.player))

    @pyqtSlot()
    def drawShape(self, label):
        if self.player is not None and not label.hasShape:
            label.drawShape(self.player.shape)

    def closeEvent(self, event):
        self.connectionThread.quit()
        self.connectionThread.wait()
        super().closeEvent(event)


if __name__ == '__main__':
    myApp = QApplication(sys.argv)
    game = TicTacMainWin()
    game.show()
    sys.exit(myApp.exec_())
