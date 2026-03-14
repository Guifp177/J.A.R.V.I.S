import math
import time

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPen, QRadialGradient
from PySide6.QtWidgets import QWidget


class ArcMeter(QWidget):
    """
    Núcleo JARVIS estilo MCU:
    - múltiplos anéis
    - rotação em camadas
    - pulso de energia
    - ticks radiais
    - glow neon azul
    """

    def __init__(self, size=260, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)

        self.angle_fast = 0
        self.angle_slow = 0
        self.pulse_phase = 0.0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)  # ~60 FPS

    def animate(self):
        self.angle_fast = (self.angle_fast + 1.8) % 360
        self.angle_slow = (self.angle_slow + 0.4) % 360
        self.pulse_phase += 0.04
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx = self.width() // 2
        cy = self.height() // 2

        t = time.time()
        pulse = (math.sin(self.pulse_phase) + 1) / 2  # 0..1

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(5, 10, 20))
        painter.drawEllipse(0, 0, self.width(), self.height())

        # =========================
        # GLOW CENTRAL
        # =========================
        glow = QRadialGradient(cx, cy, cx)
        glow.setColorAt(0.0, QColor(0, 255, 255, int(120 + 80 * pulse)))
        glow.setColorAt(0.4, QColor(0, 180, 255, 60))
        glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(glow)
        painter.drawEllipse(cx - cx, cy - cy, cx * 2, cy * 2)

        r_outer = cx - 8

        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self.angle_slow)  # gira DEVAGAR
        painter.translate(-cx, -cy)

        pen = QPen()
        pen.setWidth(4)
        pen.setCapStyle(Qt.RoundCap)

        for i in range(12):
            alpha = 40 + i * 10
            pen.setColor(QColor(0, 220, 255, alpha))
            painter.setPen(pen)

            painter.drawArc(
                cx - r_outer,
                cy - r_outer,
                r_outer * 2,
                r_outer * 2,
                int((20 + i * 2) * 16),  # início deslocado
                int(220 * 16),  # NÃO fecha o círculo
            )

        painter.restore()

        tick_pen = QPen(QColor(0, 255, 255, 200))
        tick_pen.setWidth(2)
        painter.setPen(tick_pen)

        for i in range(0, 360, 6):
            rad = math.radians(i)
            inner = cx - 30
            outer = cx - 16

            x1 = cx + inner * math.cos(rad)
            y1 = cy + inner * math.sin(rad)
            x2 = cx + outer * math.cos(rad)
            y2 = cy + outer * math.sin(rad)

            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        pen_mid = QPen(QColor(0, 180, 255, 140))
        pen_mid.setWidth(4)
        painter.setPen(pen_mid)

        r_mid = cx - 45
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(-self.angle_slow)
        painter.translate(-cx, -cy)

        for i in range(0, 360, 20):
            painter.drawArc(
                cx - r_mid, cy - r_mid, r_mid * 2, r_mid * 2, i * 16, 10 * 16
            )
        painter.restore()

        pulse_radius = cx - 75 - int(6 * pulse)
        pen_inner = QPen(QColor(0, 255, 255, int(160 + 80 * pulse)))
        pen_inner.setWidth(5)
        painter.setPen(pen_inner)
        painter.drawEllipse(
            cx - pulse_radius, cy - pulse_radius, pulse_radius * 2, pulse_radius * 2
        )

        core_r = cx - 110
        core_grad = QRadialGradient(cx, cy, core_r)
        core_grad.setColorAt(0.0, QColor(255, 255, 255, 220))
        core_grad.setColorAt(0.3, QColor(0, 255, 255, 220))
        core_grad.setColorAt(1.0, QColor(0, 120, 180, 200))
        painter.setBrush(core_grad)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(cx - core_r, cy - core_r, core_r * 2, core_r * 2)
