import json
import httpx

from database.api import SUPABASE_URL, HEADERS


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

def inserir(tabela, dados):

    resposta = httpx.post(
        f"{SUPABASE_URL}/rest/v1/{tabela}",
        headers={
            **HEADERS,
            "Prefer": "return=representation"
        },
        json=dados,
        timeout=60
    )

    resposta.raise_for_status()

    return resposta.json()[0]


def limpar_tabelas():

    for tabela in ORDEM_EXCLUSAO:

        httpx.delete(
            f"{SUPABASE_URL}/rest/v1/{tabela}?id=neq.0",
            headers=HEADERS,
            timeout=60
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

        novo = inserir("usuarios", dados)

        mapa_usuarios[antigo_id] = novo["id"]

    # ==========================
    # FORNECEDORES
    # ==========================

    print("RESTAURANDO FORNECEDORES")

    for registro in backup.get("fornecedores", []):

        antigo_id = registro["id"]

        dados = registro.copy()
        dados.pop("id", None)

        novo = inserir("fornecedores", dados)

        mapa_fornecedores[antigo_id] = novo["id"]

    # ==========================
    # SETORES
    # ==========================

    print("RESTAURANDO SETORES")

    for registro in backup.get("setores", []):

        antigo_id = registro["id"]

        dados = registro.copy()
        dados.pop("id", None)

        novo = inserir("setores", dados)

        mapa_setores[antigo_id] = novo["id"]

    # ==========================
    # PRODUTOS
    # ==========================

    print("RESTAURANDO PRODUTOS")

    for registro in backup.get("produtos", []):

        antigo_id = registro["id"]

        dados = registro.copy()
        dados.pop("id", None)

        novo = inserir("produtos", dados)

        mapa_produtos[antigo_id] = novo["id"]

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

        inserir("lotes", dados)

    # ==========================
    # ENTRADAS
    # ==========================

    print("RESTAURANDO ENTRADAS")

    for registro in backup.get("entradas", []):

        antigo_id = registro["id"]

        dados = registro.copy()
        dados.pop("id", None)

        novo = inserir("entradas", dados)

        mapa_entradas[antigo_id] = novo["id"]

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

        inserir("itens_entrada", dados)

    # ==========================
    # SAÍDAS
    # ==========================

    print("RESTAURANDO SAIDAS")

    for registro in backup.get("saidas", []):

        antigo_id = registro["id"]

        dados = registro.copy()
        dados.pop("id", None)

        novo = inserir("saidas", dados)

        mapa_saidas[antigo_id] = novo["id"]

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

        inserir("itens_saida", dados)

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

        inserir("ajustes_estoque", dados)

    print("RESTAURAÇÃO FINALIZADA")    

    return True 