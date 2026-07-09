from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import tempfile
import threading


class DownloadHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            directory=tempfile.gettempdir(),
            **kwargs
        )


_servidor = None


def iniciar_servidor():
    global _servidor

    if _servidor:
        return

    _servidor = ThreadingHTTPServer(
        ("127.0.0.1", 8001),
        DownloadHandler
    )

    threading.Thread(
        target=_servidor.serve_forever,
        daemon=True
    ).start()


def url_download(arquivo):
    return f"http://127.0.0.1:8001/{Path(arquivo).name}"