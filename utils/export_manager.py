from datetime import datetime
from pathlib import Path
import tempfile

def novo_pdf(nome):
    agora = datetime.now().strftime("%Y%m%d_%H%M%S")
    return Path(tempfile.gettempdir()) / f"{nome}_{agora}.pdf"

def novo_excel(nome):
    agora = datetime.now().strftime("%Y%m%d_%H%M%S")
    return Path(tempfile.gettempdir()) / f"{nome}_{agora}.xlsx"

def url_download(arquivo):
    return f"/download/{Path(arquivo).name}"

async def abrir_pdf(page, arquivo):
    await page.launch_url(url_download(arquivo))

async def abrir_excel(page, arquivo):
    await page.launch_url(url_download(arquivo))