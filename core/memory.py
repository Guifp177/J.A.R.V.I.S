import json
from pathlib import Path


class Memory:
    def __init__(self, file_path="core/memory_store.json", max_items=40):
        self.file_path = Path(file_path)
        self.max_items = max_items
        self.history = []
        self._load()

    def _load(self):
        if self.file_path.exists():
            try:
                self.history = json.loads(self.file_path.read_text(encoding="utf-8"))
            except:
                self.history = []
        else:
            self.history = []

    def _save(self):
        try:
            self.file_path.write_text(
                json.dumps(self.history, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except:
            pass

    def add(self, role, content):
        self.history.append({"role": role, "content": content})
        self.history = self.history[-self.max_items:]
        self._save()

    def get_context(self):
        return self.history.copy()

    def clear(self):
        self.history = []
        self._save()
