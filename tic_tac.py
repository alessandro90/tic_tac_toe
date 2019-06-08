import sys
from functools import partial
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from players import Player
from connections import ConnectionInitializer, MessageInterface
from board import Board
from result import Result


qtCreatorFile = "tic_tac_ui.ui"
Ui_MainWindow, _ = uic.loadUiType(qtCreatorFile)


class TicTacMainWin(QMainWindow, Ui_MainWindow):

    signalConnection = pyqtSignal()
    signalInitializeConn = pyqtSignal()

    def __init__(self, host_name):
        super().__init__()
        self.setupUi(self)
        self.endOfGame = False
        self.cells = (
            self.cell_0,
            self.cell_1,
            self.cell_2,
            self.cell_3,
            self.cell_4,
            self.cell_5,
            self.cell_6,
            self.cell_7,
            self.cell_8
        )

        self.board = Board(self.cells)

        self.connected = False
        self.player = Player()
        self.actionSetAsServer.triggered.connect(self.makeServerPlayer)
        self.actionSetAsClient.triggered.connect(self.makeClientPlayer)

        self.connectionThread = QThread()
        self.connectionThread.start()
        self.connectionInitializer = ConnectionInitializer(
            self.player, host_name
        )
        self.connectionInitializer.moveToThread(self.connectionThread)
        self.connectionInitializer.connectionEstablished.connect(
            self.setConnected
        )

        self.connectionInitializer.connectionError.connect(
            self.disconnect
        )

        self.actionConnect.triggered.connect(
            lambda: self.connectionInitializer.start.emit()
        )

        self.actionInfo.triggered.connect(self.showInfoBox)

        self.msgThread = QThread()
        self.msgThread.start()
        self.messageInterface = MessageInterface(self.player)
        self.messageInterface.msgSent.connect(self.messageSent)
        self.messageInterface.msgReceived.connect(self.messageReceived)
        self.messageInterface.msgError.connect(self.disconnect)
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
        self.checkForWinner()
        if self.endOfGame and self.player.matchResult is Result.WIN:
            self.player.isSending = True
        else:
            self.player.isReceiving = True
            self.signalConnection.emit()

    @pyqtSlot()
    def messageReceived(self):
        index = int(self.player.msgCell)
        self.cells[index].drawShape(self.player.opponentShape)
        self.checkForWinner()
        if self.endOfGame and self.player.matchResult is Result.LOOSE:
            self.player.isReceiving = True
            self.signalConnection.emit()
        else:
            self.player.isSending = True

    @pyqtSlot()
    def disconnect(self):
        self.connected = False
        if self.player.socket is not None:
            self.player.socket.close()
        if self.player.clientSocket is not None:
            self.player.clientSocket.close()
        self.player.reset()
        self.updateStatusBar()

    @pyqtSlot()
    def setConnected(self):
        self.connected = True
        if self.player.isServer:
            self.signalConnection.emit()
        self.updateStatusBar()

    @pyqtSlot()
    def makeServerPlayer(self):
        if not self.connected:
            self.player.setRole("server")
            self.player.isReceiving = True
            self.updateStatusBar()

    @pyqtSlot()
    def makeClientPlayer(self):
        if not self.connected:
            self.player.setRole("client")
            self.player.isSending = True
            self.updateStatusBar()

    def updateStatusBar(self):
        self.statusbar.showMessage(
            f"{self.player}. Connected: {'Yes' if self.connected else 'No'}"
        )

    @pyqtSlot()
    def drawShape(self, cell):
        if self.player.isSending and self.connected:
            if self.player is not None and not cell.hasShape:
                cell.drawShape(self.player.shape)
                self.player.msgCell = str(cell.index)
                self.signalConnection.emit()

    def checkForWinner(self):
        mustClean = False
        self.endOfGame = False
        if self.board.checkForWinner(self.player.shape):
            self.board.showWinningCells()
            matchResult = Result.WIN
            mustClean = True
        elif self.board.checkForWinner(self.player.opponentShape):
            self.board.showWinningCells()
            matchResult = Result.LOOSE
            mustClean = True
        elif self.board.boardIsFull():
            mustClean = True
            matchResult = Result.TIE
        if mustClean:
            self.endOfGame = True
            self.player.matchResult = matchResult
            self.board.clean()

    @pyqtSlot()
    def showInfoBox(self):
        msg = f"Status: {self.player.strStatus}.\n" + \
            f"Symbol: {self.player.strSymbol}.\n"
        status = 'Connected' if self.connected else 'Not connected'
        msg += f"Connection: {status}.\n"
        if self.connected:
            if self.player.isSending:
                msg += "Your turn."
            else:
                msg += "Opponent turn."
        else:
            msg += "No player 2."
        box = QMessageBox(self)
        box.setWindowTitle("Connection info")
        box.setText(msg)
        box.setStyleSheet(
            """
            background-color: #282828;
            color: #ffffff;
            """
        )
        box.show()

    def closeSocketsAndThreads(self):
        if self.player.socket is not None:
            self.player.socket.close()
        if self.player.clientSocket is not None:
            self.player.clientSocket.close()
        self.connectionInitializer.closeApp = True
        self.messageInterface.closeApp = True
        self.connectionThread.quit()
        self.connectionThread.wait()
        self.msgThread.quit()
        self.msgThread.wait()

    def closeEvent(self, event):
        self.closeSocketsAndThreads()
        super().closeEvent(event)


if __name__ == '__main__':
    myApp = QApplication(sys.argv)
    if len(sys.argv) == 2:
        host_name = sys.argv[1]
    else:
        host_name = None
    game = TicTacMainWin(host_name)
    game.show()
    sys.exit(myApp.exec_())
