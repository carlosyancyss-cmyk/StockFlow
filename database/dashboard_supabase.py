from database.api import rpc


def total_produtos():

    return rpc("total_produtos")

def estoque_total():

    return rpc("estoque_total")

def total_entradas():

    return rpc("total_entradas")

def total_saidas():

    return rpc("total_saidas")

def produtos_estoque_baixo():

    return rpc(
        "dashboard_produtos_estoque_baixo"
    )

def proximos_vencimentos():

    return rpc(
        "dashboard_proximos_vencimentos"
    )

def listar_movimentacoes():

    return rpc(
        "dashboard_listar_movimentacoes"
    )

def buscar_itens_historico_entrada(entrada_id):

    return rpc(
        "dashboard_itens_entrada",
        {
            "p_entrada_id": entrada_id
        }
    )

def buscar_itens_historico_saida(saida_id):

    return rpc(
        "dashboard_itens_saida",
        {
            "p_saida_id": saida_id
        }
    )

def ultimas_movimentacoes():

    return rpc(
        "dashboard_ultimas_movimentacoes"
    )