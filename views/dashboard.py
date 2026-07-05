import flet as ft

from datetime import datetime

print("DASHBOARD CARREGADO")

from database.dashboard_supabase import (
    total_produtos,
    estoque_total,
    total_entradas,
    total_saidas,
    produtos_estoque_baixo,
    proximos_vencimentos,
    listar_movimentacoes,
    buscar_itens_historico_entrada,
    buscar_itens_historico_saida,
    ultimas_movimentacoes
)


from views.tema import (
    AZUL,
    VERDE,
    BRANCO,
    FUNDO,
    TEXTO,
    CINZA,
    PADDING_CARD,
    ESPACAMENTO,
    card_padrao,
    botao_primario,
    botao_sucesso,
    botao_secundario,
    titulo_pagina,
    container_pagina
)

def dashboard_view(page, usuario):

    qtd_produtos = total_produtos()

    qtd_estoque = estoque_total()

    qtd_entradas = total_entradas()

    qtd_saidas = total_saidas()

    baixo_estoque = produtos_estoque_baixo()

    vencimentos = proximos_vencimentos()

    movimentacoes = ultimas_movimentacoes()

    historico = listar_movimentacoes()

    def formatar_data(e):

        valor = e.control.value

        valor = valor.replace("/", "")

        if len(valor) > 8:

            valor = valor[:8]

        if len(valor) >= 5:

            valor = valor[:2] + "/" + valor[2:4] + "/" + valor[4:]

        elif len(valor) >= 3:

            valor = valor[:2] + "/" + valor[2:]

        e.control.value = valor

        e.page.update()

    lista_historico = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )

    data_inicial = ft.TextField(

        label="Data inicial",

        hint_text="dd/mm/aaaa",

        width=180,

        on_change=formatar_data

    )

    data_final = ft.TextField(

        label="Data final",

        hint_text="dd/mm/aaaa",

        width=180,

        on_change=formatar_data

    )

    tipo_movimento = ft.Dropdown(
        label="Tipo",

        width=180,

        value="TODAS",

        options=[

            ft.dropdown.Option("TODAS"),

            ft.dropdown.Option("ENTRADA"),

            ft.dropdown.Option("SAIDA")

        ]

    )

    resultado_historico = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )

    def fechar_detalhe(e):

        dialog_detalhe.open = False

        e.page.update()

    dialog_detalhe = ft.AlertDialog(

        modal=True,

        title=ft.Row(

            [

                ft.Icon(ft.Icons.DESCRIPTION),

                ft.Text(

                    "Detalhes da Movimentação",

                    weight=ft.FontWeight.BOLD

                )

            ],

            alignment=ft.MainAxisAlignment.CENTER,

            spacing=10

        ),

        content=ft.Container(

            content=resultado_historico,

            width=min(page.width - 30, 900),
            height=min(page.height - 150, 650),
            padding=10

        ),

        actions=[

            ft.TextButton(
                "Fechar",
                on_click=fechar_detalhe
            )

        ]

    )

    def fechar_detalhe(e):

        dialog_detalhe.open = False

        e.page.update()

    def visualizar_movimentacao(e, mov):

        resultado_historico.controls.clear()

        resultado_historico.controls.append(

            card_padrao(

                content=ft.Container(

                    content=ft.Column(

                        [

                            ft.Text(
                                f"Código: {mov['codigo']}",
                                size=18,
                                weight=ft.FontWeight.BOLD
                            ),

                            ft.Text(
                                f"Tipo: {mov['tipo']}"
                            ),

                            ft.Text(
                                f"Usuário: {mov['usuario']}"
                            ),

                            ft.Text(
                                f"Movimentação: {mov['movimento']}"
                            ),

                            ft.Text(
                                f"Data: {mov['data']}"
                            )

                        ],
                        spacing=10,

                    ),

                    padding=20

                )

            )

        )

        resultado_historico.controls.append(
            ft.Divider(

                color=VERDE,

                thickness=1

                )
        )
        # =========================
        # ITENS DA MOVIMENTAÇÃO
        # =========================

        resultado_historico.controls.append(

            ft.Container(

                content=ft.Row(

                    [

                        ft.Icon(
                            ft.Icons.INVENTORY
                        ),

                        ft.Text(
                            "Itens da Movimentação",
                            size=18,
                            weight=ft.FontWeight.BOLD
                        )

                    ]

                ),

                padding=10

            )

        )

        if mov["movimento"] == "ENTRADA":

            itens = buscar_itens_historico_entrada(
                mov["id"]
            )

            resultado_historico.controls.append(

                ft.Text(
                    "Itens da Entrada",
                    size=18,
                    weight=ft.FontWeight.BOLD
                )

            )

            for item in itens:

                resultado_historico.controls.append(

                    card_padrao(

                        content=ft.Container(

                            content=ft.Column(

                                [

                                    ft.Text(
                                        f"{item['nome']}",
                                        weight=ft.FontWeight.BOLD
                                    ),

                                    ft.Text(
                                        f"Quantidade: {item['quantidade']}"
                                    ),

                                    ft.Text(
                                        f"Lote: {item['lote']}"
                                    ),

                                    ft.Text(
                                        f"Validade: {item['validade']}"
                                    )

                                ]

                            ),

                            padding=10

                        )

                    )

                )

        else:

            itens = buscar_itens_historico_saida(
                mov["id"]
            )

            resultado_historico.controls.append(

                ft.Text(
                    "Itens da Saída",
                    size=18,
                    weight=ft.FontWeight.BOLD
                )

            )

            for item in itens:

                resultado_historico.controls.append(

                    card_padrao(

                        content=ft.Container(

                            content=ft.Column(

                                [

                                    ft.Text(
                                        f"{item['nome']}",
                                        weight=ft.FontWeight.BOLD
                                    ),

                                    ft.Text(
                                        f"Quantidade: {item['quantidade']}"
                                    ),

                                    ft.Text(
                                        f"Lote: {item['lote']}"
                                    )

                                ]

                            ),

                            padding=10

                        )

                    )

                )

        if dialog_detalhe not in e.page.overlay:
            e.page.overlay.append(dialog_detalhe)

        dialog_detalhe.open = True

        e.page.update()

    def filtrar_historico(e):

        lista_historico.controls.clear()

        for mov in historico:

            try:

                data_mov = datetime.fromisoformat(
                    mov["data"]
                )

                if data_inicial.value:

                    dt_inicio = datetime.strptime(

                        data_inicial.value,

                        "%d/%m/%Y"

                    )

                    if data_mov < dt_inicio:

                        continue

                if data_final.value:

                    dt_fim = datetime.strptime(

                        data_final.value,

                        "%d/%m/%Y"

                    )

                    dt_fim = dt_fim.replace(

                        hour=23,

                        minute=59,

                        second=59

                    )

                    if data_mov > dt_fim:

                        continue

                if tipo_movimento.value != "TODAS":

                    movimento = mov["movimento"]

                    movimento = movimento.upper()

                    movimento = movimento.replace("Í","I")

                    selecionado = tipo_movimento.value

                    selecionado = selecionado.upper()

                    selecionado = selecionado.replace("Í","I")

                    if movimento != selecionado:

                        continue

            except:

                pass

            lista_historico.controls.append(

                card_padrao(

                    content=ft.Container(

                        content=ft.Column(

                            [

                                ft.Text(

                                    f"{'📥' if mov['movimento']=='ENTRADA' else '📤'} {mov['codigo']}",

                                    size=18,

                                    weight=ft.FontWeight.BOLD

                                ),

                                ft.Text(

                                    mov["tipo"]

                                ),

                                ft.Text(

                                    f"{mov['usuario']}"

                                ),

                                ft.Text(

                                    f"{mov['data']}"

                                ),

                                botao_primario(

                                    "Visualizar Detalhes",

                                    icon=ft.Icons.VISIBILITY,

                                    on_click=lambda e, m=mov:

                                        visualizar_movimentacao(e, m)

                                )

                            ]

                        ),

                        padding=15

                    )

                )

            )

        e.page.update()    


    def abrir_historico(e):

        lista_historico.controls.clear()

        for mov in historico:

            lista_historico.controls.append(

                card_padrao(

                    content=ft.Container(

                        content=ft.Column(

                            [

                                ft.Text(
                                    f"{'📥' if mov['movimento'] == 'ENTRADA' else '📤'} {mov['codigo']}",
                                    size=18,
                                    weight=ft.FontWeight.BOLD
                                ),

                                ft.Text(
                                    mov["tipo"]
                                ),

                                ft.Text(
                                    f"{mov['usuario']}"
                                ),

                                ft.Text(
                                    f"{mov['data']}"
                                ),

                                botao_primario(

                                    "Visualizar Detalhes",

                                    icon=ft.Icons.VISIBILITY,

                                    on_click=lambda e, m=mov:
                                        visualizar_movimentacao(e, m)

                                )

                            ]

                        ),

                        padding=15

                    )

                )

            )

        if dialog_historico not in e.page.overlay:
            e.page.overlay.append(dialog_historico)

        dialog_historico.open = True

        e.page.update()

    def fechar_historico(e):

        dialog_historico.open = False

        e.page.update() 

    dialog_historico = ft.AlertDialog(

        modal=True,

        title=ft.Row(

            [

                ft.Icon(
                    ft.Icons.HISTORY
                ),

                ft.Text(
                    "Histórico de Movimentações"
                )

            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,

        ),

        content=ft.Container(

            content=ft.Column(

                [

                    ft.Row(

                        [

                            data_inicial,

                            data_final,

                            tipo_movimento,

                            botao_primario(
                                "Filtrar",
                                icon=ft.Icons.SEARCH,
                                width=140,
                                height=45,
                                on_click=filtrar_historico
                            ),

                        ],

                        wrap=True,
                        spacing=10,

                        run_spacing=10,

                        alignment=ft.MainAxisAlignment.CENTER,

                    ),

                    ft.Divider(

                    color=VERDE,

                    thickness=1

                    ),

                    lista_historico

                ],

                scroll=ft.ScrollMode.AUTO

            ),

            width=min(page.width - 30, 900),
            height=min(page.height - 150, 650),
            padding=10

        ),

        actions=[

            ft.TextButton(
                "Fechar",
                on_click=fechar_historico
            )

        ]

    )       

    return ft.Container(

        expand=True,

        bgcolor=BRANCO,

        alignment=ft.Alignment(0, 0),

        padding=15,

        content=ft.Container(

            width=min(page.width - 30, 1100),

            alignment=ft.Alignment(0, -1),

            content=ft.Column(
        [
            card_padrao(
                content=ft.Column(
                    [
                        ft.Text(
                            "STOCK FLOW",
                            size=40,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Text(
                            "Sistema de Controle de Estoque",
                            size=18
                        ),

                        ft.Divider(

                        color=VERDE,

                        thickness=1

                        ),

                        ft.Text(
                            f"{usuario['nome']}",
                            size=18,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Text(
                            f"Perfil: {usuario['perfil']}",
                            size=16
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                width=min(page.width - 40, 900)
            ),

            ft.ResponsiveRow(

                [

                    ft.Container(

                        col={"xs":12,"sm":6,"md":3},

                        content=card_padrao(

                            content=ft.Column(

                                [

                                    ft.Text(

                                        "Produtos",

                                        size=20,

                                        weight=ft.FontWeight.BOLD,

                                        color=TEXTO


                                    ),

                                    ft.Divider(

                                    color=VERDE,

                                    thickness=1

                                    ),

                                    ft.Text(

                                        str(qtd_produtos),

                                        size=42,

                                        weight=ft.FontWeight.BOLD

                                    )

                                ],

                                horizontal_alignment=ft.CrossAxisAlignment.CENTER

                            )

                        )

                    ),

                    ft.Container(

                        col={"xs":12,"sm":6,"md":3},

                        content=card_padrao(

                            content=ft.Column(

                                [

                                    ft.Text(

                                        "Estoque Total",

                                        size=20,

                                        weight=ft.FontWeight.BOLD,

                                        color=TEXTO

                                    ),

                                    ft.Divider(

                                    color=VERDE,

                                    thickness=1

                                    ),

                                    ft.Text(

                                        str(qtd_estoque),

                                        size=42,

                                        weight=ft.FontWeight.BOLD

                                    )

                                ],

                                horizontal_alignment=ft.CrossAxisAlignment.CENTER

                            )

                        )

                    ),

                    ft.Container(

                        col={"xs":12,"sm":6,"md":3},

                        content=card_padrao(

                            content=ft.Column(

                                [

                                    ft.Text(

                                        "Entradas",

                                        size=20,

                                        weight=ft.FontWeight.BOLD,

                                        color=TEXTO

                                    ),

                                    ft.Divider(

                                    color=VERDE,

                                    thickness=1

                                    ),

                                    ft.Text(

                                        str(qtd_entradas),

                                        size=42,

                                        weight=ft.FontWeight.BOLD

                                    )

                                ],

                                horizontal_alignment=ft.CrossAxisAlignment.CENTER

                            )

                        )

                    ),

                    ft.Container(

                        col={"xs":12,"sm":6,"md":3},

                        content=card_padrao(

                            content=ft.Column(

                                [

                                    ft.Text(

                                        "Saídas",

                                        size=20,

                                        weight=ft.FontWeight.BOLD,

                                        color=TEXTO

                                    ),

                                    ft.Divider(

                                    color=VERDE,

                                    thickness=1

                                    ),

                                    ft.Text(

                                        str(qtd_saidas),

                                        size=42,

                                        weight=ft.FontWeight.BOLD

                                    )

                                ],

                                horizontal_alignment=ft.CrossAxisAlignment.CENTER

                            )

                        )

                    ),

                ],

                spacing=10,

                run_spacing=10

            ),   

        ft.Divider(

        color=VERDE,

        thickness=1

        ),

        ft.Row(
            [

                card_padrao(
                    content=ft.Container(
                        expand=True,
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Estoque Baixo",
                                    size=20,

                                    weight=ft.FontWeight.BOLD,

                                    color=TEXTO
                                ),

                                ft.Divider(

                                color=VERDE,

                                thickness=1

                                ),

                                ft.Column(
                                    [
                                        ft.Text(
                                            f"{produto['nome']} - Estoque: {produto['estoque']} / Mínimo: {produto['estoque_minimo']}"
                                        )
                                        for produto in baixo_estoque
                                    ]
                                    if baixo_estoque
                                    else [
                                        ft.Text(
                                            "Nenhum item em alerta"
                                        )
                                    ]
                                )
                            ],
                            spacing=10,
                        ),
                        padding=20,

                        width=min(page.width - 40, 450),
                        height=260
                    )
                ),

                card_padrao(
                    content=ft.Container(
                        expand=True,
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Próximos Vencimentos",
                                    size=20,

                                    weight=ft.FontWeight.BOLD,

                                    color=TEXTO
                                ),
                                
                                ft.Divider(

                                color=VERDE,

                                thickness=1

                                ),

                                ft.Column(
                                    [
                                        ft.Text(
                                            f"{item['nome']} - {item['validade']}"
                                        )
                                        for item in vencimentos
                                    ]
                                    if vencimentos
                                    else [
                                        ft.Text(
                                            "Nenhum item em alerta"
                                        )
                                    ]
                                )
                            ],
                            spacing=10,
                        ),
                        padding=20,

                        width=min(page.width - 40, 450),
                        height=260
                    )
                )

            ],

            wrap=True,

            spacing=10,

            run_spacing=10,

            alignment=ft.MainAxisAlignment.CENTER
        ),

        ft.Divider(

        color=VERDE,

        thickness=1

        ),

        ft.Row(
        [
            ft.Icon(
                ft.Icons.HISTORY,
                size=28
            ),

            ft.Text(
                "Últimas Movimentações",
                size=20,

                weight=ft.FontWeight.BOLD,

                color=TEXTO
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    ),

        ft.Column(

            [

                card_padrao(

                    content=ft.Container(

                        content=ft.Column(

                            [

                                ft.Text(

                                    f"{'📥' if mov['movimento'] == 'ENTRADA' else '📤'} "

                                    f"{mov['codigo']}",

                                    size=20,

                                    weight=ft.FontWeight.BOLD

                                ),

                                ft.Text(

                                    mov["tipo"],

                                    size=16

                                ),

                                ft.Divider(

                                color=VERDE,

                                thickness=1

                                ),

                                ft.Text(

                                    f"{mov['usuario']}"

                                ),

                                ft.Text(

                                    "" +

                                    datetime.fromisoformat(
                                        mov["data"]
                                    ).strftime(
                                        "%d/%m/%Y %H:%M"
                                    )

                                )

                            ],

                            spacing=10

                        ),

                        padding=20

                    )

                )

                for mov in movimentacoes

            ]

            if movimentacoes

            else

            [

                ft.Container(

                    content=ft.Column(

                        [

                            ft.Icon(

                                ft.Icons.INBOX,

                                size=60

                            ),

                            ft.Text(

                                "Nenhuma movimentação encontrada",

                                size=18,

                                weight=ft.FontWeight.BOLD

                            )

                        ],

                        horizontal_alignment=ft.CrossAxisAlignment.CENTER

                    ),

                    padding=20

                )

            ],

            width=min(page.width - 40, 900),

            spacing=15

        ),

        botao_primario(
            "Ver Histórico Completo",
            icon=ft.Icons.HISTORY,
            width=320,
            height=50,
            on_click=abrir_historico
        ),
        
        ft.Divider(

        color=VERDE,

        thickness=1

        ),

        ft.Column(
            [
                ft.Text(
                    "Stock Flow v1.0",

                    italic=True,

                    size=14,

                    weight=ft.FontWeight.W_500

                ),

                ft.Text(
                    datetime.now().strftime(
                        "%d/%m/%Y %H:%M"
                    ),

                    size=13

                )
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        ],

scroll=ft.ScrollMode.AUTO,
spacing=18,
horizontal_alignment=ft.CrossAxisAlignment.CENTER

            )

        )

    )