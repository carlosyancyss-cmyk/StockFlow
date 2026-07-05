from database.supabase_db import supabase


def listar_estoque():

    resposta = (
        supabase
        .table("lotes")
        .select("""
            id,
            quantidade,
            lote,
            validade,
            produtos(
                id,
                nome,
                unidade_medida,
                estoque_minimo
            )
        """)
        .execute()
    )

    dados = []

    agrupados = {}

    for item in resposta.data:

        produto = item["produtos"]

        chave = (
            produto["id"],
            item["lote"],
            item["validade"]
        )

        if chave not in agrupados:

            agrupados[chave] = {
                "produto_id": produto["id"],
                "lote_id": item["id"],      # mantém o primeiro ID
                "lote_ids": [item["id"]],   # guarda todos os IDs
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

    (
        supabase
        .table("produtos")
        .update({
            "nome": nome,
            "unidade_medida": unidade
        })
        .eq("id", produto_id)
        .execute()
    )

    quantidade_por_lote = quantidade // len(lote_ids)
    resto = quantidade % len(lote_ids)

    for i, lote_id in enumerate(lote_ids):

        qtd = quantidade_por_lote

        if i == 0:
            qtd += resto

        (
            supabase
            .table("lotes")
            .update({
                "quantidade": qtd,
                "lote": lote,
                "validade": validade
            })
            .eq("id", lote_id)
            .execute()
        )

def excluir_lote(lote_ids):

    if not isinstance(lote_ids, list):
        lote_ids = [lote_ids]

    for lote_id in lote_ids:

        (
            supabase
            .table("lotes")
            .delete()
            .eq("id", lote_id)
            .execute()
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

    (
        supabase
        .table("ajustes_estoque")
        .insert({
            "produto_id": produto_id,
            "lote_id": lote_id,
            "produto": produto,
            "usuario": usuario,
            "acao": acao,
            "antes": antes,
            "depois": depois
        })
        .execute()
    )       