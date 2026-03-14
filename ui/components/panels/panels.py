from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget


class SidePanel(QWidget):
    def __init__(self, width=280, height=600, parent=None, show_inner_lines=True):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.show_inner_lines = show_inner_lines

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        painter.setPen(QColor(0, 180, 255, 90))

        painter.drawLine(10, 10, w - 60, 10)
        painter.drawLine(10, 10, 10, h - 60)

        painter.drawLine(w - 10, 60, w - 10, h - 10)
        painter.drawLine(60, h - 10, w - 10, h - 10)

        painter.setPen(QColor(0, 255, 255, 50))
        painter.drawRect(30, 30, w - 60, h - 60)

        # linhas técnicas decorativas (OPCIONAL)
        if self.show_inner_lines:
            painter.setPen(QColor(0, 200, 255, 70))
            painter.drawLine(30, 80, w - 30, 80)
            painter.drawLine(30, 120, w - 80, 120)
