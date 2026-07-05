import flet as ft

from datetime import datetime
from pathlib import Path


from app_paths import REPORTS_DIR, LOGO_PATHS
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image
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

print("SAIDAS.PY CARREGADO")


from database.setores_supabase import (
    cadastrar_setor,
    listar_setores
)

from database.saidas_supabase import (
    salvar_saida,
    salvar_item_saida,
    baixar_estoque,
    gerar_codigo_saida,
    consultar_saida,
    consultar_itens_saida,
    listar_lotes_produto,
    listar_lotes_vencidos,
    listar_produtos_com_lotes_vencidos,
    baixar_estoque_lote,
    baixar_estoque_lotes_agrupados
)

from database.produtos_supabase import (
    buscar_produto_por_nome,
    listar_nomes_produtos
)



#BASE_DIR = Path(__file__).resolve().parent.parent

#REPORTS_DIR = BASE_DIR / "reports"
#REPORTS_DIR.mkdir(exist_ok=True)

#LOGO_PATHS = [
#    BASE_DIR / "assets" / "logo.png",
#    BASE_DIR / "assets" / "logo" / "logo_nova.png",
#    BASE_DIR / "logo.png"
#]

def saidas_view(page, usuario):

    largura_tela = page.width or 390
    altura_tela = page.height or 700

    largura_util = max(largura_tela - 30, 300)

    largura_campo_pequeno = min(largura_util, 250)
    largura_campo_medio = min(largura_util, 300)
    largura_campo_grande = min(largura_util, 400)

    largura_dialog = min(largura_util, 700)
    altura_dialog = min(max(altura_tela - 180, 350), 500)

    largura_botao = min(largura_util, 300)

    # =========================
    # ESTADO
    # =========================
    itens_saida = []

    codigo_text = ft.Text(
        "Código: ---",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=TEXTO
    )

    item_em_edicao = None

    mensagem = ft.Text(
        size=16,
        weight=ft.FontWeight.BOLD
    )

    texto_alerta_estoque = ft.Text()

    dialog_alerta_estoque = ft.AlertDialog(
        modal=True,
        title=ft.Text("Estoque insuficiente"),
        content=texto_alerta_estoque,
        actions=[
            ft.TextButton(
                "OK",
                on_click=lambda e: (
                    setattr(dialog_alerta_estoque, "open", False),
                    e.page.update()
                )
            )
        ]
    )

    dialog_sucesso = ft.AlertDialog(
        modal=True,
        title=ft.Text(""),
        content=ft.Column(),
        actions=[],
    )

    codigo_consulta = ft.TextField(
        label="Código da Saída",
        width=largura_campo_pequeno
    )

    resultado_consulta = ft.Text()

    itens_consulta = ft.Column()

    lista_itens = ft.Column(
        spacing=10
    )

    nome_setor = ft.TextField(
        label="Nome do Setor/Instituição",
        width=largura_campo_medio
    )
    

    # =========================
    # CAMPOS
    # =========================

    setores_db = listar_setores()

    destino = ft.Dropdown(
        label="Destino",
        width=largura_campo_medio,
        visible=False,
        options=[
            ft.dropdown.Option(s["nome"])
            for s in setores_db
        ]
    )

    motivo = ft.TextField(
        label="Motivo",
        width=largura_campo_medio,
        visible=False
    )

    def abrir_setor(e):

        if dialog_setor not in e.page.overlay:
            e.page.overlay.append(dialog_setor)

        dialog_setor.open = True
        e.page.update()

    def abrir_consulta(e):

        if dialog_consulta not in e.page.overlay:

            e.page.overlay.append(
                dialog_consulta
            )

        dialog_consulta.open = True

        e.page.update()    

    def salvar_setor(e):

        if not nome_setor.value:

            return

        sucesso = cadastrar_setor(
            nome_setor.value
        )

        if sucesso:

            destino.options.append(
                ft.dropdown.Option(
                    nome_setor.value
                )
            )

        nome_setor.value = ""

        dialog_setor.open = False

        e.page.update()

    def fechar_setor(e):

        nome_setor.value = ""
        dialog_setor.open = False

        e.page.update()    

    dialog_setor = ft.AlertDialog(
        modal=True,
        title=ft.Text("Novo Setor"),
        content=ft.Column(
            [
                nome_setor
            ],
            tight=True
        ),
        actions=[
            botao_secundario(
                "Cancelar",
                icon=ft.Icons.CLOSE,
                on_click=fechar_setor
            ),

            botao_sucesso(
                "Salvar",
                icon=ft.Icons.SAVE,
                on_click=salvar_setor
            )
        ]
    )  

    def carregar_produtos():

        produto_dropdown.value = None
        produto_dropdown.options.clear()

        if tipo_saida.value == "Saída por Vencimento":

            produtos = listar_produtos_com_lotes_vencidos()

        else:

            produtos = listar_nomes_produtos()

        produto_dropdown.options.extend(
            [
                ft.dropdown.Option(p["nome"])
                for p in produtos
            ]
        )  

    def alterar_tipo_saida(e):

        print("TIPO SAIDA EXECUTOU")
        print(tipo_saida.value)

        carregar_produtos()

        page.update()

        destino.visible = False
        motivo.visible = False

        if tipo_saida.value == "Saída para Setor":
            destino.label = "Setor Destino"
            destino.visible = True

        elif tipo_saida.value == "Saída por Empréstimo":
            destino.label = "Instituição / Responsável"
            destino.visible = True

        elif tipo_saida.value == "Saída por Doação":
            destino.label = "Instituição Beneficiada"
            destino.visible = True

        elif tipo_saida.value == "Saída por Avaria":
            motivo.label = "Motivo da Avaria"
            motivo.visible = True

        elif tipo_saida.value == "Saída por Vencimento":
            motivo.label = "Observação"
            motivo.visible = True

        elif tipo_saida.value == "Ajuste de estoque":
            motivo.label = "Observação do ajuste"
            motivo.visible = True    

        e.page.update()

    tipo_saida = ft.Dropdown(
        label="Tipo de Saída",
        width=largura_campo_medio,
        options=[
            ft.dropdown.Option("Saída para Setor"),
            ft.dropdown.Option("Saída por Empréstimo"),
            ft.dropdown.Option("Saída por Doação"),
            ft.dropdown.Option("Saída por Avaria"),
            ft.dropdown.Option("Saída por Vencimento"),
            ft.dropdown.Option("Ajuste de estoque")

        ],
        on_select=alterar_tipo_saida
    )

    produtos_db = listar_nomes_produtos()

    produto_dropdown = ft.Dropdown(
        label="Produto",
        width=largura_campo_grande,
        options=[
            ft.dropdown.Option(p["nome"])
            for p in produtos_db
        ]
    )

    lote = ft.Dropdown(
        label="Lote disponível",
        width=largura_campo_grande,
        options=[]
    )

    estoque_disponivel = ft.Text(
        "Estoque disponível: -",
        size=16,
        weight=ft.FontWeight.BOLD,
        color=TEXTO
    )

    validade_lote = ft.Text(
        "Validade: -",
        size=16,
        color=TEXTO
    )

    lotes_produto_atual = []

    quantidade = ft.TextField(
        label="Quantidade",
        width=largura_campo_pequeno
    )

    def selecionar_produto(e):

        nonlocal lotes_produto_atual

        lote.options.clear()
        lote.value = None

        estoque_disponivel.value = "Estoque disponível: -"
        validade_lote.value = "Validade: -"

        if not produto_dropdown.value:
            e.page.update()
            return

        if tipo_saida.value == "Saída por Vencimento":

            lotes_produto_atual = listar_lotes_vencidos(
                produto_dropdown.value
            )

        else:

            lotes_produto_atual = listar_lotes_produto(
                produto_dropdown.value
            )

        total_disponivel = 0

        for item in lotes_produto_atual:
            total_disponivel += item["quantidade"]

        estoque_disponivel.value = (
            f"Estoque disponível: {total_disponivel}"
        )    

        for item in lotes_produto_atual:

            lote.options.append(
                ft.dropdown.Option(
                    key=f"{item['lote']}|{item['validade']}",
                    text=(
                        f"{item['lote']} | "
                        f"Validade: {item['validade']} | "
                        f"Qtd: {item['quantidade']}"
                    )
                )
            )

        e.page.update()


    def selecionar_lote(e):

        estoque_disponivel.value = "Estoque disponível: -"
        validade_lote.value = "Validade: -"

        if not lote.value:
            e.page.update()
            return

        for item in lotes_produto_atual:

            if lote.value == f"{item['lote']}|{item['validade']}":

                estoque_disponivel.value = (
                    f"Estoque disponível: {item['quantidade']}"
                )

                validade_lote.value = (
                    f"Validade: {item['validade']}"
                )

                break

        e.page.update()


    produto_dropdown.on_select = selecionar_produto
    lote.on_select = selecionar_lote

    def editar_item(indice):

        nonlocal item_em_edicao

        item = itens_saida[indice]

        produto_dropdown.value = item["produto"]

        lotes_produto_atual.clear()

        if tipo_saida.value == "Saída por Vencimento":

            lotes_produto_atual.extend(
                listar_lotes_vencidos(item["produto"])
            )

        else:

            lotes_produto_atual.extend(
                listar_lotes_produto(item["produto"])
            )

        lote.options.clear()

        for item_lote in lotes_produto_atual:

            lote.options.append(
                ft.dropdown.Option(
                    key=f"{item_lote['lote']}|{item_lote['validade']}",
                    text=(
                        f"{item_lote['lote']} | "
                        f"Validade: {item_lote['validade']} | "
                        f"Qtd: {item_lote['quantidade']}"
                    )
                )
            )

        lote.value = f"{item['lote']}|{item['validade']}"
        quantidade.value = item["quantidade"]

        estoque_disponivel.value = (
            f"Estoque disponível: {item['estoque_disponivel']}"
        )

        validade_lote.value = (
            f"Validade: {item['validade']}"
        )

        item_em_edicao = indice

        produto_dropdown.update()
        lote.update()
        quantidade.update()
        estoque_disponivel.update()
        validade_lote.update()

    def atualizar_lista_itens():

        lista_itens.controls.clear()

        for indice, item in enumerate(itens_saida):

            lista_itens.controls.append(

                card_padrao(

                    content=ft.Container(

                        content=ft.Column(

                            [

                                ft.Text(
                                    f"{item['produto']}",
                                    size=16,
                                    weight=ft.FontWeight.BOLD
                                ),

                                ft.Text(
                                    f"Lote: {item['lote']}"
                                ),

                                ft.Text(
                                    f"Quantidade: {item['quantidade']}"
                                ),

                                ft.Row(

                                    [

                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            tooltip="Editar",
                                            on_click=lambda e,
                                            i=indice:
                                            editar_item(i)
                                        ),

                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            tooltip="Excluir",
                                            on_click=lambda e,
                                            i=indice:
                                            excluir_item(i)
                                        )

                                    ]

                                )

                            ]

                        ),

                        padding=15

                    )

                )

            )    

    def excluir_item(indice):

        itens_saida.pop(indice)

        atualizar_lista_itens()

    def logo_path():

        for path in LOGO_PATHS:

            if path.exists():

                return path

        return None


    def nome_usuario():

        if isinstance(usuario, dict):

            return (
                usuario.get("nome")
                or usuario.get("email")
                or usuario.get("login")
                or "Usuário"
            )

        return "Usuário"


    def gerar_pdf_consulta_saida(e):

        saida = consultar_saida(
            codigo_consulta.value
        )

        if not saida:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Consulte uma saída antes de gerar o PDF.")
            )
            page.snack_bar.open = True
            page.update()
            return

        itens = consultar_itens_saida(
            codigo_consulta.value
        )

        agora_arquivo = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo_pdf = REPORTS_DIR / f"Consulta_Saida_{saida['codigo']}_{agora_arquivo}.pdf"

        doc = SimpleDocTemplate(
            str(arquivo_pdf),
            pagesize=landscape(A4),
            rightMargin=1 * cm,
            leftMargin=1 * cm,
            topMargin=1 * cm,
            bottomMargin=1 * cm
        )

        estilos = getSampleStyleSheet()
        elementos = []

        logo = logo_path()

        cabecalho = []

        if logo:
            try:
                cabecalho.append(
                    Image(str(logo), width=3.0 * cm, height=1.5 * cm)
                )
            except:
                cabecalho.append("")
        else:
            cabecalho.append("")

        cabecalho.append(
            Paragraph(
                "<b>Stock Flow</b><br/>"
                "Consulta de Saída<br/>"
                f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}<br/>"
                f"Gerado por: {nome_usuario()}",
                estilos["Normal"]
            )
        )

        tabela_cabecalho = Table(
            [cabecalho],
            colWidths=[4 * cm, 22 * cm]
        )

        tabela_cabecalho.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                    ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
                    ("PADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        elementos.append(tabela_cabecalho)
        elementos.append(Spacer(1, 10))

        elementos.append(
            Paragraph(
                f"<b>Filtro:</b> Código da saída: {saida['codigo']}",
                estilos["Normal"]
            )
        )

        elementos.append(Spacer(1, 10))

        dados_saida = [
            ["Campo", "Informação"],
            ["Código", saida["codigo"]],
            ["Tipo", saida["tipo"]],
            ["Setor/Destino", saida["setor"]],
            ["Motivo/Observação", saida["motivo"]],
            ["Usuário", saida["usuario"]],
            ["Data", saida["data"]],
        ]

        tabela_dados = Table(
            dados_saida,
            colWidths=[4 * cm, 18 * cm],
            repeatRows=1
        )

        tabela_dados.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
                ]
            )
        )

        elementos.append(
            Paragraph("<b>Dados da Saída</b>", estilos["Heading2"])
        )
        elementos.append(Spacer(1, 8))
        elementos.append(tabela_dados)
        elementos.append(Spacer(1, 14))

        dados_itens = [
            [
                "Produto",
                "Quantidade",
                "Lote"
            ]
        ]

        for item in itens:
            dados_itens.append(
                [
                    str(item["nome"]),
                    str(item["quantidade"]),
                    str(item["lote"]),
                ]
            )

        tabela_itens = Table(
            dados_itens,
            repeatRows=1
        )

        tabela_itens.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("FONTSIZE", (0, 0), (-1, -1), 7),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
                ]
            )
        )

        elementos.append(
            Paragraph("<b>Itens da Saída</b>", estilos["Heading2"])
        )
        elementos.append(Spacer(1, 8))
        elementos.append(tabela_itens)

        doc.build(elementos)

        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"PDF gerado: {arquivo_pdf}")
        )
        page.snack_bar.open = True
        page.update()    

    def buscar_saida(e):

        itens_consulta.controls.clear()

        saida = consultar_saida(
            codigo_consulta.value
        )

        if not saida:

            resultado_consulta.value = (
                "Saída não encontrada."
            )

        else:

            resultado_consulta.value = (

                f"Código: {saida['codigo']}\n"
                f"Tipo: {saida['tipo']}\n"
                f"Setor: {saida['setor']}\n"
                f"Motivo: {saida['motivo']}\n"
            )

            itens = consultar_itens_saida(
                codigo_consulta.value
            )

            itens_consulta.controls.append(

                ft.Text(
                    "Itens da Saída",
                    size=18,
                    weight=ft.FontWeight.BOLD
                )

            )

            for item in itens:

                itens_consulta.controls.append(

                    card_padrao(

                        content=ft.Container(

                            content=ft.Column(

                                [

                                    ft.Text(
                                        f"{item['nome']}",
                                        size=16,
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

                            padding=15

                        )

                    )

                )

        e.page.update()

    def fechar_consulta(e):

        codigo_consulta.value = ""

        resultado_consulta.value = ""

        itens_consulta.controls.clear()

        dialog_consulta.open = False

        e.page.update()

    dialog_consulta = ft.AlertDialog(

        modal=True,

        title=ft.Row(

            [

                ft.Icon(
                    ft.Icons.SEARCH
                ),

                ft.Text(
                    "Consultar Saída"
                )

            ]

        ),

        content=ft.Container(

            content=ft.Column(

                [

                    codigo_consulta,

                    resultado_consulta,

                    ft.Divider(
                        color=VERDE,
                        thickness=1
                    ),

                    ft.Container(

                        content=ft.Row(

                            [

                                ft.Icon(
                                    ft.Icons.OUTBOX
                                ),

                                ft.Text(
                                    "Itens da Saída",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXTO
                                )

                            ]

                        ),

                        padding=10

                    ),

                    itens_consulta

                ],

                scroll=ft.ScrollMode.AUTO

            ),

            width=largura_dialog,
            height=altura_dialog,
            padding=10

        ),

        actions=[

            botao_sucesso(
                "Gerar PDF",
                icon=ft.Icons.PICTURE_AS_PDF,
                on_click=gerar_pdf_consulta_saida
            ),

            botao_primario(
                "Buscar",
                icon=ft.Icons.SEARCH,
                on_click=buscar_saida
            ),

            botao_secundario(
                "Fechar",
                icon=ft.Icons.CLOSE,
                on_click=fechar_consulta
            )

        ]

    )            

    # =========================
    # ADICIONAR ITEM
    # =========================

    def adicionar_item(e):

        mensagem.value = ""

        nonlocal item_em_edicao

        if not quantidade.value:

            mensagem.value = "Informe a quantidade"

            e.page.update()

            return
        
        try:

            qtd = int(quantidade.value)

            if qtd <= 0:

                mensagem.value = (
                    "Quantidade deve ser maior que zero"
                )

                e.page.update()

                return

        except:

            mensagem.value = "Quantidade inválida"

            e.page.update()

            return

        if not produto_dropdown.value:

            mensagem.value = "Selecione um produto"
            e.page.update()
            return
        
        if not lote.value:

            mensagem.value = "Selecione um lote disponível"
            e.page.update()
            return

        lote_selecionado = None

        for item_lote in lotes_produto_atual:

            if lote.value == f"{item_lote['lote']}|{item_lote['validade']}":

                lote_selecionado = item_lote
                break

        if not lote_selecionado:

            mensagem.value = "Lote inválido"
            e.page.update()
            return

        qtd_ja_adicionada = 0

        for indice, item in enumerate(itens_saida):

            if item_em_edicao is not None and indice == item_em_edicao:
                continue

            if (
                item["lote"] == lote_selecionado["lote"]
                and
                item["validade"] == lote_selecionado["validade"]
            ):
                qtd_ja_adicionada += int(item["quantidade"])

        if qtd + qtd_ja_adicionada > lote_selecionado["quantidade"]:

            texto_alerta_estoque.value = (
                "A quantidade informada é maior que o estoque disponível "
                "para este lote.\n\n"
                f"Estoque disponível: {lote_selecionado['quantidade']}\n"
                f"Quantidade solicitada: {qtd + qtd_ja_adicionada}"
            )

            if dialog_alerta_estoque not in e.page.overlay:
                e.page.overlay.append(dialog_alerta_estoque)

            dialog_alerta_estoque.open = True

            e.page.update()
            return

        item = {
            "produto": produto_dropdown.value,
            "lote_ids": lote_selecionado["lote_ids"],
            "lote": lote_selecionado["lote"],
            "validade": lote_selecionado["validade"],
            "estoque_disponivel": lote_selecionado["quantidade"],
            "quantidade": quantidade.value
        }

        if item_em_edicao is not None:

            itens_saida[item_em_edicao] = item

            item_em_edicao = None

        else:

            itens_saida.append(item)

        atualizar_lista_itens()

        produto_dropdown.value = None
        lote.value = ""
        lote.options.clear()
        estoque_disponivel.value = "Estoque disponível: -"
        validade_lote.value = "Validade: -"
        quantidade.value = ""

        e.page.update()

    # =========================
    # CONFIRMAR SAÍDA
    # =========================

    def confirmar_saida(e):

        if dialog_sucesso not in e.page.overlay:
            e.page.overlay.append(dialog_sucesso)

        if len(itens_saida) == 0:

            mensagem.value = "Adicione itens antes"
            e.page.update()
            return

        if not tipo_saida.value:

            mensagem.value = "Selecione o tipo de saída"
            e.page.update()
            return

        codigo = gerar_codigo_saida()

        saida_id = salvar_saida(
            codigo,
            tipo_saida.value,
            destino.value,
            motivo.value,
            "ADMCY"
        )

        for item in itens_saida:

            produto = buscar_produto_por_nome(
                item["produto"]
            )

            if int(item["quantidade"]) > produto["estoque"]:

                mensagem.value = (
                    f"Estoque insuficiente para "
                    f"{produto['nome']}"
                )

                e.page.update()
                return

            produto = buscar_produto_por_nome(
                item["produto"]
            )

            salvar_item_saida(
                saida_id,
                produto["id"],
                item["quantidade"],
                item["lote"]
            )

            baixar_estoque(
                produto["id"],
                int(item["quantidade"])
            )

            baixar_estoque_lotes_agrupados(
                item["lote_ids"],
                int(item["quantidade"])
            )

        dialog_sucesso.title = ft.Text(
            "✔ Saída realizada com sucesso"
        )

        dialog_sucesso.content = ft.Column(
            [
                ft.Text(
                    "Código da Saída",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    codigo,
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        dialog_sucesso.actions = [
            ft.TextButton(
                "OK",
                on_click=fechar_popup,
            )
        ]

        dialog_sucesso.open = True

        e.page.update()

    def fechar_popup(ev):

        dialog_sucesso.open = False

        itens_saida.clear()
        lista_itens.controls.clear()

        item_em_edicao = None

        produto_dropdown.value = None

        lote.value = None
        lote.options.clear()

        estoque_disponivel.value = "Estoque disponível: -"
        validade_lote.value = "Validade: -"

        quantidade.value = ""

        destino.value = ""
        destino.visible = False

        motivo.value = ""
        motivo.visible = False

        tipo_saida.value = None

        mensagem.value = ""

        carregar_produtos()

        page.update()

    # =========================
    # UI
    # =========================

    return ft.Container(

        expand=True,

        bgcolor=BRANCO,

        alignment=ft.Alignment(0, 0),

        padding=15,

        content=ft.Container(
            width=min(largura_util, 1100),
            alignment=ft.Alignment(0, -1),
            content=ft.Column(
                [

            ft.Row(
                [
                    ft.Icon(
                        ft.Icons.OUTBOX,
                        size=34
                    ),

                    ft.Text(
                        "SAÍDA DE PRODUTOS",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=TEXTO
                    )
                ],
                wrap=True,
                spacing=10,
                run_spacing=10,
                alignment=ft.MainAxisAlignment.CENTER
            ),

            ft.Text(
                "Dados da Saída",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=TEXTO
            ),

            tipo_saida,

            botao_primario(
                "Consultar Saída",
                icon=ft.Icons.SEARCH,
                on_click=abrir_consulta
            ),

            ft.Row(
                [
                    destino,

                    botao_primario(
                        "Novo Setor",
                        icon=ft.Icons.ADD,
                        on_click=abrir_setor
                    )
                ],
                wrap=True,
                spacing=10,
                run_spacing=10,
                alignment=ft.MainAxisAlignment.CENTER
            ),

            motivo,


            ft.Divider(
                color=VERDE,
                thickness=1
            ),

            ft.Text(
                "Produtos da Saída",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=TEXTO
            ),

            ft.Row(
                [
                    produto_dropdown,
                    lote
                ],
                wrap=True,
                spacing=10,
                run_spacing=10,
                alignment=ft.MainAxisAlignment.CENTER
            ),

            estoque_disponivel,

            validade_lote,

            ft.Row(
                [
                    quantidade
                ],
                wrap=True,
                spacing=10,
                run_spacing=10,
                alignment=ft.MainAxisAlignment.CENTER
            ),

            botao_primario(
                "Adicionar Item",
                icon=ft.Icons.ADD,
                on_click=adicionar_item
            ),

            ft.Divider(
                color=VERDE,
                thickness=1
            ),

            ft.Container(

                content=ft.Row(

                    [

                        ft.Icon(
                            ft.Icons.LIST_ALT
                        ),

                        ft.Text(
                            "Itens da Saída",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=TEXTO
                        )

                    ]

                ),

                padding=10

            ),

            lista_itens,

            ft.Row(

                [

                    botao_primario(

                        "Confirmar Saída",

                        icon=ft.Icons.SAVE,

                        width=largura_botao,

                        height=50,

                        on_click=confirmar_saida

                    )

                ],

                alignment=ft.MainAxisAlignment.CENTER

            ),

            ft.Divider(
                color=VERDE,
                thickness=1
            ),

            mensagem
                    ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            spacing=10
        )
    )
)