from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QLineF
from PyQt5.QtGui import QPainter, QPen, QColor
from shapes import Shape


class ShapeLabel(QLabel):

    clicked = pyqtSignal()
    delta = 25

    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentShape = Shape.NONE
        self.pen = QPen()
        self.pen.setWidth(20)
        self.shouldPaint = False
        self.index = None

    @property
    def hasShape(self):
        return self.currentShape is not Shape.NONE

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        else:
            super().mousePressEvent(event)

    def _getDimensions(self):
        return self.size().width(), self.size().height()

    def drawCircle(self):
        painter = QPainter(self)
        self.pen.setColor(QColor.fromRgb(236, 47, 47))
        painter.setPen(self.pen)
        w, h = self._getDimensions()
        painter.drawEllipse(self.delta, self.delta,
                            w - 2 * self.delta, h - 2 * self.delta)

    def drawCross(self):
        w, h = self._getDimensions()
        painter = QPainter(self)
        self.pen.setColor(QColor.fromRgb(47, 101, 236))
        painter.setPen(self.pen)
        lines = [QLineF(self.delta, self.delta,
                        w - self.delta, h - self.delta),
                 QLineF(self.delta, h - self.delta,
                        w - self.delta, self.delta)]
        painter.drawLines(lines)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.currentShape is Shape.CIRCLE:
            self.drawCircle()
        elif self.currentShape is Shape.CROSS:
            self.drawCross()

    def drawShape(self, shape):
        self.currentShape = shape
        self.repaint()
