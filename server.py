from contextlib import asynccontextmanager

import flet.fastapi as flet_fastapi
from fastapi.responses import FileResponse
from pathlib import Path
import tempfile

from main import main


@asynccontextmanager
async def lifespan(app):
    await flet_fastapi.app_manager.start()
    yield
    await flet_fastapi.app_manager.shutdown()


app = flet_fastapi.FastAPI(
    lifespan=lifespan
)

TEMP_DIR = Path(tempfile.gettempdir())


@app.get("/download/{arquivo}")
def download(arquivo: str):

    caminho = TEMP_DIR / arquivo

    return FileResponse(
        caminho,
        filename=arquivo
    )


app.mount(
    "/",
    flet_fastapi.app(
        main,
        assets_dir="assets"
    ),
)