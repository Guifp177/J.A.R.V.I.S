import re
import subprocess
import urllib.parse
from pathlib import Path

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


def _get_chrome():
    for p in CHROME_PATHS:
        if Path(p).exists():
            return p
    return None


def pesquisar_no_chrome(texto: str):
    m = re.search(r'pesquise\s+"(.+?)"', texto, re.IGNORECASE)
    if m:
        query = m.group(1)
    else:
        query = texto.lower().replace("pesquise", "").strip()

    if not query:
        return False

    url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)

    chrome = _get_chrome()
    if not chrome:
        return False

    subprocess.Popen([chrome, url])
    return True
