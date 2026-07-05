import json

from datetime import datetime, date
from app_paths import BACKUPS_DIR

from database.supabase_db import supabase




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

        resposta = (
            supabase
            .table(tabela)
            .select("*")
            .execute()
        )

        backup[tabela] = resposta.data

    nome = "Backup_StockFlow.json"

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

    enviar_backup_nuvem(caminho)

    atualizar_data_ultimo_backup()

    return caminho


def enviar_backup_nuvem(caminho_arquivo):

    storage = supabase.storage.from_("backups")

    with open(caminho_arquivo, "rb") as arquivo:

        try:

            storage.update(
                path="backup_atual.json",
                file=arquivo,
                file_options={
                    "content-type": "application/json"
                }
            )

        except Exception:

            arquivo.seek(0)

            storage.upload(
                path="backup_atual.json",
                file=arquivo,
                file_options={
                    "content-type": "application/json"
                }
            )

def obter_data_ultimo_backup():

    resposta = (
        supabase
        .table("configuracoes")
        .select("valor")
        .eq("chave", "ultimo_backup")
        .single()
        .execute()
    )

    return resposta.data["valor"]

def atualizar_data_ultimo_backup():

    (
        supabase
        .table("configuracoes")
        .update({
            "valor": str(date.today())
        })
        .eq("chave", "ultimo_backup")
        .execute()
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

    destino = BACKUPS_DIR / "backup_nuvem_temp.json"

    with open(destino, "wb") as arquivo:

        resposta = (
            supabase
            .storage
            .from_("backups")
            .download("backup_atual.json")
        )

        arquivo.write(resposta)

    return destino