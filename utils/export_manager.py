from datetime import datetime
from pathlib import Path
import tempfile
import webbrowser


def novo_pdf(nome):
    agora = datetime.now().strftime("%Y%m%d_%H%M%S")
    return Path(tempfile.gettempdir()) / f"{nome}_{agora}.pdf"


def novo_excel(nome):
    agora = datetime.now().strftime("%Y%m%d_%H%M%S")
    return Path(tempfile.gettempdir()) / f"{nome}_{agora}.xlsx"


import os


def url_download(arquivo):

    base = os.getenv("APP_URL", "")

    return f"{base}/download/{Path(arquivo).name}"


def abrir_pdf(page, arquivo):
    webbrowser.open(url_download(arquivo))


def abrir_excel(page, arquivo):
    webbrowser.open(url_download(arquivo))