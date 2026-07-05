from database.supabase_db import supabase


def cadastrar_fornecedor(nome, cnpj):

    try:

        (
            supabase
            .table("fornecedores")
            .insert({
                "nome": nome,
                "cnpj": cnpj
            })
            .execute()
        )

        return True

    except Exception as erro:

        print(erro)
        return False


def listar_fornecedores():

    resposta = (
        supabase
        .table("fornecedores")
        .select("*")
        .order("nome")
        .execute()
    )

    return resposta.data