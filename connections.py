from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


_HOST = '127.0.0.1'
_PORT = 65432


class ConnectionInitializer(QObject):

    start = pyqtSignal()
    connectionEstablished = pyqtSignal()
    connectionError = pyqtSignal()

    def __init__(self, player, host_name, parent=None):
        super().__init__(parent)
        self.player = player
        self.start.connect(self.establishConnection)
        if host_name is None:
            self._host = _HOST
        else:
            self._host = host_name
        self.closeApp = False

    @pyqtSlot()
    def establishConnection(self):
        if self.player.isServer:
            try:
                self.player.socket.bind((self._host, _PORT))
            except Exception:
                self.connectionError.emit()
            else:
                self.player.socket.listen()
                while True:
                    try:
                        self.player.clientSocket, _ = self.player.socket.accept()
                    except Exception:
                        pass
                    else:
                        self.clientSocket.settimeout(1)
                        self.connectionEstablished.emit()
                        break
                    if self.closeApp:
                        break
        elif self.player.isClient:
            try:
                self.player.socket.connect((self._host, _PORT))
            except Exception:
                self.connectionError.emit()
            else:
                self.connectionEstablished.emit()


class MessageInterface(QObject):

    msgSent = pyqtSignal()
    msgReceived = pyqtSignal()
    msgError = pyqtSignal()

    def __init__(self, player, parent=None):
        super().__init__(parent)
        self.player = player
        self.closeApp = False

    def communicate(self):
        if self.player.isReceiving:
            data = None
            while True:
                try:
                    if self.player.isServer:
                        data = self.player.clientSocket.recv(1024)
                    else:
                        data = self.player.socket.recv(1024)
                except Exception:
                    pass
                if data or self.closeApp:
                    break
            if data is not None:
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
