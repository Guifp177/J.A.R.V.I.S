from datetime import datetime

import pytz
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QWidget


class ClockWidget(QWidget):
    def __init__(self, parent=None, width=150, height=50):
        super().__init__(parent)
        self.setFixedSize(width, height)

        self.time_label = QLabel(self)
        self.time_label.setAlignment(Qt.AlignCenter)

        self.time_label.setFont(QFont("Consolas", 30, QFont.Bold))
        self.time_label.setStyleSheet(
            "color: rgba(0,255,255,220); background-color: transparent;"
        )

        self.time_label.setGeometry(0, 0, width, height)

        # Atualiza a cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self):
        manaus_tz = pytz.timezone("America/Manaus")
        now = datetime.now(manaus_tz)
        self.time_label.setText(now.strftime("%H:%M"))
