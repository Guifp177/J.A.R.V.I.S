from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
from pathlib import Path


class SoundFX:
    def __init__(self):
        self.audio = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio)
        self.audio.setVolume(0.6)

        self.start_url = self._url("assets/sounds/jarvis-start.mp3")
        self.search_url = self._url("assets/sounds/jarvis-search.m4a")

    def _url(self, path):
        return QUrl.fromLocalFile(str(Path(path).resolve()))

    def play_start(self):
        self.player.setSource(self.start_url)
        self.player.play()

    def play_search(self):
        self.player.setSource(self.search_url)
        self.player.play()
