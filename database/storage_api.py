import httpx

from database.api import (
    SUPABASE_URL,
    SUPABASE_KEY
)

BUCKET = "backups"

STORAGE_URL = f"{SUPABASE_URL}/storage/v1/object/{BUCKET}"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}


def upload_backup(caminho_local, nome_arquivo):

    with open(caminho_local, "rb") as arquivo:

        resposta = httpx.post(
            f"{STORAGE_URL}/{nome_arquivo}",
            headers={
                **HEADERS,
                "Content-Type": "application/json",
                "x-upsert": "true"
            },
            content=arquivo.read(),
            timeout=60
        )

    return resposta.status_code in (200, 201)


def download_backup(nome_arquivo, destino):

    resposta = httpx.get(
        f"{STORAGE_URL}/{nome_arquivo}",
        headers=HEADERS,
        timeout=60
    )

    if resposta.status_code != 200:
        return False

    with open(destino, "wb") as arquivo:
        arquivo.write(resposta.content)

    return True


def excluir_backup(nome_arquivo):

    resposta = httpx.delete(
        f"{STORAGE_URL}/{nome_arquivo}",
        headers=HEADERS
    )

    return resposta.status_code in (200, 204)


def listar_backups():

    resposta = httpx.post(
        f"{SUPABASE_URL}/storage/v1/object/list/{BUCKET}",
        headers=HEADERS,
        json={
            "limit": 100
        }
    )

    if resposta.status_code != 200:
        return []

    return resposta.json()