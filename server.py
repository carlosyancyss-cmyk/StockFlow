from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
import tempfile

app = FastAPI()

TEMP_DIR = Path(tempfile.gettempdir())


@app.get("/download/{arquivo}")
def download(arquivo: str):

    caminho = TEMP_DIR / arquivo

    if not caminho.exists():
        return {"erro": "Arquivo não encontrado"}

    return FileResponse(
        path=caminho,
        filename=arquivo
    )