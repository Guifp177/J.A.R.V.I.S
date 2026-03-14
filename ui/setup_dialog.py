from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from core.config.config_manager import ConfigManager


class SetupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigManager()
        self.setWindowTitle("J.A.R.V.I.S - PROTOCOLO DE ACESSO")
        self.setFixedSize(400, 250)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)

        self.setStyleSheet("""
            QDialog { background-color: #050b10; border: 2px solid #00fbff; }
            QLabel { color: #00fbff; font-family: 'Segoe UI'; font-size: 12px; }
            QLineEdit {
                background-color: #0a141e; color: white;
                border: 1px solid #0088ff; border-radius: 4px; padding: 5px;
            }
            QPushButton {
                background-color: #00fbff; color: black; font-weight: bold;
                border-radius: 4px; padding: 8px;
            }
            QPushButton:hover { background-color: #0088ff; color: white; }
        """)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("SISTEMA DE AUTENTICAÇÃO JARVIS"))
        layout.addWidget(QLabel("Cole sua GEMINI_API_KEY (Prioridade 1 - Nuvem):"))
        self.gemini_input = QLineEdit()
        self.gemini_input.setPlaceholderText("Chave do Google AI Studio...")
        layout.addWidget(self.gemini_input)

        layout.addWidget(QLabel("Cole sua OLLAMA_API_KEY (Prioridade 2 - Local):"))
        self.ollama_input = QLineEdit()
        self.ollama_input.setPlaceholderText(
            "Deixe em branco se usar o padrão local..."
        )
        layout.addWidget(self.ollama_input)

        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("AUTORIZAR")
        self.btn_save.clicked.connect(self.save_and_close)
        btn_layout.addWidget(self.btn_save)

        layout.addLayout(btn_layout)

    def save_and_close(self):
        g_key = self.gemini_input.text().strip()
        o_key = self.ollama_input.text().strip()

        if g_key:
            self.config.save_key_to_windows("GEMINI_API_KEY", g_key)
        if o_key:
            self.config.save_key_to_windows("OLLAMA_API_KEY", o_key)

        self.accept()
