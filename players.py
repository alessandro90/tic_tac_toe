import socket
from shapes import Shape


class Player:
    def setRole(self, role):
        if role == "server":
            self.isServer = True
            self.isClient = False
            self.shape = Shape.CIRCLE
            self.strSymbol = "circle"
            self.clientSocket = None
        elif role == "client":
            self.isServer = False
            self.isClient = True
            self.shape = Shape.CROSS
            self.strSymbol = "cross"
        else:
            raise NotImplementedError
        self.strStatus = role
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __str__(self):
        return f"Status: {self.strStatus}, symbol: {self.strSymbol}"
