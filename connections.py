from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

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