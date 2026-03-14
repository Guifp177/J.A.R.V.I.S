import threading

from PySide6.QtCore import QPoint, Qt, QTimer, Signal, Slot
from PySide6.QtGui import QFont, QMovie
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from voice.jarvis_voice import JarvisTTS

from core.bot.gemini_client import GeminiClient  # Prioridade 1 (Novo)
from core.bot.ollama_client import OllamaClient  # Prioridade 2
from core.config.config_manager import ConfigManager  # Gestor de Keys
from modules.mic_input import MicInput
from modules.sound import SoundFX
from ui.components.panels.info_panel import InfoPanel
from ui.components.panels.panels import SidePanel
from ui.components.widgets.arc_meter import ArcMeter
from ui.components.widgets.chat_panel import ChatPanel
from ui.components.widgets.radar import Radar


class MainWindow(QMainWindow):
    voice_command_signal = Signal(str)
    jarvis_reply_signal = Signal(str)

    def __init__(self, use_voice=False):
        super().__init__()

        # 1. Inicialização de Configuração e Motores de IA
        self.config = ConfigManager()
        self.gemini = GeminiClient()  # Tenta carregar P1
        self.ollama = OllamaClient()  # Tenta carregar P2

        self.use_voice = use_voice
        self.tts = JarvisTTS() if self.use_voice else None
        self.mic = MicInput()
        self.sfx = SoundFX()

        self.setWindowTitle("J.A.R.V.I.S")
        self.setFixedSize(1100, 700)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._drag_pos = QPoint()

        central = QWidget(self)
        self.setCentralWidget(central)
        self.background = QFrame(central)
        self.background.setGeometry(self.rect())
        self.background.setStyleSheet("background-color: #050b10;")

        self.voice_command_signal.connect(self.handle_user_message)
        self.jarvis_reply_signal.connect(self._post_jarvis_message)

        self._setup_ui_elements()

        self._setup_hud()

        self.sfx.play_start()

    def _setup_ui_elements(self):

        self.title = QLabel("J.A.R.V.I.S", self.background)
        self.title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.title.move(20, 12)

        self.subtitle = QLabel("...SYSTEM ONLINE", self.background)
        self.subtitle.setFont(QFont("Segoe UI", 9))
        self.subtitle.move(25, 55)

        self.btn_close = QPushButton("✕", self.background)
        self.btn_close.setFixedSize(34, 24)
        self.btn_close.move(self.width() - 44, 12)
        self.btn_close.clicked.connect(self.close)

        self.btn_mic = QPushButton("🎤", self.background)
        self.btn_mic.setFixedSize(34, 24)
        self.btn_mic.move(self.width() - 136, 12)
        self.btn_mic.clicked.connect(self.listen_mic)

    def _setup_hud(self):

        self.radar = Radar(parent=self.background)
        self.radar.move(50, 130)

        self.info_panel = InfoPanel(parent=self.background)
        self.info_panel.move(50, 390)

        self.core = ArcMeter(size=260, parent=self.background)
        self.core.move(self.width() // 2 - 130, self.height() // 2 - 195)

        arc_bottom = self.core.y() + self.core.height()
        self.chat_panel = ChatPanel(parent=self.background, width=420, max_height=250)
        self.chat_panel.move(self.width() // 2 - 210, arc_bottom + 10)
        self.chat_panel.message_sent.connect(self.handle_user_message)

    # ───────── LÓGICA DE INTELIGÊNCIA HÍBRIDA ─────────

    @Slot(str)
    def handle_user_message(self, text):
        if not text.strip():
            return

        self.sfx.play_search()
        self.chat_panel.append_message("You", text)
        self.chat_panel.append_message("Jarvis", "Processando diretrizes...")

        # Rodar IA em Thread separada para não travar o ArcMeter
        threading.Thread(
            target=self._process_ai_logic, args=(text,), daemon=True
        ).start()

    def _process_ai_logic(self, text):
        """Orquestrador de Fallback: Gemini (P1) -> Ollama (P2)"""
        reply = None

        # Tenta Prioridade 1: Gemini Cloud
        if self.config.has_gemini():
            print("[SISTEMA] Solicitando Gemini...")
            reply = self.gemini.chat(text)

        # Tenta Prioridade 2: Ollama Local (se Gemini falhar ou não houver key)
        if reply is None:
            print("[SISTEMA] Fallback: Acionando Ollama...")
            try:
                reply = self.ollama.chat(text)
            except Exception as e:
                reply = f"Senhor, os sistemas críticos falharam. Erro: {e}"

        if self.use_voice and self.tts:
            self.tts.generate_and_speak(
                reply, lambda: self.jarvis_reply_signal.emit(reply)
            )
        else:
            self.jarvis_reply_signal.emit(reply)

    @Slot(str)
    def _post_jarvis_message(self, text):
        self.chat_panel.append_message("Jarvis", text)

    def listen_mic(self):
        self.chat_panel.append_message("Jarvis", "Ouvindo, Senhor...")
        threading.Thread(target=self._mic_worker, daemon=True).start()

    def _mic_worker(self):
        text = self.mic.listen()
        if text:
            self.voice_command_signal.emit(text)
        else:
            QTimer.singleShot(
                0,
                lambda: self.chat_panel.append_message(
                    "Jarvis", "Nenhum comando detectado."
                ),
            )

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPosition().toPoint() - self._drag_pos
            self.move(self.pos() + delta)
            self._drag_pos = event.globalPosition().toPoint()
