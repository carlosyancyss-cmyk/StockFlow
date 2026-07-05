from datetime import datetime

from database.supabase_db import supabase


def gerar_codigo_saida():

    resposta = (
        supabase
        .table("saidas")
        .select("id", count="exact")
        .execute()
    )

    total = resposta.count + 1

    data = datetime.now().strftime("%Y%m%d")

    return f"S{total:05d}"


def salvar_saida(
    codigo,
    tipo,
    setor,
    motivo,
    usuario
):

    resposta = (
        supabase
        .table("saidas")
        .insert({
            "codigo": codigo,
            "tipo": tipo,
            "setor": setor,
            "motivo": motivo,
            "usuario": usuario
        })
        .execute()
    )

    return resposta.data[0]["id"]


def salvar_item_saida(
    saida_id,
    produto_id,
    quantidade,
    lote
):

    (
        supabase
        .table("itens_saida")
        .insert({
            "saida_id": saida_id,
            "produto_id": produto_id,
            "quantidade": quantidade,
            "lote": lote
        })
        .execute()
    )

def consultar_saida(codigo):

    resposta = (
        supabase
        .table("saidas")
        .select("*")
        .eq("codigo", codigo)
        .execute()
    )

    if resposta.data:
        return resposta.data[0]

    return None    

def consultar_itens_saida(codigo):

    saida = consultar_saida(codigo)

    if not saida:
        return []

    resposta = (
        supabase
        .table("itens_saida")
        .select("""
            quantidade,
            lote,
            produtos(nome)
        """)
        .eq("saida_id", saida["id"])
        .execute()
    )

    itens = []

    for item in resposta.data:

        itens.append({
            "nome": item["produtos"]["nome"],
            "quantidade": item["quantidade"],
            "lote": item["lote"]
        })

    return itens

def listar_lotes_produto(nome_produto):

    resposta = (
        supabase
        .table("lotes")
        .select("""
            id,
            lote,
            validade,
            quantidade,
            produtos!inner(nome)
        """)
        .eq("produtos.nome", nome_produto)
        .gt("quantidade", 0)
        .order("validade")
        .execute()
    )

    agrupados = {}

    for item in resposta.data:

        chave = (
            item["lote"],
            item["validade"]
        )

        if chave not in agrupados:

            agrupados[chave] = {
                "lote_ids": [],
                "lote": item["lote"],
                "validade": item["validade"],
                "quantidade": 0
            }

        agrupados[chave]["lote_ids"].append(
            {
                "id": item["id"],
                "quantidade": item["quantidade"]
            }
        )

        agrupados[chave]["quantidade"] += item["quantidade"]

    return list(agrupados.values())

from datetime import date


from datetime import datetime


def listar_lotes_vencidos(nome_produto):

    resposta = (
        supabase
        .table("lotes")
        .select("""
            id,
            lote,
            validade,
            quantidade,
            produtos!inner(nome)
        """)
        .eq("produtos.nome", nome_produto)
        .gt("quantidade", 0)
        .execute()
    )

    hoje = datetime.today().date()

    lotes = []

    for item in resposta.data:

        try:

            validade = datetime.strptime(
                item["validade"],
                "%d/%m/%Y"
            ).date()

            if validade < hoje:

                lotes.append({

                    "lote_id": item["id"],
                    "lote": item["lote"],
                    "validade": item["validade"],
                    "quantidade": item["quantidade"]

                })

        except:
            pass

    lotes.sort(
        key=lambda x: datetime.strptime(
            x["validade"],
            "%d/%m/%Y"
        )
    )

    return lotes

def listar_produtos_com_lotes_vencidos():

    resposta = (
        supabase
        .table("lotes")
        .select("""
            validade,
            quantidade,
            produtos!inner(nome)
        """)
        .gt("quantidade", 0)
        .execute()
    )

    hoje = datetime.today().date()

    produtos = []
    nomes = set()

    for item in resposta.data:

        try:

            validade = datetime.strptime(
                item["validade"],
                "%d/%m/%Y"
            ).date()

            if validade >= hoje:
                continue

            nome = item["produtos"]["nome"]

            if nome not in nomes:

                nomes.add(nome)

                produtos.append({
                    "nome": nome
                })

        except:
            pass

    produtos.sort(
        key=lambda x: x["nome"]
    )

    return produtos

def baixar_estoque(produto_id, quantidade):

    print("===================================")
    print("PRODUTO_ID:", produto_id)
    print("QUANTIDADE:", quantidade)

    resposta = (
        supabase
        .table("produtos")
        .select("id, estoque")
        .eq("id", produto_id)
        .execute()
    )

    print("RESPOSTA:", resposta.data)

    if not resposta.data:
        print("PRODUTO NÃO ENCONTRADO")
        return

    estoque_atual = resposta.data[0]["estoque"] or 0

    print("ESTOQUE ATUAL:", estoque_atual)

    novo_estoque = estoque_atual - quantidade

    print("NOVO ESTOQUE:", novo_estoque)

    resposta_update = (
        supabase
        .table("produtos")
        .update({
            "estoque": novo_estoque
        })
        .eq("id", produto_id)
        .execute()
    )

    print("UPDATE:", resposta_update.data)
    print("===================================")

def baixar_estoque_lote(lote_id, quantidade):

    resposta = (
        supabase
        .table("lotes")
        .select("quantidade")
        .eq("id", lote_id)
        .execute()
    )

    quantidade_atual = resposta.data[0]["quantidade"] or 0

    nova_quantidade = quantidade_atual - quantidade

    if nova_quantidade <= 0:

        (
            supabase
            .table("lotes")
            .delete()
            .eq("id", lote_id)
            .execute()
        )

    else:

        (
            supabase
            .table("lotes")
            .update({
                "quantidade": nova_quantidade
            })
            .eq("id", lote_id)
            .execute()
        ) 

def baixar_estoque_lotes_agrupados(lote_ids, quantidade):

    restante = quantidade

    for lote in lote_ids:

        if restante <= 0:
            break

        lote_id = lote["id"]
        disponivel = lote["quantidade"]

        if disponivel <= restante:

            (
                supabase
                .table("lotes")
                .delete()
                .eq("id", lote_id)
                .execute()
            )

            restante -= disponivel

        else:

            (
                supabase
                .table("lotes")
                .update({
                    "quantidade": disponivel - restante
                })
                .eq("id", lote_id)
                .execute()
            )

            restante = 0     