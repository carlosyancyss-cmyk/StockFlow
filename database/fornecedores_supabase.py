from database.api import (
    select,
    insert,
)

def cadastrar_fornecedor(nome, cnpj):

    try:

        insert(
            "fornecedores",
            {
                "nome": nome,
                "cnpj": cnpj
            }
        )

        return True

    except Exception as erro:

        print(erro)
        return False
    
def listar_fornecedores():

    return select(
        "fornecedores",
        "*",
        order="nome"
    )