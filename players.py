from shapes import Shape


class Player:
    def __init__(self, role):
        if role == "server":
            self.isServer = True
            self.isClient = False
            self.shape = Shape.CIRCLE
            self.strSymbol = "circle"
        elif role == "client":
            self.isServer = False
            self.isCleint = True
            self.shape = Shape.CROSS
            self.strSymbol = "cross"
        else:
            raise NotImplementedError
        self.strStatus = role

    def __str__(self):
        return f"Status: {self.strStatus}, symbol: {self.strSymbol}"
