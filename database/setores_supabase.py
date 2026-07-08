from database.api import (
    select,
    insert,
)


def cadastrar_setor(nome):

    try:

        insert(
            "setores",
            {
                "nome": nome
            }
        )

        return True

    except Exception as erro:

        print(erro)
        return False

def listar_setores():

    return select(
        "setores",
        "*",
        order="nome"
    )