import socket
from shapes import Shape


class Player:
    def __init__(self):
        self.reset()

    def reset(self):
        self.isServer = False
        self.isClient = False
        self.shape = Shape.NONE
        self.opponentShape = Shape.NONE
        self.strSymbol = ""
        self.clientSocket = None
        self.socket = None
        self.strStatus = ""
        self._isReceiving = False
        self._isSending = False
        self.msgCell = ""
        self.isWinner = False

    @property
    def isReceiving(self):
        return self._isReceiving

    @isReceiving.setter
    def isReceiving(self, value):
        self._isReceiving = value
        self._isSending = not value

    @property
    def isSending(self):
        return self._isSending

    @isSending.setter
    def isSending(self, value):
        self._isSending = value
        self._isReceiving = not value

    def setRole(self, role):
        if role == "server":
            self.isServer = True
            self.isClient = False
            self.shape = Shape.CIRCLE
            self.opponentShape = Shape.CROSS
            self.strSymbol = "circle"
            self.clientSocket = None
        elif role == "client":
            self.isServer = False
            self.isClient = True
            self.shape = Shape.CROSS
            self.opponentShape = Shape.CIRCLE
            self.strSymbol = "cross"
        else:
            raise NotImplementedError
        self.strStatus = role
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __str__(self):
        return f"Status: {self.strStatus}, symbol: {self.strSymbol}"
