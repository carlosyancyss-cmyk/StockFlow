from database.api import (
    select,
    select_where,
    insert,
    update,
    delete,
)


def listar_produtos():

    return select(
        "produtos",
        "*",
        order="nome"
    )

def cadastrar_produto(
    nome,
    unidade_medida,
    estoque_minimo
):

    try:

        if select_where(
            "produtos",
            "id",
            {"nome": nome}
        ):
            return False

        insert(
            "produtos",
            {
                "nome": nome,
                "unidade_medida": unidade_medida,
                "estoque_minimo": estoque_minimo,
                "estoque": 0
            }
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

        update(
            "produtos",
            {
                "id": produto_id
            },
            {
                "nome": nome,
                "unidade_medida": unidade_medida,
                "estoque_minimo": estoque_minimo
            }
        )

        return True

    except Exception as erro:

        print(erro)
        return False

def excluir_produto(produto_id):

    try:

        delete(
            "produtos",
            {
                "id": produto_id
            }
        )

        return True

    except Exception as erro:

        print(erro)
        return False

def buscar_produto_por_nome(nome):

    dados = select_where(
        "produtos",
        "*",
        {
            "nome": nome
        }
    )

    if dados:
        return dados[0]

    return None

def listar_nomes_produtos():

    return select(
        "produtos",
        "nome",
        order="nome"
    )