import socket
from shapes import Shape


class Player:
    def __init__(self):
        self.isServer = False
        self.isClient = False
        self.shape = Shape.NONE
        self.opponentShape = Shape.NONE
        self.strSymbol = ""
        self.clientSocket = None
        self.socket = None
        self.strStatus = ""
        self.__isReceiving = False
        self.__isSending = False
        self.msgCell = ""

    def reset(self):
        self.isServer = False
        self.isClient = False
        self.shape = Shape.NONE
        self.opponentShape = Shape.NONE
        self.strSymbol = ""
        self.clientSocket = None
        self.socket = None
        self.strStatus = ""
        self.__isReceiving = False
        self.__isSending = False
        self.msgCell = ""

    @property
    def isReceiving(self):
        return self.__isReceiving

    @isReceiving.setter
    def isReceiving(self, value):
        self.__isReceiving = value
        self.__isSending = not value

    @property
    def isSending(self):
        return self.__isSending

    @isSending.setter
    def isSending(self, value):
        self.__isSending = value
        self.__isReceiving = not value

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
