import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}


def select(tabela, campos="*", order=None):

    url = f"{SUPABASE_URL}/rest/v1/{tabela}?select={campos}"

    if order:
        url += f"&order={order}"

    resposta = httpx.get(
        url,
        headers=HEADERS,
        timeout=60
    )

    resposta.raise_for_status()

    return resposta.json()


def select_where(
    tabela,
    campos="*",
    filtros=None,
    order=None
):

    url = f"{SUPABASE_URL}/rest/v1/{tabela}?select={campos}"

    if filtros:

        for campo, valor in filtros.items():

            if isinstance(valor, tuple):

                operador, dado = valor

                url += f"&{campo}={operador}.{dado}"

            else:

                url += f"&{campo}=eq.{valor}"

    if order:
        url += f"&order={order}"

    resposta = httpx.get(
        url,
        headers=HEADERS,
        timeout=60
    )

    resposta.raise_for_status()

    return resposta.json()


def insert(tabela, dados):

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

    return resposta.json()


def update(tabela, filtros, dados):

    url = f"{SUPABASE_URL}/rest/v1/{tabela}?"

    primeiro = True

    for campo, valor in filtros.items():

        if not primeiro:
            url += "&"

        url += f"{campo}=eq.{valor}"

        primeiro = False

    resposta = httpx.patch(
        url,
        headers={
            **HEADERS,
            "Prefer": "return=representation"
        },
        json=dados,
        timeout=60
    )

    resposta.raise_for_status()

    return resposta.json()


def delete(tabela, filtros):

    url = f"{SUPABASE_URL}/rest/v1/{tabela}?"

    primeiro = True

    for campo, valor in filtros.items():

        if not primeiro:
            url += "&"

        url += f"{campo}=eq.{valor}"

        primeiro = False

    resposta = httpx.delete(
        url,
        headers=HEADERS,
        timeout=60
    )

    resposta.raise_for_status()

    return True


def rpc(nome_funcao, parametros=None):

    if parametros is None:
        parametros = {}

    resposta = httpx.post(
        f"{SUPABASE_URL}/rest/v1/rpc/{nome_funcao}",
        headers=HEADERS,
        json=parametros,
        timeout=120
    )

    resposta.raise_for_status()

    return resposta.json()


def get(url):

    resposta = httpx.get(
        f"{SUPABASE_URL}/rest/v1/{url}",
        headers=HEADERS,
        timeout=60
    )

    resposta.raise_for_status()

    return resposta.json()


def post(url, dados):

    resposta = httpx.post(
        f"{SUPABASE_URL}/rest/v1/{url}",
        headers={
            **HEADERS,
            "Prefer": "return=representation"
        },
        json=dados,
        timeout=60
    )

    resposta.raise_for_status()

    return resposta.json()


def patch(url, dados):

    resposta = httpx.patch(
        f"{SUPABASE_URL}/rest/v1/{url}",
        headers={
            **HEADERS,
            "Prefer": "return=representation"
        },
        json=dados,
        timeout=60
    )

    resposta.raise_for_status()

    return resposta.json()


def remove(url):

    resposta = httpx.delete(
        f"{SUPABASE_URL}/rest/v1/{url}",
        headers=HEADERS,
        timeout=60
    )

    resposta.raise_for_status()

    return True