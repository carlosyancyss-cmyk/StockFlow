import flet as ft

from database.fornecedores_supabase import (
    cadastrar_fornecedor,
    listar_fornecedores
)

from database.produtos_supabase import (
    cadastrar_produto,
    listar_produtos,
    atualizar_produto_cadastrado,
    excluir_produto,
    buscar_produto_por_nome
)

from database.entradas_supabase import (
    gerar_codigo_entrada,
    salvar_entrada,
    salvar_item_entrada,
    salvar_lote,
    consultar_entrada,
    consultar_itens_entrada
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


from app_paths import REPORTS_DIR, LOGO_PATHS
from datetime import datetime
from pathlib import Path

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

# BASE_DIR = Path(__file__).resolve().parent.parent

# REPORTS_DIR = BASE_DIR / "reports"
# REPORTS_DIR.mkdir(exist_ok=True)

# LOGO_PATHS = [

#    BASE_DIR / "assets" / "logo.png",

#    BASE_DIR / "assets" / "logo" / "logo_nova.png",

#    BASE_DIR / "logo.png"

#]



def entradas_view(page, usuario):

    print("USUARIO RECEBIDO:", usuario)

    largura_tela = page.width or 390
    altura_tela = page.height or 700

    largura_util = max(largura_tela - 30, 300)

    largura_campo_pequeno = min(largura_util, 250)
    largura_campo_medio = min(largura_util, 300)
    largura_campo_grande = min(largura_util, 400)
    largura_campo_total = min(largura_util, 500)

    largura_dialog = min(largura_util, 700)
    altura_dialog = min(max(altura_tela - 180, 350), 500)

    largura_botao = min(largura_util, 300)

    itens_entrada = []

    item_em_edicao = None

    mensagem = ft.Text(
        size=16,
        weight=ft.FontWeight.BOLD,
        color=TEXTO
    )

    codigo_consulta = ft.TextField(
        label="Código da Entrada",
        width=largura_campo_pequeno
    )

    resultado_consulta = ft.Column()

    itens_consulta = ft.Column()

    lista_produtos = ft.Column()
    lista_itens = ft.Column(
        spacing=10
    )

    dialog_sucesso = ft.AlertDialog(
        modal=True
    )

    codigo_text = ft.Text(
        "Código: ---",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=TEXTO
    )

    # =========================
    # FORNECEDORES
    # =========================

    fornecedor = ft.Dropdown(
        label="Fornecedor",
        width=largura_campo_grande,
        visible=False
    )

    origem = ft.Dropdown(
        label="Origem",
        width=largura_campo_grande,
        visible=False,
        options=[]
    )

    numero_nf = ft.TextField(
        label="Número da Nota Fiscal",
        width=largura_campo_pequeno,
        visible=False
    )

    valor_total = ft.TextField(
        label="Valor Total (R$)",
        width=largura_campo_pequeno,
        visible=False
    )

    observacao = ft.TextField(
        label="Observação",
        multiline=True,
        min_lines=3,
        width=largura_campo_total,
        visible=False
    )

    nome_fornecedor = ft.TextField(
        label="Nome do Fornecedor"
    )

    cnpj_fornecedor = ft.TextField(
        label="CNPJ"
    )

    nome_instituicao = ft.TextField(
        label="Nome da Instituição",
        visible=False
    )

    def alterar_tipo_cadastro(e):

        if tipo_cadastro.value == "Fornecedor":

            nome_fornecedor.visible = True
            cnpj_fornecedor.visible = True
            nome_instituicao.visible = False

        elif tipo_cadastro.value == "Instituição":

            nome_fornecedor.visible = False
            cnpj_fornecedor.visible = False
            nome_instituicao.visible = True

        e.page.update()

    tipo_cadastro = ft.Dropdown(
        label="Tipo",
        width=largura_campo_medio,
        options=[
            ft.dropdown.Option("Fornecedor"),
            ft.dropdown.Option("Instituição")
        ],
        on_select=alterar_tipo_cadastro
    )


    # =========================
    # PRODUTOS
    # =========================

    produtos_db = listar_produtos()

    produto_dropdown = ft.Dropdown(
        label="Produto",
        width=largura_campo_grande,
        options=[
            ft.dropdown.Option(p["nome"])
            for p in produtos_db
        ]
    )

    def formatar_validade(e):

        texto = "".join(
            c for c in e.control.value if c.isdigit()
        )

        if len(texto) > 8:
            texto = texto[:8]

        if len(texto) >= 5:

            texto = (
                texto[:2] + "/" +
                texto[2:4] + "/" +
                texto[4:]
            )

        elif len(texto) >= 3:

            texto = (
                texto[:2] + "/" +
                texto[2:]
            )

        e.control.value = texto

        e.page.update()

    def validar_data(data):

        try:

            dia, mes, ano = data.split("/")

            dia = int(dia)
            mes = int(mes)
            ano = int(ano)

            if dia < 1 or dia > 31:
                return False

            if mes < 1 or mes > 12:
                return False

            if ano < 2000:
                return False

            return True

        except:
            return False    

    lote = ft.TextField(label="Lote", width=largura_campo_pequeno)
    validade = ft.TextField(
    label="Validade",
    width=largura_campo_pequeno,
    hint_text="dd/mm/aaaa",
    on_change=formatar_validade
)
    quantidade = ft.TextField(label="Quantidade", width=largura_campo_pequeno)

    valor_unitario = ft.TextField(
        label="Valor Unitário",
        width=largura_campo_pequeno,
        visible=False
    )

    nome_produto = ft.TextField(
        label="Nome do Produto",
        width=largura_campo_grande,
    )

    unidade = ft.Dropdown(
        label="Unidade",
        width=largura_campo_pequeno,
        options=[
            ft.dropdown.Option("UN"),
            ft.dropdown.Option("CX"),
            ft.dropdown.Option("PCT"),
            ft.dropdown.Option("FR"),
            ft.dropdown.Option("ML"),
            ft.dropdown.Option("L"),
            ft.dropdown.Option("KG"),
            ft.dropdown.Option("G"),
        ]
    )

    estoque_minimo = ft.TextField(
        label="Estoque Mínimo",
        width=largura_campo_pequeno
    )

    tabela_produtos = ft.DataTable(

        columns=[

            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Produto")),
            ft.DataColumn(ft.Text("Unidade")),
            ft.DataColumn(ft.Text("Estoque Mínimo"))

        ],

        rows=[]

    )

    # =========================
    # FUNÇÕES
    # =========================

    def carregar_fornecedores():

        fornecedores = listar_fornecedores()

        opcoes = [
            ft.dropdown.Option(f["nome"])
            for f in fornecedores
        ]

        fornecedor.options = opcoes
        origem.options = opcoes

    def salvar_fornecedor(e):

        if tipo_cadastro.value == "Fornecedor":

            if not nome_fornecedor.value:
                mensagem.value = "Informe o nome do fornecedor."
                e.page.update()
                return

            sucesso = cadastrar_fornecedor(
                nome_fornecedor.value,
                cnpj_fornecedor.value if cnpj_fornecedor.value else None
            )

            texto_sucesso = "Fornecedor cadastrado."
            texto_erro = "Erro ao cadastrar fornecedor."

        elif tipo_cadastro.value == "Instituição":

            if not nome_instituicao.value:
                mensagem.value = "Informe o nome da instituição."
                e.page.update()
                return

            sucesso = cadastrar_fornecedor(
                nome_instituicao.value,
                None
            )

            texto_sucesso = "Instituição cadastrada."
            texto_erro = "Erro ao cadastrar instituição."

        else:

            mensagem.value = "Selecione o tipo de cadastro."
            e.page.update()
            return

        if sucesso:

            carregar_fornecedores()

            nome_fornecedor.value = ""
            cnpj_fornecedor.value = ""
            nome_instituicao.value = ""
            tipo_cadastro.value = None

            dialog.open = False

            mensagem.value = texto_sucesso

        else:

            mensagem.value = texto_erro

        e.page.update()

    def fechar_fornecedor(e):

        nome_fornecedor.value = ""
        cnpj_fornecedor.value = ""
        nome_instituicao.value = ""
        tipo_cadastro.value = None

        dialog.open = False

        e.page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Novo Fornecedor - Instituição"),
        content=ft.Column(
            [
                tipo_cadastro,
                nome_fornecedor,
                cnpj_fornecedor,
                nome_instituicao
            ],
            tight=True
        ),
        actions=[

            botao_secundario(
                "Cancelar",
                icon=ft.Icons.CLOSE,
                on_click=fechar_fornecedor
            ),

            botao_sucesso(
                "Salvar",
                icon=ft.Icons.SAVE,
                on_click=salvar_fornecedor
            )

        ]
    )

    def buscar_entrada(e):

        itens_consulta.controls.clear()

        entrada = consultar_entrada(
            codigo_consulta.value
        )

        if not entrada:

            resultado_consulta.value = (
                "Entrada não encontrada."
            )

        else:

            resultado_consulta.controls.clear()

            resultado_consulta.controls.append(

                card_padrao(

                    content=ft.Column(

                            [

                                ft.Text(
                                    f"Código: {entrada['codigo']}",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXTO
                                ),

                                ft.Text(
                                    f"Tipo: {entrada['tipo']}"
                                ),

                                ft.Text(
                                    f"Fornecedor: {entrada['fornecedor']}"
                                ),

                                ft.Text(
                                    f"NF: {entrada['numero_nf']}"
                                ),

                                ft.Text(
                                    f"Valor Total: R$ {entrada['valor_total']}"
                                ),

                                ft.Text(
                                    f"Data: {entrada['data']}"
                                )

                            ],
                            spacing=10

                    ),


                )

            )

            itens = consultar_itens_entrada(
                codigo_consulta.value
            )

            for item in itens:

                itens_consulta.controls.append(

                    card_padrao(

                        content=ft.Container(

                            content=ft.Column(

                                [

                                    ft.Text(
                                        f"{item['nome']}",
                                        size=18,
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
                                    ),

                                    ft.Text(
                                        f"Valor Unitário: R$ {item['valor_unitario']}"
                                    )

                                ],
                                spacing=10

                            ),

                        )

                    )

                )

        e.page.update()

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

    def gerar_pdf_consulta_entradas(e):

        entrada = consultar_entrada(
            codigo_consulta.value
        )

        if not entrada:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Consulte uma entrada antes de gerar o PDF.")
            )
            page.snack_bar.open = True
            page.update()
            return

        itens = consultar_itens_entrada(
            codigo_consulta.value
        )

        agora_arquivo = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo_pdf = REPORTS_DIR / f"Consulta_Entrada_{entrada['codigo']}_{agora_arquivo}.pdf"

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
                "Consulta de Entrada<br/>"
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
                f"<b>Filtro:</b> Código da entrada: {entrada['codigo']}",
                estilos["Normal"]
            )
        )

        elementos.append(Spacer(1, 10))

        dados_entrada = [
            ["Campo", "Informação"],
            ["Código", entrada["codigo"]],
            ["Tipo", entrada["tipo"]],
            ["Fornecedor", entrada["fornecedor"]],
            ["Origem", entrada["origem"]],
            ["NF", entrada["numero_nf"]],
            ["Valor Total", f"R$ {entrada['valor_total']}"],
            ["Usuário", entrada["usuario"]],
            ["Data", entrada["data"]],
        ]

        tabela_dados = Table(
            dados_entrada,
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
            Paragraph("<b>Dados da Entrada</b>", estilos["Heading2"])
        )
        elementos.append(Spacer(1, 8))
        elementos.append(tabela_dados)
        elementos.append(Spacer(1, 14))

        dados_itens = [
            [
                "Produto",
                "Quantidade",
                "Lote",
                "Validade",
                "Valor Unit."
            ]
        ]

        for item in itens:
            dados_itens.append(
                [
                    str(item["nome"]),
                    str(item["quantidade"]),
                    str(item["lote"]),
                    str(item["validade"]),
                    f"R$ {item['valor_unitario']}",
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
            Paragraph("<b>Itens da Entrada</b>", estilos["Heading2"])
        )
        elementos.append(Spacer(1, 8))
        elementos.append(tabela_itens)

        doc.build(elementos)

        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"PDF gerado: {arquivo_pdf}")
        )
        page.snack_bar.open = True
        page.update()  

    def fechar_consulta(e):

        resultado_consulta.controls.clear()

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
                    "Consultar Entrada"
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
                                    ft.Icons.INVENTORY
                                ),

                                ft.Text(
                                    "Itens da Entrada",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=AZUL
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
                on_click=gerar_pdf_consulta_entradas
            ),

            botao_primario(
                "Buscar",
                icon=ft.Icons.SEARCH,
                on_click=buscar_entrada
            ),

            botao_secundario(
                "Fechar",
                icon=ft.Icons.CLOSE,
                on_click=fechar_consulta
            )

        ]

    )

    def abrir_fornecedor(e):

        if dialog not in e.page.overlay:
            e.page.overlay.append(dialog)

        dialog.open = True
        e.page.update()

    def abrir_consulta(e):

        if dialog_consulta not in e.page.overlay:

            e.page.overlay.append(
                dialog_consulta
            )

        dialog_consulta.open = True

        e.page.update()

    def abrir_produto(e):

        if dialog_produto not in e.page.overlay:

            e.page.overlay.append(
                dialog_produto
            )

        dialog_produto.open = True

        e.page.update()

    tabela_produtos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Produto")),
            ft.DataColumn(ft.Text("Unidade")),
            ft.DataColumn(ft.Text("Estoque Mínimo"))
        ],
        rows=[]
    )            

    def alterar_tipo_entrada(e):

        print("EXECUTOU")
        print("VALOR:", e.control.value)

        fornecedor.visible = False
        origem.visible = False
        numero_nf.visible = False
        valor_total.visible = False
        valor_unitario.visible = False
        observacao.visible = False

        if e.control.value == "Nota Fiscal":

            fornecedor.visible = True
            numero_nf.visible = True
            valor_total.visible = True
            valor_unitario.visible = True

            print("FORNECEDOR:", fornecedor.visible)
            print("NF:", numero_nf.visible)
            print("VALOR TOTAL:", valor_total.visible)
            print("VALOR UNITARIO:", valor_unitario.visible)

        elif e.control.value == "Empréstimo":

            origem.label = "Origem do Empréstimo"
            origem.visible = True

        elif e.control.value == "Doação":

            origem.label = "Origem da Doação"
            origem.visible = True

        elif e.control.value == "Inventário":

            observacao.visible = True

        elif e.control.value == "Ajuste de Estoque":

            observacao.visible = True    

        e.page.update()


    tipo_entrada = ft.Dropdown(
        label="Tipo de Entrada",
        width=largura_campo_medio,
        options=[
            ft.dropdown.Option("Nota Fiscal"),
            ft.dropdown.Option("Empréstimo"),
            ft.dropdown.Option("Doação"),
            ft.dropdown.Option("Inventário"),
            ft.dropdown.Option("Ajuste de Estoque")
        ],
        on_select=alterar_tipo_entrada
    )

    print(dir(tipo_entrada))

    print("EVENTO ATRIBUIDO")

    editar_nome_produto = ft.TextField(
        label="Nome do Produto"
    )

    editar_unidade_produto = ft.TextField(
        label="Unidade"
    )

    editar_estoque_minimo_produto = ft.TextField(
        label="Estoque Mínimo"
    )

    produto_editando_id = None
    produto_excluindo_id = None

    tabela_produtos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Produto")),
            ft.DataColumn(ft.Text("Unidade")),
            ft.DataColumn(ft.Text("Estoque Mínimo")),
            ft.DataColumn(ft.Text("Ações"))
        ],
        rows=[]
    )


    def carregar_produtos():

        lista_produtos.controls.clear()

        produtos = listar_produtos()

        if not produtos:

            lista_produtos.controls.append(
                ft.Text("Nenhum produto cadastrado.")
            )

            return

        for p in produtos:

            lista_produtos.controls.append(
                card_padrao(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    p["nome"],
                                    size=18,
                                    weight=ft.FontWeight.BOLD
                                ),

                                ft.Text(
                                    f"Unidade: {p['unidade_medida']}"
                                ),

                                ft.Text(
                                    f"Estoque mínimo: {p['estoque_minimo']}"
                                ),

                                botao_secundario(
                                    "Excluir",
                                    icon=ft.Icons.DELETE,
                                    on_click=lambda e, pid=p["id"]: excluir_produto(pid)
                                )
                            ],
                            spacing=10
                        ),
                    )
                )
            )

    def salvar_edicao_produto(e):

        sucesso = atualizar_produto_cadastrado(

            produto_editando_id,

            editar_nome_produto.value,

            editar_unidade_produto.value,

            int(editar_estoque_minimo_produto.value)

        )

        if sucesso:

            carregar_tabela_produtos()

            dialog_editar_produto.open = False

            e.page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    "Produto atualizado com sucesso!"
                )
            )

            e.page.snack_bar.open = True

        else:

            e.page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    "Erro ao atualizar produto!"
                )
            )

            e.page.snack_bar.open = True

        e.page.update()       

    dialog_editar_produto = ft.AlertDialog(

        modal=True,

        title=ft.Text("Editar Produto"),

        content=ft.Column(
            [
                editar_nome_produto,
                editar_unidade_produto,
                editar_estoque_minimo_produto
            ],
            tight=True
        ),

        actions=[

            botao_secundario(
                "Cancelar",
                icon=ft.Icons.CLOSE,
                on_click=lambda e: (
                    setattr(dialog_editar_produto, "open", False),
                    e.page.update()
                )
            ),

            botao_sucesso(
                "Salvar",
                icon=ft.Icons.SAVE,
                on_click=salvar_edicao_produto
            )

        ]

    ) 

    def confirmar_exclusao_produto(e):

        print("ID que será excluído:", produto_excluindo_id)
        print("ENTROU EM confirmar_exclusao_produto")
        print("ID:", produto_excluindo_id)

        sucesso = excluir_produto(produto_excluindo_id)

        if sucesso is False:
            e.page.snack_bar = ft.SnackBar(
                content=ft.Text("Erro ao excluir produto.")
            )
        else:
            carregar_tabela_produtos()
            carregar_produtos()   # atualiza o dropdown também

            e.page.snack_bar = ft.SnackBar(
                content=ft.Text("Produto excluído com sucesso.")
            )

        e.page.snack_bar.open = True

        dialog_excluir_produto.open = False

        e.page.update()

    dialog_excluir_produto = ft.AlertDialog(

        modal=True,

        title=ft.Text(
            "Excluir Produto"
        ),

        content=ft.Text(
            "Deseja realmente excluir este produto?"
        ),

        actions=[

            botao_secundario(
                "Cancelar",
                icon=ft.Icons.CLOSE,
                on_click=lambda e: (
                    setattr(dialog_excluir_produto, "open", False),
                    e.page.update()
                )
            ),

            botao_sucesso(
                "Excluir",
                icon=ft.Icons.DELETE,
                on_click=confirmar_exclusao_produto
            )

        ]

    )       

    def editar_produto_cadastrado(e, produto):

        nonlocal produto_editando_id

        produto_editando_id = produto["id"]

        editar_nome_produto.value = produto["nome"]

        editar_unidade_produto.value = produto["unidade_medida"]

        editar_estoque_minimo_produto.value = str(
            produto["estoque_minimo"]
        )

        if dialog_editar_produto not in e.page.overlay:
            e.page.overlay.append(
                dialog_editar_produto
            )

        dialog_editar_produto.open = True

        e.page.update()

    def excluir_produto_cadastrado(e, produto):

        print("PRODUTO:", produto)
        print("ID:", produto["id"])

        nonlocal produto_excluindo_id

        produto_excluindo_id = produto["id"]

        print("ID armazenado:", produto_excluindo_id)

        if dialog_excluir_produto not in e.page.overlay:
            e.page.overlay.append(dialog_excluir_produto)

        dialog_excluir_produto.open = True

        e.page.update()                

    def carregar_tabela_produtos():

        tabela_produtos.rows.clear()

        produtos = listar_produtos()

        for p in produtos:

            tabela_produtos.rows.append(

                ft.DataRow(

                    cells=[

                        ft.DataCell(
                            ft.Text(str(p["id"]))
                        ),

                        ft.DataCell(
                            ft.Text(p["nome"])
                        ),

                        ft.DataCell(
                            ft.Text(p["unidade_medida"])
                        ),

                        ft.DataCell(
                            ft.Text(str(p["estoque_minimo"]))
                        ),

                        ft.DataCell(

                            ft.Row(

                                [

                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        tooltip="Editar",
                                        on_click=lambda e, produto=p:
                                            editar_produto_cadastrado(e, produto)
                                    ),

                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        tooltip="Excluir",
                                        on_click=lambda e, produto=p:
                                            excluir_produto_cadastrado(e, produto)
                                    )

                                ]

                            )

                        )

                    ]

                )

            )        

    def atualizar_total_nf():

        total = 0

        for item in itens_entrada:

            try:

                valor = float(
                    str(item["valor"]).replace(",", ".")
                )

                qtd = int(item["quantidade"])

                total += valor * qtd

            except:

                pass

        valor_total.value = f"{total:.2f}"        

    def atualizar_lista_itens():

        lista_itens.controls.clear()

        for indice, item in enumerate(itens_entrada):

            lista_itens.controls.append(

                card_padrao(

                    content=ft.Container(

                        content=ft.Column(

                            [

                                ft.Text(
                                    f"{item['produto']}",
                                    size=18,
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

                            ],
                            spacing=10

                        ),

                    )

                )

            )

    def excluir_item(indice):

        itens_entrada.pop(indice)

        atualizar_lista_itens()

        atualizar_total_nf()

    def editar_item(indice):

        item = itens_entrada[indice]

        produto_dropdown.value = item["produto"]
        lote.value = item["lote"]
        validade.value = item["validade"]
        quantidade.value = item["quantidade"]
        valor_unitario.value = item["valor"]

        itens_entrada.pop(indice)

        atualizar_lista_itens()

        atualizar_total_nf() 
                            

    def adicionar_item(e):

        if not produto_dropdown.value:
            mensagem.value = "Selecione um produto"
            e.page.update()
            return

        if valor_unitario.value and quantidade.value:

            total_atual = 0

            for item_existente in itens_entrada:

                valor = float(
                    str(item_existente["valor"]).replace(",", ".")
                )

                qtd = int(item_existente["quantidade"])

                total_atual += valor * qtd

            valor_novo = float(
                valor_unitario.value.replace(",", ".")
            )

            qtd_nova = int(quantidade.value)

            total_atual += valor_novo * qtd_nova

            valor_total.value = f"{total_atual:.2f}"

        item = {
            "produto": produto_dropdown.value,
            "lote": lote.value,
            "validade": validade.value,
            "quantidade": quantidade.value,
            "valor": valor_unitario.value
        }

        itens_entrada.append(item)

        atualizar_total_nf()

        atualizar_lista_itens()

        produto_dropdown.value = None
        lote.value = ""
        validade.value = ""
        quantidade.value = ""
        valor_unitario.value = ""

        e.page.update()
        
    def confirmar_entrada(e):

        if not tipo_entrada.value:

            mensagem.value = "Selecione o tipo de entrada"

            e.page.update()

            return
        
        if tipo_entrada.value == "Nota Fiscal":

            if not fornecedor.value:

                mensagem.value = "Selecione o fornecedor"

                e.page.update()

                return

            if not numero_nf.value:

                mensagem.value = "Informe o número da NF"

                e.page.update()

                return
            
        if tipo_entrada.value in ["Empréstimo", "Doação"]:

            if not origem.value:

                mensagem.value = "Selecione a instituição ou fornecedor de origem"

                e.page.update()

                return

        if len(itens_entrada) == 0:

            mensagem.value = "Adicione itens primeiro"

            e.page.update()

            return

        codigo = gerar_codigo_entrada()

        entrada_id = salvar_entrada(
            codigo,
            tipo_entrada.value,
            fornecedor.value if fornecedor.value else "",
            origem.value if origem.value else "",
            numero_nf.value,
            valor_total.value,
            "ADMCY"
        )

        for item in itens_entrada:

            produto = buscar_produto_por_nome(
                item["produto"]
            )

            salvar_item_entrada(
                entrada_id,
                produto["id"],
                item["quantidade"],
                item["lote"],
                item["validade"],
                item["valor"]
            )

            salvar_lote(
                produto["id"],
                item["lote"],
                item["validade"],
                item["quantidade"]
            )

        def fechar_popup(ev):

            dialog_sucesso.open = False

            # limpa formulário
            itens_entrada.clear()
            lista_itens.controls.clear()

            tipo_entrada.value = None

            fornecedor.value = None
            fornecedor.visible = False

            origem.value = None
            origem.visible = False

            numero_nf.value = ""

            valor_total.value = ""

            mensagem.value = ""

            carregar_fornecedores()
            carregar_produtos()

            fornecedor.update()
            origem.update()
            tipo_entrada.update()
            numero_nf.update()
            valor_total.update()

            tipo_entrada.focus()

            e.page.update()
            
        dialog_sucesso.title = ft.Text("✔ Entrada realizada com sucesso")

        dialog_sucesso.content = ft.Column(
            [
                ft.Text(
                    "Código da Entrada",
                    text_align=ft.TextAlign.CENTER,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    codigo,
                    text_align=ft.TextAlign.CENTER,
                    size=24,
                    weight=ft.FontWeight.BOLD,
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

        if dialog_sucesso not in e.page.overlay:
            e.page.overlay.append(dialog_sucesso)

        dialog_sucesso.open = True

        e.page.update()

    def salvar_produto(e):

        sucesso = cadastrar_produto(
            nome_produto.value,
            unidade.value,
            estoque_minimo.value
        )

        if sucesso:

            carregar_produtos()

            mensagem.value = "Produto salvo!"

            dialog_produto.open = False

        else:

            mensagem.value = "Produto já cadastrado."

        e.page.update()   

    def fechar_produto(e):

        nome_produto.value = ""
        unidade.value = None
        estoque_minimo.value = ""

        dialog_produto.open = False

        e.page.update()

    def consultar_produtos(e):

        carregar_tabela_produtos()

        if dialog_produtos not in e.page.overlay:
            e.page.overlay.append(dialog_produtos)

        dialog_produtos.open = True

        e.page.update()       

    dialog_produto = ft.AlertDialog(

            modal=True,

            title=ft.Text(
                "Novo Produto"
            ),

            content=ft.Column(

                [

                    nome_produto,
                    unidade,
                    estoque_minimo

                ],

                tight=True

            ),

            actions=[

                botao_primario(
                    "Consultar Produtos",
                    icon=ft.Icons.SEARCH,
                    on_click=consultar_produtos
                ),

                botao_secundario(
                    "Cancelar",
                    icon=ft.Icons.CLOSE,
                    on_click=fechar_produto
                ),

                botao_sucesso(
                    "Salvar",
                    icon=ft.Icons.SAVE,
                    on_click=salvar_produto
                )

            ]

        )
    
    dialog_produtos = ft.AlertDialog(

        modal=True,

        title=ft.Text("Produtos Cadastrados"),

        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            tabela_produtos
                        ],
                        scroll=ft.ScrollMode.AUTO
                    )
                ],
                scroll=ft.ScrollMode.AUTO
            ),
            width=largura_dialog,
            height=min(altura_dialog, 400)
        ),

        actions=[

            botao_secundario(
                "Fechar",
                icon=ft.Icons.CLOSE,
                on_click=lambda e: (
                    setattr(dialog_produtos, "open", False),
                    e.page.update()
                )
            )

        ]

    )

    carregar_fornecedores()
    carregar_produtos()

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
            ft.Container(

            content=ft.Row(
                [

                    ft.Icon(
                        ft.Icons.INVENTORY
                    ),
                    
                    ft.Text(
                        "ENTRADA DE PRODUTOS",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=TEXTO
                    )
                ],
                wrap=True,
                alignment=ft.MainAxisAlignment.CENTER
            ),

            padding=15

        ),

            ft.Text(
                "Dados da Entrada",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=TEXTO
            ),

            tipo_entrada,

            ft.Row(

                [

                    fornecedor,
                    origem

                ],

                wrap=True,
                spacing=10,
                run_spacing=10,
                alignment=ft.MainAxisAlignment.CENTER

            ),

            ft.Container(

                content=ft.Row(

                    [

                        botao_primario(
                            "Novo Fornecedor - Instituição",
                            icon=ft.Icons.ADD,
                            on_click=abrir_fornecedor
                        ),

                        botao_primario(
                            "Novo Produto",
                            icon=ft.Icons.ADD,
                            on_click=abrir_produto
                        ),

                        botao_primario(
                            "Consultar Entrada",
                            icon=ft.Icons.SEARCH,
                            on_click=abrir_consulta
                        )

                    ],

                        wrap=True,
                        spacing=10,
                        run_spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER

                ),

                padding=10

            ),


            ft.Divider(
                color=VERDE,
                thickness=1
            ),

            ft.Row(

                [

                    numero_nf,
                    valor_total

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

                ft.Text(
                    "Dados do Produto",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=TEXTO
                ),

            observacao,

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

            ft.Row(

                [

                    validade,
                    quantidade,
                    valor_unitario

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
                                "Itens da Entrada",
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

                        "Confirmar Entrada",

                        icon=ft.Icons.SAVE,

                        height=50,

                        width=largura_botao,

                        on_click=confirmar_entrada

                    )

                ],

                alignment=ft.MainAxisAlignment.CENTER

            ),

            ft.Divider(
                color=VERDE,
                thickness=1
            ),

            mensagem,

            ft.Divider(
                color=VERDE,
                thickness=1
            ),

            #ft.Text("CADASTRO PRODUTOS"),

            #nome_produto,
            #unidade,
            #estoque_minimo,

            #ft.Button(
            #    "Salvar Produto",
            #    on_click=salvar_produto
            #),

            #ft.Divider(),

            #lista_produtos
                   ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            spacing=ESPACAMENTO
        )
    )
)

