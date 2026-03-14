import os
import subprocess

# ✅ coloque aqui o caminho de seus apps
APP_PATHS = {
    "Chrome": r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "Edge": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Edge.lnk",
    "Minecraft": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\TLauncher\TLauncher.lnk",
    "Calculadora": r"C:\Windows\System32\calc.exe",
    "Explorer": r"C:\Windows\explorer.exe",
    "Cursor": r"C:\Users\guifp\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Cursor\Cursor.lnk",
    "Hydra": r"C:\Users\guifp\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Hydra.lnk",
}


def open_app(name: str):
    name = name.lower().strip()

    if name in APP_PATHS:
        path = APP_PATHS[name]

        if os.path.exists(path):
            subprocess.Popen(path)
            return {"ok": True}
        else:
            return {"ok": False, "msg": "path não existe"}

    try:
        subprocess.Popen(name)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "msg": str(e)}
