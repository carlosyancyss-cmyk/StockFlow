from datetime import datetime

from database.api import (
    select,
    select_where,
    insert,
    rpc,
)

def gerar_codigo_entrada():

    return rpc("gerar_codigo_entrada")

def salvar_entrada(
    codigo,
    tipo,
    fornecedor,
    origem,
    numero_nf,
    valor_total,
    usuario
):

    return insert(
        "entradas",
        {
            "codigo": codigo,
            "tipo": tipo,
            "fornecedor": fornecedor,
            "origem": origem,
            "numero_nf": numero_nf,
            "valor_total": valor_total,
            "usuario": usuario
        }
    )[0]["id"]

def salvar_item_entrada(
    entrada_id,
    produto_id,
    quantidade,
    lote,
    validade,
    valor_unitario
):


    insert(
        "itens_entrada",
        {
            "entrada_id": entrada_id,
            "produto_id": produto_id,
            "quantidade": quantidade,
            "lote": lote,
            "validade": validade,
            "valor_unitario": (
                float(valor_unitario)
                if valor_unitario not in ("", None)
                else 0
            )
        }
    )

def consultar_entrada(codigo):

    dados = select_where(
        "entradas",
        "*",
        {
            "codigo": codigo
        }
    )

    if dados:
        return dados[0]

    return None

def consultar_itens_entrada(codigo):

    return rpc(
        "consultar_itens_entrada",
        {
            "p_codigo": codigo
        }
    )

def salvar_lote(
    produto_id,
    lote,
    validade,
    quantidade
):

    insert(
        "lotes",
        {
            "produto_id": produto_id,
            "lote": lote,
            "validade": validade,
            "quantidade": quantidade
        }
    )