import flet as ft

BRANCO = "#FFFFFF"
AZUL = "#1565C0"
AZUL_CLARO = "#EAF3FF"
VERDE = "#2E7D32"
VERDE_CLARO = "#EAF8EF"
FUNDO = "#F5F9FF"
TEXTO = "#1F2937"
CINZA = "#607080"

PADDING_TELA = 15
PADDING_CARD = 20
ESPACAMENTO = 10
RAIO_CARD = 8
LARGURA_CONTEUDO = 1100


def aplicar_tema_page(page):

    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = FUNDO


def botao_primario(texto, icon=None, on_click=None, width=None, height=45):

    return ft.Button(
        texto,
        icon=icon,
        on_click=on_click,
        bgcolor=AZUL,
        color=BRANCO,
        width=width,
        height=height
    )


def botao_sucesso(
    texto,
    icon=None,
    on_click=None,
    width=None,
    height=45,
    visible=True
):

    return ft.Button(
        texto,
        icon=icon,
        on_click=on_click,
        bgcolor=VERDE,
        color=BRANCO,
        width=width,
        height=height,
        visible=visible
    )


def botao_secundario(texto, icon=None, on_click=None, width=None, height=45):

    return ft.Button(
        texto,
        icon=icon,
        on_click=on_click,
        bgcolor=BRANCO,
        color=AZUL,
        width=width,
        height=height
    )


def card_padrao(
    content,
    width=None,
    height=None,
    padding=PADDING_CARD,
    on_click=None
):

    return ft.Card(
        elevation=2,
        bgcolor=BRANCO,
        content=ft.Container(
            content=content,
            width=width,
            height=height,
            padding=padding,
            border_radius=RAIO_CARD,
            on_click=on_click
        )
    )


def titulo_pagina(texto, icone):

    return ft.Row(
        [
            ft.Icon(
                icone,
                size=34,
                color=AZUL
            ),
            ft.Text(
                texto,
                size=24,
                weight=ft.FontWeight.BOLD,
                color=TEXTO
            )
        ],
        wrap=True,
        spacing=ESPACAMENTO,
        run_spacing=ESPACAMENTO,
        alignment=ft.MainAxisAlignment.CENTER
    )


def container_pagina(largura_util, controles):

    return ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        padding=PADDING_TELA,
        bgcolor=FUNDO,
        content=ft.Container(
            width=min(largura_util, LARGURA_CONTEUDO),
            alignment=ft.Alignment(0, -1),
            content=ft.Column(
                controles,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
                spacing=ESPACAMENTO
            )
        )
    )