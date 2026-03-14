import asyncio
import os
import time
from pathlib import Path

import edge_tts
from PySide6.QtCore import QObject, QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer


class JarvisTTS(QObject):
    def __init__(self):
        super().__init__()
        self.base_path = Path(__file__).parent.parent
        self.cache_dir = self.base_path / "voice" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)

        # Voz "Antonio" ou "Francisca" da Microsoft
        self.voice = "pt-BR-AntonioNeural"

    async def _generate(self, text, output_file):
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_file)

    def generate_and_speak(self, text, callback):
        """Versão ultra rápida usando Edge-TTS"""
        timestamp = int(time.time())
        output_file = self.cache_dir / f"speech_{timestamp}.wav"

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._generate(text, str(output_file)))
            loop.close()

            if output_file.exists():
                self.player.setSource(QUrl.fromLocalFile(str(output_file.absolute())))
                callback()
                self.player.play()
        except Exception as e:
            print(f"[EDGE-TTS ERROR] {e}")
            callback()
