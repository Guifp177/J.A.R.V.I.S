from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLineEdit, QTextEdit, QVBoxLayout, QWidget


class ChatPanel(QWidget):
    message_sent = Signal(str)

    def __init__(self, parent=None, width=600, max_height=250):
        super().__init__(parent)
        self.setFixedWidth(width)

        self.setStyleSheet("""
            background-color: rgba(5, 15, 25, 180);
            border: 1px solid rgba(0, 255, 255, 50);
            border-radius: 12px;
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Segoe UI", 11))
        self.chat_display.setStyleSheet("""
            background-color: transparent;
            color: rgba(0, 255, 255, 230);
            border: none;
        """)

        self.chat_display.setMaximumHeight(max_height)
        self.chat_display.setMinimumHeight(100)
        self.chat_display.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.chat_display.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.chat_input = QLineEdit(self)
        self.chat_input.setFont(QFont("Segoe UI", 11))
        self.chat_input.setPlaceholderText("Comando de voz ou texto...")
        self.chat_input.setStyleSheet("""
            background-color: rgba(0, 40, 60, 120);
            color: white;
            border: 1px solid rgba(0, 255, 255, 80);
            border-radius: 6px;
            padding: 6px;
        """)
        self.chat_input.returnPressed.connect(self._on_enter)

        layout.addWidget(self.chat_display)
        layout.addWidget(self.chat_input)

    def _on_enter(self):
        text = self.chat_input.text().strip()
        if not text:
            return

        self.message_sent.emit(text)
        self.chat_input.clear()

    def append_message(self, author, text):
        """
        Adiciona a mensagem ao histórico com formatação HTML.
        """
        if author == "You":
            color = "#00ffff"
            prefix = "YOU"
        else:
            color = "#8fd3ff"
            prefix = "JARVIS"

        html_text = (
            f"<span style='color: {color}; font-weight: bold;'>[{prefix}]:</span> "
            f"<span style='color: #d1f3ff;'>{text}</span>"
        )

        self.chat_display.append(html_text)

        QTimer.singleShot(
            10,
            lambda: self.chat_display.verticalScrollBar().setValue(
                self.chat_display.verticalScrollBar().maximum()
            ),
        )
