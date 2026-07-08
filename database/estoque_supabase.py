from database.api import (
    get,
    update,
    remove,
    insert,
)


def listar_estoque():

    resposta = get(
        "lotes?select=id,quantidade,lote,validade,produtos(id,nome,unidade_medida,estoque_minimo)"
    )

    agrupados = {}

    for item in resposta:

        produto = item["produtos"]

        chave = (
            produto["id"],
            item["lote"],
            item["validade"]
        )

        if chave not in agrupados:

            agrupados[chave] = {
                "produto_id": produto["id"],
                "lote_id": item["id"],
                "lote_ids": [item["id"]],
                "nome": produto["nome"],
                "unidade_medida": produto["unidade_medida"],
                "estoque_minimo": produto["estoque_minimo"],
                "quantidade": item["quantidade"],
                "lote": item["lote"],
                "validade": item["validade"]
            }

        else:

            agrupados[chave]["quantidade"] += item["quantidade"]
            agrupados[chave]["lote_ids"].append(item["id"])

    dados = list(agrupados.values())

    dados.sort(key=lambda x: x["nome"])

    return dados


def atualizar_produto(
    produto_id,
    lote_ids,
    nome,
    unidade,
    quantidade,
    lote,
    validade
):

    update(
        "produtos",
        {
            "id": produto_id
        },
        {
            "nome": nome,
            "unidade_medida": unidade
        }
    )

    quantidade_por_lote = quantidade // len(lote_ids)
    resto = quantidade % len(lote_ids)

    for i, lote_id in enumerate(lote_ids):

        qtd = quantidade_por_lote

        if i == 0:
            qtd += resto

        update(
            "lotes",
            {
                "id": lote_id
            },
            {
                "quantidade": qtd,
                "lote": lote,
                "validade": validade
            }
        )


def excluir_lote(lote_ids):

    if not isinstance(lote_ids, list):
        lote_ids = [lote_ids]

    for lote_id in lote_ids:

        remove(
            f"lotes?id=eq.{lote_id}"
        )

def registrar_ajuste_estoque(
    produto_id,
    lote_id,
    produto,
    usuario,
    acao,
    antes,
    depois
):

    insert(
        "ajustes_estoque",
        {
            "produto_id": produto_id,
            "lote_id": lote_id,
            "produto": produto,
            "usuario": usuario,
            "acao": acao,
            "antes": antes,
            "depois": depois
        }
    )