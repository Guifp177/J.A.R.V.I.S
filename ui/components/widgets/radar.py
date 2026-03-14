import math

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPen, QRadialGradient
from PySide6.QtWidgets import QWidget


class Radar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(220, 220)

        self.angle = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    def animate(self):
        self.angle = (self.angle + 1.5) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx = self.width() // 2
        cy = self.height() // 2
        radius = cx - 10

        glow = QRadialGradient(cx, cy, radius)
        glow.setColorAt(0.0, QColor(0, 255, 255, 90))
        glow.setColorAt(0.6, QColor(0, 120, 200, 40))
        glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(glow)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())

        pen = QPen(QColor(0, 200, 255, 120))
        pen.setWidth(1)
        painter.setPen(pen)

        for r in range(40, radius, 40):
            painter.drawEllipse(cx - r, cy - r, r * 2, r * 2)

        painter.drawLine(cx, 10, cx, self.height() - 10)
        painter.drawLine(10, cy, self.width() - 10, cy)

        sweep_pen = QPen(QColor(0, 255, 255, 200))
        sweep_pen.setWidth(2)
        painter.setPen(sweep_pen)

        rad = math.radians(self.angle)
        x = cx + radius * math.cos(rad)
        y = cy + radius * math.sin(rad)

        painter.drawLine(cx, cy, int(x), int(y))
