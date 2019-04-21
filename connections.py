from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

_HOST = '127.0.0.1'
_PORT = 65432


class ConnectionInitializer(QObject):

    start = pyqtSignal()
    connectionEstablished = pyqtSignal()

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
        elif self.player.isClient:
            self.player.socket.connect((_HOST, _PORT))
        self.connectionEstablished.emit()


class MessageInterface(QObject):

    commStart = pyqtSignal()
    msgSent = pyqtSignal()
    msgReceived = pyqtSignal()

    def __init__(self, player, parent=None):
        super().__init__(parent)
        self.player = player
        self.commStart.connect(self.communicate)

    def communicate(self):
        if self.player.isReceiving:
            if self.player.isServer:
                data = self.player.clientSocket.recv(1024)
            else:
                data = self.player.socket.recv(1024)
            if data:
                self.player.msgCell = data.decode()
                self.msgReceived.emit()
        elif self.player.isSending:
            msg = self.player.msgCell.encode()
            sent = ""
            if self.player.isServer:
                sent = self.player.clientSocket.sendall(msg)
            else:
                sent = self.player.socket.sendall(msg)
            if sent is None:
                self.msgSent.emit()
