
import flet.fastapi as flet_fastapi
from fastapi.responses import FileResponse
from pathlib import Path
import tempfile

from main import main

BASE_DIR = Path(__file__).resolve().parent

app = flet_fastapi.FastAPI()


TEMP_DIR = Path(tempfile.gettempdir())


@app.get("/download/{arquivo}")
async def download(arquivo: str):

    print("=" * 50)
    print("DOWNLOAD SOLICITADO")
    print("Arquivo recebido:", arquivo)

    print("TEMP_DIR:", TEMP_DIR)

    print("Arquivos existentes no TEMP_DIR:")
    for f in TEMP_DIR.iterdir():
        print(" -", f.name)

    caminho = TEMP_DIR / arquivo

    print("CAMINHO:", caminho)
    print("EXISTE?", caminho.exists())
    print("=" * 50)

    if not caminho.exists():
        return {"erro": "Arquivo não encontrado"}

    return FileResponse(
        path=caminho,
        filename=arquivo,
        media_type="application/octet-stream",
    )


app.mount(
    "/",
    flet_fastapi.app(
        main,
        assets_dir=str(BASE_DIR / "assets")
    ),
)