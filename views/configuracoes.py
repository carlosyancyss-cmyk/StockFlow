import flet as ft

from pathlib import Path
from shutil import copy2

from utils.export_manager import url_download
from app_paths import DB_FILE, BACKUPS_DIR
from database.backup_supabase import (
    fazer_backup as fazer_backup_supabase,
    baixar_backup_nuvem
)
from database.restaurar_supabase import restaurar_backup
from database.usuarios_supabase import (
    alterar_senha,
    atualizar_dados_usuario
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


def configuracoes_view(page, usuario, logout_callback=None):

    largura_tela = page.width or 390

    largura_util = max(largura_tela - 30, 300)

    largura_dialog_perfil = min(largura_util, 480)
    largura_dialog_senha = min(largura_util, 450)
    largura_conteudo = min(largura_util, 900)

    # =====================================
    # LOGOUT
    # =====================================

    def fazer_logout(e):

        if logout_callback:
            logout_callback(e)
        

    # =====================================
    # VER PERFIL
    # =====================================

    def abrir_perfil(e):

        nome = ft.TextField(
            label="Nome",
            value=usuario["nome"],
            read_only=True
        )

        telefone = ft.TextField(
            label="Telefone",
            value=usuario["telefone"] or "",
            read_only=True
        )

        email = ft.TextField(
            label="Email",
            value=usuario["email"],
            read_only=True
        )

        perfil = ft.TextField(
            label="Perfil",
            value=usuario["perfil"],
            read_only=True
        )

        status = ft.TextField(
            label="Status",
            value=usuario["status"],
            read_only=True
        )

        cadastro = ft.TextField(
            label="Data de cadastro",
            value=str(usuario["data_cadastro"]),
            read_only=True
        )

        botao_editar = botao_sucesso(
            "Editar",
            icon=ft.Icons.EDIT
        )

        botao_salvar = botao_sucesso(
            "Salvar",
            icon=ft.Icons.SAVE,
            visible=False
        )

        def ativar_edicao(ev):
            nome.read_only = False
            telefone.read_only = False
            email.read_only = False

            botao_editar.visible = False
            botao_salvar.visible = True

            page.update()

        def salvar_perfil(ev):
            if not nome.value or not email.value:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Nome e email são obrigatórios.")
                )
                page.snack_bar.open = True
                page.update()
                return

            sucesso = atualizar_dados_usuario(
                usuario["id"],
                nome.value,
                telefone.value,
                email.value
            )

            if sucesso:
                usuario["nome"] = nome.value
                usuario["telefone"] = telefone.value
                usuario["email"] = email.value

                nome.read_only = True
                telefone.read_only = True
                email.read_only = True

                botao_editar.visible = True
                botao_salvar.visible = False

                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Perfil atualizado com sucesso.")
                )
                page.snack_bar.open = True

            else:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Não foi possível atualizar o perfil.")
                )
                page.snack_bar.open = True

            page.update()

        botao_editar.on_click = ativar_edicao
        botao_salvar.on_click = salvar_perfil

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Meu perfil"),
            content=ft.Container(
                width=largura_dialog_perfil,
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.CircleAvatar(
                                    content=ft.Text(
                                        usuario["nome"][0].upper(),
                                        size=22,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    radius=28
                                ),
                                ft.Column(
                                    [
                                        ft.Text(
                                            usuario["nome"],
                                            size=20,
                                            weight=ft.FontWeight.BOLD
                                        ),
                                        ft.Text(usuario["perfil"])
                                    ],
                                    spacing=2
                                )
                            ],
                            spacing=12,
                            wrap=True,
                            alignment=ft.MainAxisAlignment.CENTER
                        ),

                        ft.Divider(

                        color=VERDE,

                        thickness=1

                        ),

                        nome,
                        telefone,
                        email,
                        perfil,
                        status,
                        cadastro
                    ],
                    spacing=12,
                    tight=True
                )
            ),
            actions=[
                botao_editar,
                botao_salvar,
                botao_secundario(
                "Fechar",
                icon=ft.Icons.CLOSE,
                    on_click=lambda e: fechar_dialog(e, dialog)
                )
            ]
        )

        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    # =====================================
    # FECHAR DIALOG
    # =====================================

    def fechar_dialog(e, dialog):

        dialog.open = False

        page.update()

    # =====================================
    # ALTERAR SENHA
    # =====================================

    def abrir_alterar_senha(e):

        senha_atual = ft.TextField(

            label="Senha atual",

            password=True,

            can_reveal_password=True

        )

        nova_senha = ft.TextField(

            label="Nova senha",

            password=True,

            can_reveal_password=True

        )

        confirmar = ft.TextField(

            label="Confirmar senha",

            password=True,

            can_reveal_password=True

        )

        def salvar(e):

            if senha_atual.value != usuario["senha"]:

                page.snack_bar = ft.SnackBar(

                    content=ft.Text(
                        "Senha atual incorreta."
                    )

                )

                page.snack_bar.open = True

                page.update()

                return

            if nova_senha.value != confirmar.value:

                page.snack_bar = ft.SnackBar(

                    content=ft.Text(
                        "As senhas não coincidem."
                    )

                )

                page.snack_bar.open = True

                page.update()

                return

            alterar_senha(

                usuario["id"],

                nova_senha.value

            )

            dialog.open = False

            page.snack_bar = ft.SnackBar(

                content=ft.Text(
                    "Senha alterada com sucesso."
                )

            )

            page.snack_bar.open = True

            page.update()

        dialog = ft.AlertDialog(

            modal=True,

            title=ft.Text(
                "Alterar Senha"
            ),

            content=ft.Container(

                width=largura_dialog_senha,

                content=ft.Column(

                    [

                        senha_atual,

                        nova_senha,

                        confirmar

                    ]

                )

            ),

            actions=[

                botao_sucesso(
                    "Salvar",
                    icon=ft.Icons.SAVE,
                    on_click=salvar

                ),

                botao_secundario(
                    "Cancelar",
                    icon=ft.Icons.CLOSE,

                    on_click=lambda e: fechar_dialog(
                        e,
                        dialog
                    )

                )

            ]

        )

        page.overlay.append(dialog)

        dialog.open = True

        page.update()

    # =====================================
    # BACKUP
    # =====================================

    def fazer_backup(e):

        try:

            arquivo = fazer_backup_supabase()

            page.launch_url(url_download(arquivo))

            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    f"Backup criado com sucesso!\n{arquivo}"
                )
            )

            page.snack_bar.open = True
            page.update()

        except Exception as erro:

            print("ERRO BACKUP:", erro)

            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    f"Erro ao criar backup:\n{erro}"
                )
            )

            page.snack_bar.open = True
            page.update()

    def restaurar_backup_nuvem(e):

        try:

            arquivo = baixar_backup_nuvem()

            restaurar_backup(arquivo)

            if arquivo.exists():
                arquivo.unlink()

            e.page.show_dialog(
                ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Backup restaurado"),
                    content=ft.Text(
                        "Backup da nuvem restaurado com sucesso!"
                    ),
                    actions=[
                        ft.TextButton(
                            "OK",
                            on_click=lambda e: e.page.pop_dialog()
                        )
                    ]
                )
            )

        except Exception as erro:

            e.page.show_dialog(
                ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Erro"),
                    content=ft.Text(str(erro)),
                    actions=[
                        ft.TextButton(
                            "OK",
                            on_click=lambda e: e.page.pop_dialog()
                        )
                    ]
                )
            )
        

    # =====================================
    # RESTAURAR BACKUP
    # =====================================

    def selecionar_backup(arquivos):

        print("INICIOU RESTAURAÇÃO")

        if not arquivos:
            return

        try:

            restaurar_backup(arquivos[0].path)

            print("MOSTRANDO DIALOG")

            dialog_ok = ft.AlertDialog(
                modal=True,
                title=ft.Text("Sucesso"),
                content=ft.Text("Backup restaurado com sucesso!"),
                actions=[
                    ft.TextButton(
                        "OK",
                        on_click=lambda e: (
                            setattr(dialog_ok, "open", False),
                            page.update()
                        )
                    )
                ]
            )

            page.overlay.append(dialog_ok)

            dialog_ok.open = True

            page.update()

        except Exception as erro:

            print("ERRO RESTAURAR:", erro)

            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    f"Erro ao restaurar:\n{erro}"
                )
            )

            page.snack_bar.open = True
            page.update()

    async def abrir_restauracao(e):

        arquivos = await picker_restaurar.pick_files(
            allow_multiple=False,
            allowed_extensions=["json"]
        )

        if arquivos:
            selecionar_backup(arquivos)  

    # =====================================
    # CARD PADRÃO
    # =====================================

    def card(

        titulo,

        icone,

        funcao

    ):

        return ft.Card(

            content=ft.Container(

                padding=20,

                on_click=funcao,

                border_radius=15,

                content=ft.Row(

                    [

                        ft.Icon(
                            icone,
                            size=30
                        ),

                        ft.Text(
                            titulo,
                            size=18,
                            weight=ft.FontWeight.BOLD
                        )

                    ],
                    wrap=True,
                    spacing=10,
                    run_spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER

                )

            )

        )
    
    picker_restaurar = ft.FilePicker()

    page.services.append(picker_restaurar)

    page.update()


    # =====================================
    # TELA
    # =====================================

    componentes = [

        card_padrao(
            content=ft.Container(
                padding=20,
                border_radius=15,
                content=ft.Row(
                    [
                        ft.CircleAvatar(
                            content=ft.Text(
                                usuario["nome"][0].upper(),
                                size=24,
                                weight=ft.FontWeight.BOLD
                            ),
                            radius=32
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    usuario["nome"],
                                    size=22,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.Row(
                                    [
                                        ft.Container(
                                            padding=ft.Padding(
                                                left=10,
                                                top=4,
                                                right=10,
                                                bottom=4
                                            ),
                                            border_radius=20,
                                            bgcolor=ft.Colors.BLUE_100,
                                            content=ft.Text(
                                                usuario["perfil"],
                                                size=12,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.BLUE_900
                                            )
                                        ),
                                        ft.Container(
                                            padding=ft.Padding(
                                                left=10,
                                                top=4,
                                                right=10,
                                                bottom=4
                                            ),
                                            border_radius=20,
                                            bgcolor=ft.Colors.GREEN_100,
                                            content=ft.Text(
                                                usuario["status"],
                                                size=12,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.GREEN_900
                                            )
                                        )
                                    ],
                                    spacing=8,
                                    wrap=True,
                                    alignment=ft.MainAxisAlignment.CENTER
                                )
                            ],
                            spacing=6
                        )
                    ],
                    spacing=15,
                    run_spacing=10,
                    wrap=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        ),

        card(

            "Ver Perfil",

            ft.Icons.PERSON,

            abrir_perfil

        ),

        card(

            "Alterar Senha",

            ft.Icons.LOCK,

            abrir_alterar_senha

        )

    ]

    # =====================================
    # SOMENTE ADM
    # =====================================

    if usuario["perfil"].upper() in ("ADMINISTRADOR", "GESTOR"):

        componentes.append(

            card(

                "Backup Banco",

                ft.Icons.BACKUP,

                fazer_backup

            )

        )

        componentes.append(

            card(

                "Restaurar Backup",

                ft.Icons.RESTORE,

                abrir_restauracao

            )

        )

        componentes.append(

            card(

                "Restaurar Backup da Nuvem",

                ft.Icons.CLOUD_DOWNLOAD,

                restaurar_backup_nuvem

            )

        )

    componentes.append(

        card(

            "Logout",

            ft.Icons.LOGOUT,

            fazer_logout

        )

    )

    return ft.Container(

        expand=True,

        bgcolor=BRANCO,

        alignment=ft.Alignment(0, 0),

        padding=15,

        content=ft.Container(
            width=largura_conteudo,
            alignment=ft.Alignment(0, -1),
            content=ft.Column(
                componentes,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
                spacing=15
            )
        )
    )