from database.supabase_db import supabase

def listar_fornecedores_relatorio():

    resposta = (
        supabase
        .table("fornecedores")
        .select("nome")
        .order("nome")
        .execute()
    )

    return [
        {"fornecedor": item["nome"]}
        for item in resposta.data
    ]

def listar_setores_relatorio():

    resposta = (
        supabase
        .table("setores")
        .select("nome")
        .order("nome")
        .execute()
    )

    return [
        {"setor": item["nome"]}
        for item in resposta.data
    ]

def listar_produtos_relatorio():

    resposta = (
        supabase
        .table("produtos")
        .select("nome")
        .order("nome")
        .execute()
    )

    return resposta.data

def listar_ajustes_estoque(data_inicio=None, data_fim=None, usuario=None):

    consulta = (
        supabase
        .table("ajustes_estoque")
        .select("*")
        .order("data", desc=True)
    )

    if data_inicio:
        consulta = consulta.gte("data", data_inicio)

    if data_fim:
        consulta = consulta.lte("data", data_fim + " 23:59:59")

    if usuario:
        consulta = consulta.ilike("usuario", f"%{usuario}%")

    resposta = consulta.execute()

    return resposta.data

def consultar_entradas_relatorio():

    resposta = (
        supabase
        .table("itens_entrada")
        .select("""
            quantidade,
            lote,
            validade,
            valor_unitario,
            entradas(
                codigo,
                tipo,
                fornecedor,
                origem,
                numero_nf,
                valor_total,
                usuario,
                data
            ),
            produtos(
                nome
            )
        """)
        .execute()
    )

    resultado = []

    for item in resposta.data:

        entrada = item["entradas"]
        produto = item["produtos"]

        resultado.append({

            "codigo": entrada["codigo"],
            "tipo": entrada["tipo"],
            "fornecedor": entrada["fornecedor"],
            "origem": entrada["origem"],
            "numero_nf": entrada["numero_nf"],
            "valor_total": entrada["valor_total"],
            "usuario": entrada["usuario"],
            "data": entrada["data"],

            "produto": produto["nome"],

            "quantidade": item["quantidade"],
            "lote": item["lote"],
            "validade": item["validade"],
            "valor_unitario": item["valor_unitario"]

        })

    codigo_anterior = None

    for item in resultado:

        if item["codigo"] == codigo_anterior:

            item["codigo"] = ""
            item["tipo"] = ""
            item["fornecedor"] = ""
            item["origem"] = ""
            item["numero_nf"] = ""
            item["valor_total"] = ""
            item["usuario"] = ""
            item["data"] = ""

        else:

            codigo_anterior = item["codigo"]    

    return resultado

def consultar_saidas_relatorio():

    resposta = (
        supabase
        .table("itens_saida")
        .select("""
            quantidade,
            lote,
            saidas(
                codigo,
                tipo,
                setor,
                motivo,
                usuario,
                data
            ),
            produtos(
                nome
            )
        """)
        .execute()
    )

    resultado = []

    for item in resposta.data:

        saida = item["saidas"]
        produto = item["produtos"]

        resultado.append({

            "codigo": saida["codigo"],
            "tipo": saida["tipo"],
            "setor": saida["setor"],
            "motivo": saida["motivo"],
            "usuario": saida["usuario"],
            "data": saida["data"],

            "produto": produto["nome"],

            "quantidade": item["quantidade"],
            "lote": item["lote"]

        })

    codigo_anterior = None

    for item in resultado:

        if item["codigo"] == codigo_anterior:

            item["codigo"] = ""
            item["tipo"] = ""
            item["setor"] = ""
            item["motivo"] = ""
            item["usuario"] = ""
            item["data"] = ""

        else:

            codigo_anterior = item["codigo"]    

    return resultado

def consultar_movimentacao_produto_relatorio(produto):

    movimentacoes = []

    # ==========================
    # ENTRADAS
    # ==========================

    resposta = (
        supabase
        .table("itens_entrada")
        .select("""
            quantidade,
            lote,
            entradas(
                data,
                tipo,
                usuario
            ),
            produtos(nome)
        """)
        .execute()
    )

    for item in resposta.data:

        if not item["produtos"]:
            continue

        if item["produtos"]["nome"] != produto:
            continue

        movimentacoes.append({

            "data_mov": item["entradas"]["data"],
            "movimento": "ENTRADA",
            "tipo": item["entradas"]["tipo"],
            "produto": item["produtos"]["nome"],
            "quantidade": item["quantidade"],
            "lote": item["lote"],
            "usuario": item["entradas"]["usuario"]

        })

    # ==========================
    # SAÍDAS
    # ==========================

    resposta = (
        supabase
        .table("itens_saida")
        .select("""
            quantidade,
            lote,
            saidas(
                data,
                tipo,
                usuario
            ),
            produtos(nome)
        """)
        .execute()
    )

    for item in resposta.data:

        if not item["produtos"]:
            continue

        if item["produtos"]["nome"] != produto:
            continue

        movimentacoes.append({

            "data_mov": item["saidas"]["data"],
            "movimento": "SAIDA",
            "tipo": item["saidas"]["tipo"],
            "produto": item["produtos"]["nome"],
            "quantidade": item["quantidade"],
            "lote": item["lote"],
            "usuario": item["saidas"]["usuario"]

        })

    # ==========================
    # AJUSTES
    # ==========================

    resposta = (
        supabase
        .table("ajustes_estoque")
        .select("*")
        .eq("produto", produto)
        .execute()
    )

    for item in resposta.data:

        movimentacoes.append({

            "data_mov": item["data"],
            "movimento": "AJUSTE",
            "tipo": item["acao"],
            "produto": item["produto"],
            "quantidade": 0,
            "antes": item["antes"],
            "depois": item["depois"],
            "lote": "",
            "usuario": item["usuario"]

        })

    movimentacoes.sort(
        key=lambda x: x["data_mov"]
    )

    return movimentacoes

def buscar_estoque_atual_produto(nome_produto):

    resposta = (
        supabase
        .table("produtos")
        .select("estoque")
        .eq("nome", nome_produto)
        .execute()
    )

    if not resposta.data:
        return 0

    return resposta.data[0]["estoque"] or 0

def listar_origens_relatorio(tipo):

    resposta = (
        supabase
        .table("entradas")
        .select("origem")
        .eq("tipo", tipo)
        .execute()
    )

    origens = sorted({

        item["origem"]

        for item in resposta.data

        if item["origem"]

    })

    return origens

def listar_setores_saida_relatorio(tipo):

    resposta = (
        supabase
        .table("saidas")
        .select("setor")
        .eq("tipo", tipo)
        .execute()
    )

    setores = sorted({

        item["setor"]

        for item in resposta.data

        if item["setor"]

    })

    return setores
