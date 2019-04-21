from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

_HOST = '127.0.0.1'
_PORT = 65432


class ConnectionInitializer(QObject):

    start = pyqtSignal()
    connectionEstablished = pyqtSignal()
    connectionError = pyqtSignal()

    def __init__(self, player, parent=None):
        super().__init__(parent)
        self.player = player
        self.start.connect(self.establishConnection)

    @pyqtSlot()
    def establishConnection(self):
        if self.player.isServer:
            self.player.socket.bind((_HOST, _PORT))
            self.player.socket.listen()
            self.player.clientSocket, _ = self.player.socket.accept()
            self.connectionEstablished.emit()
        elif self.player.isClient:
            try:
                self.player.socket.connect((_HOST, _PORT))
            except Exception:
                self.connectionError.emit()
            else:
                self.connectionEstablished.emit()


class MessageInterface(QObject):

    commStart = pyqtSignal()
    msgSent = pyqtSignal()
    msgReceived = pyqtSignal()
    msgError = pyqtSignal()

    def __init__(self, player, parent=None):
        super().__init__(parent)
        self.player = player
        self.commStart.connect(self.communicate)

    def communicate(self):
        if self.player.isReceiving:
            try:
                if self.player.isServer:
                    data = self.player.clientSocket.recv(1024)
                else:
                    data = self.player.socket.recv(1024)
            except Exception:
                self.msgError.emit()
            if data:
                self.player.msgCell = data.decode()
                self.msgReceived.emit()
        elif self.player.isSending:
            msg = self.player.msgCell.encode()
            sent = ""
            try:
                if self.player.isServer:
                    sent = self.player.clientSocket.sendall(msg)
                else:
                    sent = self.player.socket.sendall(msg)
            except Exception:
                self.msgError.emit()
            if sent is None:
                self.msgSent.emit()
