from database.supabase_db import supabase


def cadastrar_setor(nome):

    try:

        (
            supabase
            .table("setores")
            .insert({
                "nome": nome
            })
            .execute()
        )

        return True

    except Exception as erro:

        print(erro)
        return False


def listar_setores():

    resposta = (
        supabase
        .table("setores")
        .select("*")
        .order("nome")
        .execute()
    )

    return resposta.data