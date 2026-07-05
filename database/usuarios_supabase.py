from database.supabase_db import supabase


def login_usuario(email, senha):

    resposta = (
        supabase
        .table("usuarios")
        .select("*")
        .eq("email", email)
        .eq("senha", senha)
        .eq("status", "ATIVO")
        .execute()
    )

    if resposta.data:
        return resposta.data[0]

    return None

def cadastrar_usuario(nome, telefone, email, senha):

    try:

        dados = {
            "nome": nome,
            "telefone": telefone,
            "email": email,
            "senha": senha,
            "perfil": "PENDENTE",
            "status": "PENDENTE"
        }

        (
            supabase
            .table("usuarios")
            .insert(dados)
            .execute()
        )

        return True

    except Exception as erro:

        print(erro)
        return False


def buscar_usuario_ativo_por_email(email):

    resposta = (
        supabase
        .table("usuarios")
        .select("*")
        .eq("email", email)
        .eq("status", "ATIVO")
        .execute()
    )

    if resposta.data:
        return resposta.data[0]

    return None

def listar_usuarios():

    resposta = (
        supabase
        .table("usuarios")
        .select("*")
        .order("id")
        .execute()
    )

    return resposta.data


def atualizar_perfil_usuario(usuario_id, perfil):

    (
        supabase
        .table("usuarios")
        .update({
            "perfil": perfil
        })
        .eq("id", usuario_id)
        .execute()
    )


def atualizar_status_usuario(usuario_id, status):

    (
        supabase
        .table("usuarios")
        .update({
            "status": status
        })
        .eq("id", usuario_id)
        .execute()
    )

def recuperar_senha_usuario(email, nova_senha):

    resposta = (
        supabase
        .table("usuarios")
        .select("id")
        .eq("email", email)
        .execute()
    )

    if not resposta.data:
        return False

    (
        supabase
        .table("usuarios")
        .update({
            "senha": nova_senha
        })
        .eq("email", email)
        .execute()
    )

    return True  

def atualizar_dados_usuario(
    usuario_id,
    nome,
    telefone,
    email
):

    (
        supabase
        .table("usuarios")
        .update({
            "nome": nome,
            "telefone": telefone,
            "email": email
        })
        .eq("id", usuario_id)
        .execute()
    )

    return True  

def alterar_senha(
    usuario_id,
    senha_atual,
    nova_senha
):

    resposta = (
        supabase
        .table("usuarios")
        .select("senha")
        .eq("id", usuario_id)
        .execute()
    )

    if not resposta.data:
        return False

    if resposta.data[0]["senha"] != senha_atual:
        return False

    (
        supabase
        .table("usuarios")
        .update({
            "senha": nova_senha
        })
        .eq("id", usuario_id)
        .execute()
    )

    return True