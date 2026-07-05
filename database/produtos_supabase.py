from database.supabase_db import supabase


def listar_produtos():

    resposta = (
        supabase
        .table("produtos")
        .select("*")
        .order("nome")
        .execute()
    )

    return resposta.data


def cadastrar_produto(
    nome,
    unidade_medida,
    estoque_minimo
):

    try:

        existente = (
            supabase
            .table("produtos")
            .select("id")
            .eq("nome", nome)
            .execute()
        )

        if existente.data:
            return False

        (
            supabase
            .table("produtos")
            .insert({
                "nome": nome,
                "unidade_medida": unidade_medida,
                "estoque_minimo": estoque_minimo,
                "estoque": 0
            })
            .execute()
        )

        return True

    except Exception as erro:

        print(erro)
        return False


def atualizar_produto_cadastrado(
    produto_id,
    nome,
    unidade_medida,
    estoque_minimo
):

    try:

        (
            supabase
            .table("produtos")
            .update({
                "nome": nome,
                "unidade_medida": unidade_medida,
                "estoque_minimo": estoque_minimo
            })
            .eq("id", produto_id)
            .execute()
        )

        return True

    except Exception as erro:

        print(erro)
        return False
    
def excluir_produto(produto_id):

    try:

        resposta = (
            supabase
            .table("produtos")
            .delete()
            .eq("id", produto_id)
            .execute()
        )

        print("RESPOSTA DELETE:", resposta)

        return True

    except Exception as erro:

        print("ERRO DELETE:", erro)
        return False 
    
def buscar_produto_por_nome(nome):

    resposta = (
        supabase
        .table("produtos")
        .select("*")
        .eq("nome", nome)
        .execute()
    )

    if resposta.data:
        return resposta.data[0]

    return None  

def buscar_produto_por_nome(nome):

    resposta = (
        supabase
        .table("produtos")
        .select("*")
        .eq("nome", nome)
        .execute()
    )

    if resposta.data:
        return resposta.data[0]

    return None 

def listar_nomes_produtos():

    resposta = (
        supabase
        .table("produtos")
        .select("nome")
        .order("nome")
        .execute()
    )

    return resposta.data 