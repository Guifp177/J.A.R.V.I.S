import psutil
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtWidgets import QWidget


class InfoPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(240, 160)

        self.cpu = 0
        self.memory = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(800)  # atualiza a cada 0.8s

    def update_stats(self):
        self.cpu = int(psutil.cpu_percent())
        self.memory = int(psutil.virtual_memory().percent)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QColor(0, 200, 255, 180))
        painter.setFont(QFont("Segoe UI", 9))

        painter.drawText(10, 20, "SYSTEM STATUS")
        painter.drawText(10, 45, f"CPU Usage  : {self.cpu}%")
        painter.drawText(10, 70, f"Memory     : {self.memory}%")

        # barra CPU
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 255, 255, 120))
        painter.drawRect(10, 80, int(2 * self.cpu), 6)

        # barra Memory
        painter.setBrush(QColor(0, 180, 255, 100))
        painter.drawRect(10, 100, int(2 * self.memory), 6)

        # detalhe inferior
        painter.setPen(QColor(0, 255, 255, 60))
        painter.drawLine(10, 125, 220, 125)
