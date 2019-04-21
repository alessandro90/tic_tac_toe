import sys
from functools import partial
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from players import Player
from connections import ConnectionInitializer, MessageInterface

qtCreatorFile = "tic_tac_ui.ui"
Ui_MainWindow, _ = uic.loadUiType(qtCreatorFile)


class TicTacMainWin(QMainWindow, Ui_MainWindow):

    signalConnection = pyqtSignal()
    signalInitializeConn = pyqtSignal()

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
            self.setConnected
        )

        self.actionConnect.triggered.connect(
            lambda: self.connectionInitializer.start.emit())

        self.msgThread = QThread()
        self.msgThread.start()
        self.messageInterface = MessageInterface(self.player)
        self.messageInterface.msgSent.connect(self.messageSent)
        self.messageInterface.msgReceived.connect(self.messageReceived)
        self.messageInterface.moveToThread(self.msgThread)

        self.signalInitializeConn.connect(
            self.connectionInitializer.establishConnection
        )

        self.signalConnection.connect(
            self.messageInterface.communicate
        )

        for index, cell in enumerate(self.cells):
            cell.index = index
            cell.clicked.connect(partial(self.drawShape, cell))

    @pyqtSlot()
    def messageSent(self):
        self.player.isSending = False
        self.signalConnection.emit()

    @pyqtSlot()
    def messageReceived(self):
        index = int(self.player.msgCell)
        self.cells[index].drawShape(self.player.opponentShape)
        self.player.isReceiving = False

    @pyqtSlot()
    def setConnected(self):
        self.connected = True
        if self.player.isServer:
            self.signalConnection.emit()
        self.updateStatusBar()

    @pyqtSlot()
    def makeServerPlayer(self):
        self.player.setRole("server")
        self.player.isReceiving = True
        self.updateStatusBar()

    @pyqtSlot()
    def makeClientPlayer(self):
        self.player.setRole("client")
        self.player.isSending = True
        self.updateStatusBar()

    def updateStatusBar(self):
        self.statusbar.showMessage(
            f"{self.player}. Connected: {'Yes' if self.connected else 'No'}"
        )

    @pyqtSlot()
    def drawShape(self, cell):
        if self.player.isSending:
            if self.player is not None and not cell.hasShape:
                cell.drawShape(self.player.shape)
                self.player.msgCell = str(cell.index)
                self.signalConnection.emit()

    def closeEvent(self, event):
        self.connectionThread.quit()
        self.connectionThread.wait()
        self.msgThread.quit()
        self.msgThread.terminate()
        self.msgThread.wait()
        if self.player.socket is not None:
            self.player.socket.close()
            if self.player.clientSocket is not None:
                self.player.clientSocket.close()
        super().closeEvent(event)


if __name__ == '__main__':
    myApp = QApplication(sys.argv)
    game = TicTacMainWin()
    game.show()
    sys.exit(myApp.exec_())
