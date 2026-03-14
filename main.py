import os
import sys
from tkinter.constants import S

from PySide6.QtWidgets import QApplication, QDialog
from ui.main_window import MainWindow
from ui.setup_dialog import SetupDialog

from core.config.config_manager import ConfigManager


def load_theme(app):
    try:
        if os.path.exists("ui/theme.qss"):
            with open("ui/theme.qss", "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
        else:
            print("[AVISO] Arquivo ui/theme.qss não encontrado.")
    except Exception as e:
        print(f"[ERRO] Falha ao carregar tema: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_theme(app)
    cfg = ConfigManager()

    if not cfg.has_gemini():
        print("[SISTEMA] Credenciais não encontradas. Iniciando Setup Wizard...")
        setup = SetupDialog()
        if setup.exec() == QDialog.Rejected:
            print("[SISTEMA] Protocolo de inicialização cancelado pelo usuário.")
            sys.exit()

    use_voice = "--voice" in sys.argv

    if use_voice:
        print("\n" + "!" * 40)
        print("[SISTEMA] JARVIS PROTOCOLO INTEGRAL (VOZ) ATIVADO")
        print("!" * 40 + "\n")
    else:
        print("\n" + "=" * 40)
        print("[SISTEMA] JARVIS MODO FURTIVO (SILENCIOSO)")
        print("=" * 40 + "\n")

    window = MainWindow(use_voice=use_voice)
    window.show()

    sys.exit(app.exec())
