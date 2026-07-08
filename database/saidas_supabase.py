from datetime import datetime

from database.api import (
    select,
    select_where,
    insert,
    update,
    delete,
    rpc,
)


def gerar_codigo_saida():

    return rpc("gerar_codigo_saida")

def salvar_saida(
    codigo,
    tipo,
    setor,
    motivo,
    usuario
):

    return insert(
        "saidas",
        {
            "codigo": codigo,
            "tipo": tipo,
            "setor": setor,
            "motivo": motivo,
            "usuario": usuario
        }
    )[0]["id"]

def salvar_item_saida(
    saida_id,
    produto_id,
    quantidade,
    lote
):

    insert(
        "itens_saida",
        {
            "saida_id": saida_id,
            "produto_id": produto_id,
            "quantidade": quantidade,
            "lote": lote
        }
    )

def consultar_saida(codigo):

    dados = select_where(
        "saidas",
        "*",
        {
            "codigo": codigo
        }
    )

    if dados:
        return dados[0]

    return None

def consultar_itens_saida(codigo):

    return rpc(
        "consultar_itens_saida",
        {
            "p_codigo": codigo
        }
    )

def listar_lotes_produto(nome_produto):

    return rpc(
        "listar_lotes_produto",
        {
            "p_nome_produto": nome_produto
        }
    )

def listar_lotes_vencidos(nome_produto):

    return rpc(
        "listar_lotes_vencidos",
        {
            "p_nome_produto": nome_produto
        }
    )

def listar_produtos_com_lotes_vencidos():

    return rpc(
        "listar_produtos_com_lotes_vencidos"
    )

def baixar_estoque(produto_id, quantidade):

    rpc(
        "baixar_estoque",
        {
            "p_produto_id": produto_id,
            "p_quantidade": quantidade
        }
    )

def baixar_estoque_lote(lote_id, quantidade):

    rpc(
        "baixar_estoque_lote",
        {
            "p_lote_id": lote_id,
            "p_quantidade": quantidade
        }
    )

def baixar_estoque_lotes_agrupados(lote_ids, quantidade):

    rpc(
        "baixar_estoque_lotes_agrupados",
        {
            "p_lote_ids": lote_ids,
            "p_quantidade": quantidade
        }
    )