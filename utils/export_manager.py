from datetime import datetime
from pathlib import Path
import tempfile
import os


def novo_pdf(nome):

    agora = datetime.now().strftime("%Y%m%d_%H%M%S")

    pasta_temp = Path(tempfile.gettempdir())

    return pasta_temp / f"{nome}_{agora}.pdf"


def novo_excel(nome):

    agora = datetime.now().strftime("%Y%m%d_%H%M%S")

    pasta_temp = Path(tempfile.gettempdir())

    return pasta_temp / f"{nome}_{agora}.xlsx"


def abrir_arquivo(page, arquivo):
    pass