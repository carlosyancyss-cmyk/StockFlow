from database.supabase_db import supabase
from datetime import datetime, timedelta


def total_produtos():

    resposta = (
        supabase
        .table("produtos")
        .select("id", count="exact")
        .execute()
    )

    return resposta.count


def estoque_total():

    resposta = (
        supabase
        .table("lotes")
        .select("quantidade")
        .execute()
    )

    return sum(item["quantidade"] or 0 for item in resposta.data)


def total_entradas():

    resposta = (
        supabase
        .table("entradas")
        .select("id", count="exact")
        .execute()
    )

    return resposta.count


def total_saidas():

    resposta = (
        supabase
        .table("saidas")
        .select("id", count="exact")
        .execute()
    )

    return resposta.count

def produtos_estoque_baixo():

    resposta = (
        supabase
        .table("produtos")
        .select("""
            nome,
            estoque_minimo,
            lotes(quantidade)
        """)
        .execute()
    )

    resultado = []

    for produto in resposta.data:

        estoque = sum(
            (lote["quantidade"] or 0)
            for lote in (produto.get("lotes") or [])
        )

        if estoque <= (produto["estoque_minimo"] or 0):

            resultado.append({
                "nome": produto["nome"],
                "estoque": estoque,
                "estoque_minimo": produto["estoque_minimo"]
            })

    resultado.sort(key=lambda x: x["nome"])

    return resultado

def proximos_vencimentos():

    resposta = (
        supabase
        .table("lotes")
        .select("""
            validade,
            produtos(nome)
        """)
        .execute()
    )

    hoje = datetime.now().date()
    limite = hoje + timedelta(days=30)

    resultado = []

    for item in resposta.data:

        validade = item.get("validade")

        if not validade:
            continue

        try:
            data_validade = datetime.strptime(
                validade,
                "%d/%m/%Y"
            ).date()
        except Exception:
            continue

        if hoje <= data_validade <= limite:

            resultado.append({
                "nome": item["produtos"]["nome"],
                "validade": validade,
                "_data": data_validade
            })

    resultado.sort(key=lambda x: x["_data"])

    return [
        {
            "nome": item["nome"],
            "validade": item["validade"]
        }
        for item in resultado[:5]
    ]

def listar_movimentacoes():

    entradas = (
        supabase
        .table("entradas")
        .select("id,codigo,tipo,usuario,data")
        .execute()
    ).data

    saidas = (
        supabase
        .table("saidas")
        .select("id,codigo,tipo,usuario,data")
        .execute()
    ).data

    resultado = []

    for item in entradas:
        item["movimento"] = "ENTRADA"
        resultado.append(item)

    for item in saidas:
        item["movimento"] = "SAIDA"
        resultado.append(item)

    resultado.sort(
        key=lambda x: x["data"],
        reverse=True
    )

    return resultado

def buscar_itens_historico_entrada(entrada_id):

    resposta = (
        supabase
        .table("itens_entrada")
        .select("""
            quantidade,
            lote,
            validade,
            produtos(nome)
        """)
        .eq("entrada_id", entrada_id)
        .execute()
    )

    itens = []

    for item in resposta.data:

        itens.append({
            "nome": item["produtos"]["nome"],
            "quantidade": item["quantidade"],
            "lote": item["lote"],
            "validade": item["validade"]
        })

    return itens

def buscar_itens_historico_saida(saida_id):

    resposta = (
        supabase
        .table("itens_saida")
        .select("""
            quantidade,
            lote,
            produtos(nome)
        """)
        .eq("saida_id", saida_id)
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

def ultimas_movimentacoes():

    movimentacoes = []

    # ENTRADAS
    resposta = (
        supabase
        .table("entradas")
        .select("""
            codigo,
            tipo,
            usuario,
            data
        """)
        .execute()
    )

    for item in resposta.data:

        movimentacoes.append({

            "codigo": item["codigo"],
            "tipo": item["tipo"],
            "usuario": item["usuario"],
            "data": item["data"],
            "movimento": "ENTRADA"

        })

    # SAÍDAS
    resposta = (
        supabase
        .table("saidas")
        .select("""
            codigo,
            tipo,
            usuario,
            data
        """)
        .execute()
    )

    for item in resposta.data:

        movimentacoes.append({

            "codigo": item["codigo"],
            "tipo": item["tipo"],
            "usuario": item["usuario"],
            "data": item["data"],
            "movimento": "SAIDA"

        })

    movimentacoes.sort(
        key=lambda x: x["data"],
        reverse=True
    )

    return movimentacoes[:5]