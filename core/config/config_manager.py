import os
import subprocess


class ConfigManager:
    def __init__(self):
        self.GEMINI_VAR = "GEMINI_API_KEY"
        self.OLLAMA_VAR = "OLLAMA_API_KEY"

    def get_gemini_key(self):

        return os.environ.get(self.GEMINI_VAR)

    def get_ollama_key(self):

        return os.environ.get(self.OLLAMA_VAR)

    def save_key_to_windows(self, var_name, value):

        try:
            subprocess.run(f'setx {var_name} "{value}"', check=True, shell=True)
            os.environ[var_name] = value
            return True
        except Exception as e:
            print(f"[ERRO CONFIG] Falha ao gravar {var_name} no Path: {e}")
            return False

    def has_gemini(self):

        key = self.get_gemini_key()
        return key is not None and len(key) > 10

    def has_ollama(self):

        return self.get_ollama_key() is not None
