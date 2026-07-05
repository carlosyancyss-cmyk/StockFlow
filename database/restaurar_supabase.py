import json

from database.supabase_db import supabase


ORDEM_EXCLUSAO = [

    "itens_saida",
    "saidas",

    "itens_entrada",
    "entradas",

    "lotes",

    "ajustes_estoque",

    "produtos",

    "fornecedores",

    "setores",

    "usuarios"

]


def limpar_tabelas():

    for tabela in ORDEM_EXCLUSAO:

        (
            supabase
            .table(tabela)
            .delete()
            .neq("id", 0)
            .execute()
        )


def restaurar_backup(caminho):

    with open(
        caminho,
        "r",
        encoding="utf-8"
    ) as arquivo:

        backup = json.load(arquivo)

    print("JSON CARREGADO")

    limpar_tabelas()

    print("BANCO LIMPO")

    mapa_usuarios = {}
    mapa_fornecedores = {}
    mapa_setores = {}
    mapa_produtos = {}
    mapa_entradas = {}
    mapa_saidas = {}

    # ==========================
    # USUÁRIOS
    # ==========================

    print("RESTAURANDO USUARIOS")

    for registro in backup.get("usuarios", []):

        antigo_id = registro["id"]

        dados = registro.copy()
        dados.pop("id", None)

        novo = (
            supabase
            .table("usuarios")
            .insert(dados)
            .execute()
        )

        mapa_usuarios[antigo_id] = novo.data[0]["id"]

    # ==========================
    # FORNECEDORES
    # ==========================

    print("RESTAURANDO FORNECEDORES")

    for registro in backup.get("fornecedores", []):

        antigo_id = registro["id"]

        dados = registro.copy()
        dados.pop("id", None)

        novo = (
            supabase
            .table("fornecedores")
            .insert(dados)
            .execute()
        )

        mapa_fornecedores[antigo_id] = novo.data[0]["id"]

    # ==========================
    # SETORES
    # ==========================

    print("RESTAURANDO SETORES")

    for registro in backup.get("setores", []):

        antigo_id = registro["id"]

        dados = registro.copy()
        dados.pop("id", None)

        novo = (
            supabase
            .table("setores")
            .insert(dados)
            .execute()
        )

        mapa_setores[antigo_id] = novo.data[0]["id"]

    # ==========================
    # PRODUTOS
    # ==========================

    print("RESTAURANDO PRODUTOS")

    for registro in backup.get("produtos", []):

        antigo_id = registro["id"]

        dados = registro.copy()
        dados.pop("id", None)

        novo = (
            supabase
            .table("produtos")
            .insert(dados)
            .execute()
        )

        mapa_produtos[antigo_id] = novo.data[0]["id"]

    # ==========================
    # LOTES
    # ==========================

    print("RESTAURANDO LOTES")

    for registro in backup.get("lotes", []):

        dados = registro.copy()
        dados.pop("id", None)

        dados["produto_id"] = mapa_produtos[
            registro["produto_id"]
        ]

        (
            supabase
            .table("lotes")
            .insert(dados)
            .execute()
        )

    # ==========================
    # ENTRADAS
    # ==========================

    print("RESTAURANDO ENTRADAS")

    for registro in backup.get("entradas", []):

        antigo_id = registro["id"]

        dados = registro.copy()
        dados.pop("id", None)

        novo = (
            supabase
            .table("entradas")
            .insert(dados)
            .execute()
        )

        mapa_entradas[antigo_id] = novo.data[0]["id"]

    # ==========================
    # ITENS DE ENTRADA
    # ==========================

    print("RESTAURANDO ITENS_ENTRADA")

    for registro in backup.get("itens_entrada", []):

        dados = registro.copy()
        dados.pop("id", None)

        dados["entrada_id"] = mapa_entradas[
            registro["entrada_id"]
        ]

        dados["produto_id"] = mapa_produtos[
            registro["produto_id"]
        ]

        (
            supabase
            .table("itens_entrada")
            .insert(dados)
            .execute()
        )

    # ==========================
    # SAÍDAS
    # ==========================

    print("RESTAURANDO SAIDAS")

    for registro in backup.get("saidas", []):

        antigo_id = registro["id"]

        dados = registro.copy()
        dados.pop("id", None)

        novo = (
            supabase
            .table("saidas")
            .insert(dados)
            .execute()
        )

        mapa_saidas[antigo_id] = novo.data[0]["id"]

    # ==========================
    # ITENS DE SAÍDA
    # ==========================

    print("RESTAURANDO ITENS_SAIDA")

    for registro in backup.get("itens_saida", []):

        dados = registro.copy()
        dados.pop("id", None)

        dados["saida_id"] = mapa_saidas[
            registro["saida_id"]
        ]

        dados["produto_id"] = mapa_produtos[
            registro["produto_id"]
        ]

        (
            supabase
            .table("itens_saida")
            .insert(dados)
            .execute()
        )

    # ==========================
    # AJUSTES DE ESTOQUE
    # ==========================

    print("RESTAURANDO AJUSTES")

    for registro in backup.get("ajustes_estoque", []):

        dados = registro.copy()
        dados.pop("id", None)

        if "produto_id" in dados and dados["produto_id"] is not None:
            dados["produto_id"] = mapa_produtos[
                registro["produto_id"]
            ]

        (
            supabase
            .table("ajustes_estoque")
            .insert(dados)
            .execute()
        )

    print("RESTAURAÇÃO FINALIZADA")    

    return True 