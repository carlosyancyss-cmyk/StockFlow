import flet as ft
import tempfile

import flet
import inspect

print("VERSÃO DO FLET:", flet.__version__)
print("launch_url async:", inspect.iscoroutinefunction(flet.Page.launch_url))

from fastapi.responses import FileResponse
from fastapi import HTTPException
from pathlib import Path
from database.usuarios_supabase import cadastrar_usuario
from database.backup_supabase import fazer_backup_automatico

from database.usuarios_supabase import (
    login_usuario,
    buscar_usuario_ativo_por_email,
    recuperar_senha_usuario
)

from app_paths import APP_DATA_DIR
from views.dashboard import dashboard_view
from views.entradas import entradas_view
from views.saidas import saidas_view
from views.estoque import estoque_view
from views.configuracoes import configuracoes_view
from views.permissoes import permissoes_view
from views.relatorios import relatorios_view
from views.tema import (
    aplicar_tema_page,
    botao_primario,
    botao_secundario
)

ARQUIVO_SESSAO = APP_DATA_DIR / "sessao_login.txt"


def main(page: ft.Page):

    page.title = "Stock Flow"
    aplicar_tema_page(page)
    page.bgcolor = ft.Colors.WHITE


    mensagem = ft.Text(
        color="#2E7D32",
        weight=ft.FontWeight.BOLD
    )

    def salvar_sessao(usuario):

        try:
            ARQUIVO_SESSAO.write_text(
                usuario["email"],
                encoding="utf-8"
            )
        except Exception as erro:
            print("Erro ao salvar sessão:", erro)


    def carregar_sessao():

        try:
            if not ARQUIVO_SESSAO.exists():
                return None

            email = ARQUIVO_SESSAO.read_text(
                encoding="utf-8"
            ).strip()

            if not email:
                return None

            return buscar_usuario_ativo_por_email(email)

        except Exception as erro:
            print("Erro ao carregar sessão:", erro)
            return None


    def limpar_sessao():

        try:
            if ARQUIVO_SESSAO.exists():
                ARQUIVO_SESSAO.unlink()
        except Exception as erro:
            print("Erro ao limpar sessão:", erro)

    def abrir_sistema(usuario):

        page.clean()

        conteudo = ft.Container(

            content=dashboard_view(page, usuario),

            expand=True,

            bgcolor=ft.Colors.WHITE

        )

        def logout(e):

            limpar_sessao()

            page.navigation_bar = None

            mostrar_login()

            page.update()

        def perfil_usuario():
            return usuario["perfil"]

        def pode_ver_entradas():
            return perfil_usuario() in [
                "Administrador",
                "Gestor",
                "Operador"
            ]

        def pode_ver_saidas():
            return perfil_usuario() in [
                "Administrador",
                "Gestor",
                "Operador",
                "Estoquista"
            ]

        def pode_ver_relatorios():
            return perfil_usuario() in [
                "Administrador",
                "Gestor",
                "Operador"
            ]

        def pode_ver_permissoes():
            return perfil_usuario() in [
                "Administrador",
                "Gestor"
            ]

        def pode_ver_configuracoes():
            return perfil_usuario() in [
                "Administrador",
                "Gestor",
                "Operador",
                "Estoquista",
                "Olheiro"
            ]    

        def mais_view(page, usuario, conteudo):

            def abrir_relatorios(e):

                conteudo.content = relatorios_view(
                    page,
                    usuario
                )

                page.update()

            def abrir_configuracoes(e):

                conteudo.content = configuracoes_view(
                    page,
                    usuario,
                    logout
                )

                page.update()

            def abrir_permissoes(e):

                conteudo.content = permissoes_view(
                    page,
                    usuario
                )

                page.update()

            controles = []

            if pode_ver_relatorios():

                controles.append(
                    ft.Card(
                        content=ft.Container(
                            padding=15,
                            content=ft.ListTile(
                                leading=ft.Icon(
                                    ft.Icons.INSERT_CHART
                                ),
                                title=ft.Text(
                                    "Relatórios"
                                ),
                                on_click=abrir_relatorios
                            )
                        )
                    )
                )

            if pode_ver_configuracoes():

                controles.append(
                    ft.Card(
                        content=ft.Container(
                            padding=15,
                            content=ft.ListTile(
                                leading=ft.Icon(
                                    ft.Icons.SETTINGS
                                ),
                                title=ft.Text(
                                    "Configurações"
                                ),
                                on_click=abrir_configuracoes
                            )
                        )
                    )
                )

            if pode_ver_permissoes():

                controles.append(

                    ft.Card(
                        content=ft.Container(
                            padding=15,
                            content=ft.ListTile(
                                leading=ft.Icon(
                                    ft.Icons.ADMIN_PANEL_SETTINGS
                                ),
                                title=ft.Text(
                                    "Permissões"
                                ),
                                on_click=abrir_permissoes
                            )
                        )
                    )

                )

            return ft.Container(
                expand=True,
                padding=15,
                content=ft.Column(
                    controls=controles,
                    scroll=ft.ScrollMode.AUTO
                )
            )  

        def trocar_aba(e):

            indice = e.control.selected_index

            if indice < 0 or indice >= len(abas):
                return

            conteudo.content = abas[indice]["view"]()

            page.update()

        abas = [
            {
                "nome": "Dashboard",
                "icone": ft.Icons.HOME,
                "label": "Início",
                "view": lambda: dashboard_view(page, usuario)
            },
            {
                "nome": "Estoque",
                "icone": ft.Icons.INVENTORY_2,
                "label": "Estoque",
                "view": lambda: estoque_view(page, usuario)
            }
        ]

        if pode_ver_entradas():
            abas.append(
                {
                    "nome": "Entradas",
                    "icone": ft.Icons.MOVE_TO_INBOX,
                    "label": "Entradas",
                    "view": lambda: entradas_view(page, usuario)
                }
            )

        if pode_ver_saidas():
            abas.append(
                {
                    "nome": "Saídas",
                    "icone": ft.Icons.OUTBOX,
                    "label": "Saídas",
                    "view": lambda: saidas_view(page, usuario)
                }
            )

        if (
            pode_ver_relatorios() or
            pode_ver_configuracoes() or
            pode_ver_permissoes()
        ):
            abas.append(
                {
                    "nome": "Mais",
                    "icone": ft.Icons.MENU,
                    "label": "Mais",
                    "view": lambda: mais_view(page, usuario, conteudo)
                }
            )

        destinos = [
            ft.NavigationBarDestination(
                icon=aba["icone"],
                label=aba["label"]
            )
            for aba in abas
        ]

        navegacao = ft.NavigationBar(

            destinations=destinos,

            on_change=trocar_aba,

            selected_index=0,

            bgcolor=ft.Colors.WHITE,

            indicator_color="#1565C0",

            height=72,

            label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW

        )

        page.add(conteudo)


        page.navigation_bar = navegacao

        page.update()


    def mostrar_login():

        page.clean()

        largura_tela = page.width or 390
        largura_card_login = min(max(largura_tela - 30, 300), 500)
        largura_logo = min(max(largura_tela - 80, 220), 320)
        largura_botao = min(max(largura_tela - 80, 220), 280)

        login_email = ft.TextField(
            label="Login",
            prefix_icon=ft.Icons.PERSON
        )

        login_senha = ft.TextField(
            label="Senha",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK
        )

        manter_conectado = ft.Checkbox(
            label="Manter conectado",
            value=False
        )

        nome = ft.TextField(
            label="Nome Completo"
        )

        telefone = ft.TextField(
            label="Telefone"
        )

        email = ft.TextField(
            label="E-mail"
        )

        senha = ft.TextField(
            label="Senha",
            password=True
        )

        email_recuperacao = ft.TextField(
            label="Digite seu e-mail"
        )

        nova_senha_recuperacao = ft.TextField(
            label="Nova senha",
            password=True,
            can_reveal_password=True
        )

        confirmar_senha_recuperacao = ft.TextField(
            label="Confirmar nova senha",
            password=True,
            can_reveal_password=True
        )

        def entrar(e):

            usuario = login_usuario(
                login_email.value,
                login_senha.value
            )

            if usuario:

                if usuario["perfil"] in ("Administrador", "Gestor"):


                    try:

                        fazer_backup_automatico()


                    except Exception as erro:

                        print("ERRO BACKUP AUTOMÁTICO:", erro) 

                if manter_conectado.value:
                    salvar_sessao(usuario)

                abrir_sistema(usuario)

            else:

                page.snack_bar = ft.SnackBar(
                    content=ft.Text(
                        "Usuário ou senha inválidos"
                    )
                )

                page.snack_bar.open = True
                page.update()

        login_senha.on_submit = entrar       

        def solicitar_acesso(e):

            sucesso = cadastrar_usuario(
                nome.value,
                telefone.value,
                email.value,
                senha.value
            )

            if sucesso:

                mensagem.value = (
                    "Solicitação enviada com sucesso!"
                )

                nome.value = ""
                telefone.value = ""
                email.value = ""
                senha.value = ""

                dialog_cadastro.open = False

                page.snack_bar = ft.SnackBar(
                    content=ft.Text(
                        "Solicitação enviada com sucesso!"
                    )
                )

                page.snack_bar.open = True

            else:

                mensagem.value = (
                    "Erro ao solicitar acesso."
                )

            page.update()

        def fechar_recuperacao(e):

            dialog_recuperar.open = False

            page.update()

        def recuperar_senha(e):

            if not email_recuperacao.value:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Informe o e-mail cadastrado.")
                )
                page.snack_bar.open = True
                page.update()
                return

            if not nova_senha_recuperacao.value:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Informe a nova senha.")
                )
                page.snack_bar.open = True
                page.update()
                return

            if nova_senha_recuperacao.value != confirmar_senha_recuperacao.value:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("As senhas não coincidem.")
                )
                page.snack_bar.open = True
                page.update()
                return

            sucesso = recuperar_senha_usuario(
                email_recuperacao.value,
                nova_senha_recuperacao.value
            )

            if sucesso:
                dialog_recuperar.open = False

                email_recuperacao.value = ""
                nova_senha_recuperacao.value = ""
                confirmar_senha_recuperacao.value = ""

                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Senha redefinida com sucesso.")
                )
                page.snack_bar.open = True

            else:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("E-mail não encontrado.")
                )
                page.snack_bar.open = True

            page.update()        

        def fechar_cadastro(e):

            dialog_cadastro.open = False

            page.update()

        dialog_cadastro = ft.AlertDialog(

            modal=True,

            title=ft.Text(
                "Solicitar Acesso"
            ),

            content=ft.Column(
                [
                    nome,
                    telefone,
                    email,
                    senha
                ],
                tight=True
            ),

            actions=[

                botao_secundario(
                    "Cancelar",
                    on_click=fechar_cadastro
                ),

                botao_primario(
                    "Solicitar Acesso",
                    icon=ft.Icons.PERSON_ADD,
                    on_click=solicitar_acesso
                )

            ]

        )

        dialog_recuperar = ft.AlertDialog(

            modal=True,

            title=ft.Text(
                "Recuperar Senha"
            ),

            content=ft.Column(
                [
                    ft.Text(
                        "Informe seu e-mail cadastrado e crie uma nova senha."
                    ),

                    email_recuperacao,

                    nova_senha_recuperacao,

                    confirmar_senha_recuperacao
                ],
                tight=True
            ),

            actions=[

                botao_secundario(
                    "Cancelar",
                    on_click=fechar_recuperacao
                ),

                botao_primario(
                    "Enviar",
                    icon=ft.Icons.SEND,
                    on_click=recuperar_senha
                )

            ]

        )

        page.overlay.append(dialog_cadastro)


        page.overlay.append(dialog_recuperar)

        
        def abrir_cadastro(e):


            page.dialog = dialog_cadastro

            dialog_cadastro.open = True

            page.update() 

        def abrir_recuperacao(e):

            page.dialog = dialog_recuperar

            dialog_recuperar.open = True

            page.update()     

        page.add(

            ft.Container(

                expand=True,

                alignment=ft.Alignment(0, 0),

                content=ft.Column(

                    [

                        ft.Card(

                            elevation=10,

                            content=ft.Container(

                            width=largura_card_login,

                            padding=20,

                                content=ft.Column(

                                    [

                                    ft.Image(
                                        src="/assets/logo.png",
                                        width=largura_logo,
                                        height=160
                                    ),


                                        ft.Text(
                                            "Sistema de Controle de Estoque"
                                        ),

                                        ft.Text(
                                            "Versão 1.0",
                                            italic=True,
                                            size=12
                                        ),

                                        ft.Divider(),

                                        login_email,

                                        login_senha,

                                        manter_conectado,

                                        botao_primario(
                                            "Entrar",
                                            icon=ft.Icons.LOGIN,
                                            on_click=entrar,
                                            width=largura_botao,
                                            height=45
                                        ),

                                        botao_secundario(
                                            "Esqueci minha senha",
                                            icon=ft.Icons.LOCK_RESET,
                                            on_click=abrir_recuperacao,
                                            width=largura_botao,
                                            height=42
                                        ),

                                        botao_secundario(
                                            "Cadastrar-se",
                                            icon=ft.Icons.PERSON_ADD,
                                            on_click=abrir_cadastro,
                                            width=largura_botao,
                                            height=42
                                        ),

                                        mensagem,

                                    ft.Container(
                                        content=ft.Text(
                                            "Created by Carlos Yan",
                                            size=12,
                                            color=ft.Colors.GREY_500,
                                            italic=True
                                        ),
                                        alignment=ft.Alignment(0, 0),
                                        padding=10
                                    )

                                    ],

                                    horizontal_alignment=
                                    ft.CrossAxisAlignment.CENTER

                                )

                            )

                        )

                    ],

                    alignment=ft.MainAxisAlignment.CENTER,

                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                    scroll=ft.ScrollMode.AUTO,
                    expand=True

                )

            )

        )


    usuario_salvo = carregar_sessao()

    if usuario_salvo:
        abrir_sistema(usuario_salvo)
    else:
        mostrar_login()

app = ft.run(
    main,
    assets_dir="assets",
    export_asgi_app=True,
)

TEMP_DIR = Path(tempfile.gettempdir())


@app.get("/download/{arquivo}")
async def download_arquivo(arquivo: str):

    caminho = TEMP_DIR / arquivo

    if not caminho.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    return FileResponse(
        path=caminho,
        filename=arquivo,
    )