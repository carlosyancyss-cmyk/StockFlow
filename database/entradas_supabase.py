from database.supabase_db import supabase
from datetime import datetime

def gerar_codigo_entrada():

    resposta = (
        supabase
        .table("entradas")
        .select("id", count="exact")
        .execute()
    )

    total = resposta.count + 1

    data = datetime.now().strftime("%Y%m%d")

    return f"E{total:05d}"

def salvar_entrada(
    codigo,
    tipo,
    fornecedor,
    origem,
    numero_nf,
    valor_total,
    usuario
):

    resposta = (
        supabase
        .table("entradas")
        .insert({
            "codigo": codigo,
            "tipo": tipo,
            "fornecedor": fornecedor,
            "origem": origem,
            "numero_nf": numero_nf,
            "valor_total": valor_total,
            "usuario": usuario
        })
        .execute()
    )

    return resposta.data[0]["id"]


def salvar_item_entrada(
    entrada_id,
    produto_id,
    quantidade,
    lote,
    validade,
    valor_unitario
):
    
    print("ENTRADA_ID:", entrada_id)
    print("PRODUTO_ID:", produto_id)
    print("QUANTIDADE:", quantidade)
    print("LOTE:", lote)
    print("VALIDADE:", validade)
    print("VALOR_UNITARIO:", valor_unitario)

    (
        supabase
        .table("itens_entrada")
        .insert({
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
        })
        .execute()
    )


def consultar_entrada(codigo):

    resposta = (
        supabase
        .table("entradas")
        .select("*")
        .eq("codigo", codigo)
        .execute()
    )

    if resposta.data:
        return resposta.data[0]

    return None


def consultar_itens_entrada(codigo):

    entrada = consultar_entrada(codigo)

    if not entrada:
        return []

    resposta = (
        supabase
        .table("itens_entrada")
        .select("""
            quantidade,
            lote,
            validade,
            valor_unitario,
            produtos(nome)
        """)
        .eq("entrada_id", entrada["id"])
        .execute()
    )

    resultado = []

    for item in resposta.data:

        resultado.append({
            "nome": item["produtos"]["nome"],
            "quantidade": item["quantidade"],
            "lote": item["lote"],
            "validade": item["validade"],
            "valor_unitario": item["valor_unitario"]
        })

    return resultado

def salvar_lote(
    produto_id,
    lote,
    validade,
    quantidade
):

    (
        supabase
        .table("lotes")
        .insert({
            "produto_id": produto_id,
            "lote": lote,
            "validade": validade,
            "quantidade": quantidade
        })
        .execute()
    )