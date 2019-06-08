from time import sleep
from shapes import Shape


class Board:
    WIN_COMBINATIONS = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    )

    def __init__(self, cells):
        self.cells = cells
        self.winningCombination = []

    def checkForWinner(self, shape):
        isWinner = False
        for line in self.WIN_COMBINATIONS:
            okShape = [self.cells[i].currentShape is shape for i in line]
            if all(okShape):
                isWinner = True
                self.winningCombination = [self.cells[i] for i in line]
                break
        return isWinner

    def boardIsFull(self):
        return all(cell.hasShape for cell in self.cells)

    def clean(self):
        sleep(0.5)
        for cell in self.cells:
            cell.drawShape(Shape.NONE)

    def blink(self, color):
        for cell in self.winningCombination:
            cell.setStyleSheet(f"background-color: {color};")
            cell.repaint()

    def showWinningCells(self):
        bgColors = "#ffffff", "#282828"
        count = 0
        while count < 6:
            self.blink(bgColors[count % 2])
            count += 1
            sleep(0.5)
        self.winningCombination = []
