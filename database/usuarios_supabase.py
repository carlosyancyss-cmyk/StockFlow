from database.api import (
    select,
    select_where,
    insert,
    update,
)


def login_usuario(email, senha):

    dados = select_where(
        "usuarios",
        "*",
        {
            "email": email,
            "senha": senha,
            "status": "ATIVO"
        }
    )

    if dados:
        return dados[0]

    return None

def cadastrar_usuario(nome, telefone, email, senha):

    try:

        insert(
            "usuarios",
            {
                "nome": nome,
                "telefone": telefone,
                "email": email,
                "senha": senha,
                "perfil": "PENDENTE",
                "status": "PENDENTE",
            }
        )

        return True

    except Exception:

        return False

def buscar_usuario_ativo_por_email(email):

    dados = select_where(
        "usuarios",
        "*",
        {
            "email": email,
            "status": "ATIVO"
        }
    )

    if dados:
        return dados[0]

    return None

def listar_usuarios():

    return select(
        "usuarios",
        "*",
        order="id"
    )

def atualizar_perfil_usuario(usuario_id, perfil):

    update(
        "usuarios",
        {
            "id": usuario_id
        },
        {
            "perfil": perfil
        }
    )

def atualizar_status_usuario(usuario_id, status):

    update(
        "usuarios",
        {
            "id": usuario_id
        },
        {
            "status": status
        }
    )

def recuperar_senha_usuario(email, nova_senha):

    try:

        update(
            "usuarios",
            {
                "email": email
            },
            {
                "senha": nova_senha
            }
        )

        return True

    except Exception:

        return False

def atualizar_dados_usuario(usuario_id, nome, telefone, email):

    update(
        "usuarios",
        {
            "id": usuario_id
        },
        {
            "nome": nome,
            "telefone": telefone,
            "email": email,
        }
    )

    return True

def alterar_senha(usuario_id, senha_atual, nova_senha):

    dados = select_where(
        "usuarios",
        "senha",
        {
            "id": usuario_id
        }
    )

    if not dados:
        return False

    if dados[0]["senha"] != senha_atual:
        return False

    update(
        "usuarios",
        {
            "id": usuario_id
        },
        {
            "senha": nova_senha
        }
    )

    return True