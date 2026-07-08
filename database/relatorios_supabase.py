from database.api import (
    select,
    select_where,
    rpc,
)

def listar_fornecedores_relatorio():

    dados = select(
        "fornecedores",
        "nome",
        order="nome"
    )

    return [
        {"fornecedor": item["nome"]}
        for item in dados
    ]

def listar_setores_relatorio():

    dados = select(
        "setores",
        "nome",
        order="nome"
    )

    return [
        {"setor": item["nome"]}
        for item in dados
    ]

def listar_produtos_relatorio():

    return select(
        "produtos",
        "nome",
        order="nome"
    )

def listar_ajustes_estoque(data_inicio=None, data_fim=None, usuario=None):

    parametros = {}

    if data_inicio:
        parametros["data_inicio"] = data_inicio

    if data_fim:
        parametros["data_fim"] = data_fim

    if usuario:
        parametros["usuario"] = usuario

    return rpc(
        "listar_ajustes_relatorio",
        parametros
    )

def consultar_entradas_relatorio():

    resultado = rpc(
        "consultar_entradas_relatorio"
    )

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

    resultado = rpc(
        "consultar_saidas_relatorio"
    )

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

    return rpc(
        "consultar_movimentacao_produto_relatorio",
        {
            "p_produto": produto
        }
    )

def buscar_estoque_atual_produto(nome_produto):

    dados = select_where(
        "produtos",
        "estoque",
        {"nome": nome_produto}
    )

    if not dados:
        return 0

    return dados[0]["estoque"] or 0

def listar_origens_relatorio(tipo):

    dados = select_where(
        "entradas",
        "origem",
        {"tipo": tipo}
    )

    return sorted({
        item["origem"]
        for item in dados
        if item["origem"]
    })

def listar_setores_saida_relatorio(tipo):

    dados = select_where(
        "saidas",
        "setor",
        {"tipo": tipo}
    )

    return sorted({
        item["setor"]
        for item in dados
        if item["setor"]
    })
