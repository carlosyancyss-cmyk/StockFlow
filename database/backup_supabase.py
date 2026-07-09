import json
import tempfile

from datetime import datetime, date
from app_paths import BACKUPS_DIR

from database.api import SUPABASE_URL, HEADERS
from database.storage_api import (
    upload_backup,
    download_backup
)

import httpx




TABELAS = [
    "usuarios",
    "produtos",
    "lotes",
    "fornecedores",
    "setores",
    "entradas",
    "itens_entrada",
    "saidas",
    "itens_saida",
    "ajustes_estoque"
]


def fazer_backup():

    backup = {}

    for tabela in TABELAS:

        resposta = httpx.get(
            f"{SUPABASE_URL}/rest/v1/{tabela}?select=*",
            headers=HEADERS,
            timeout=60
        )

        backup[tabela] = resposta.json()

    nome = "Backup_StockFlow.json"

    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)

    caminho = BACKUPS_DIR / nome

    if caminho.exists():
        caminho.unlink()

    with open(
        caminho,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            backup,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    upload_backup(
        caminho,
        "backup_atual.json"
    )

    atualizar_data_ultimo_backup()

    return caminho

def enviar_backup_nuvem(caminho_arquivo):

    return upload_backup(
        caminho_arquivo,
        "backup_atual.json"
    )

def obter_data_ultimo_backup():

    resposta = httpx.get(
        f"{SUPABASE_URL}/rest/v1/configuracoes"
        "?chave=eq.ultimo_backup&select=valor",
        headers=HEADERS
    )

    dados = resposta.json()

    if not dados:
        return ""

    return dados[0]["valor"]

def atualizar_data_ultimo_backup():

    httpx.patch(
        f"{SUPABASE_URL}/rest/v1/configuracoes"
        "?chave=eq.ultimo_backup",
        headers=HEADERS,
        json={
            "valor": str(date.today())
        }
    )
    
def fazer_backup_automatico():

    if obter_data_ultimo_backup() == str(date.today()):

        print("Backup automático já realizado hoje.")

        return False

    print("Executando backup automático...")

    caminho = fazer_backup()

    atualizar_data_ultimo_backup()

    print("Backup automático concluído.")

    return True

from pathlib import Path


def baixar_backup_nuvem():

    destino = Path(tempfile.gettempdir()) / "backup_nuvem_temp.json"

    ok = download_backup(
        "backup_atual.json",
        destino
    )

    if not ok:
        return None

    return destino