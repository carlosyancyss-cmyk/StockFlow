import flet as ft

from database.usuarios_supabase import (
    listar_usuarios,
    atualizar_perfil_usuario,
    atualizar_status_usuario
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


def permissoes_view(page, usuario_logado):


    conteudo = ft.Column(
        spacing=18,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )


    def salvar_alteracoes(e, usuario_id, perfil_dropdown, status_dropdown):
        atualizar_perfil_usuario(usuario_id, perfil_dropdown.value)
        atualizar_status_usuario(usuario_id, status_dropdown.value)

        page.show_dialog(
            ft.AlertDialog(
                title=ft.Text("Permissões atualizadas"),
                content=ft.Text("As alterações da conta foram salvas com sucesso."),
                actions=[
                    ft.Button(
                        "OK",
                        on_click=lambda ev: page.pop_dialog()
                    )
                ]
            )
        )

        carregar()
        page.update()

    def carregar():
        conteudo.controls.clear()

        conteudo.controls.append(

            card_padrao(

                content=ft.Container(

                    expand=True,

                    padding=25,

                    content=ft.Column(

                        [

                            ft.Text(

                                "PERMISSÕES",

                                size=32,

                                weight=ft.FontWeight.BOLD,
                                color=TEXTO

                            ),

                            ft.Text(

                                "Gerenciamento de usuários do sistema",

                                size=18,
                                color=TEXTO

                            ),

                            ft.Divider(
                                color=VERDE,
                                thickness=1
                            ),

                            ft.Text(

                                f"{usuario_logado['nome']}",

                                size=18,

                                weight=ft.FontWeight.BOLD

                            ),

                            ft.Text(

                                f"Perfil: {usuario_logado['perfil']}",

                                size=16

                            )

                        ],

                        horizontal_alignment=ft.CrossAxisAlignment.CENTER

                    )

                )

            )

        )

        perfil_logado = usuario_logado["perfil"]

        usuarios = listar_usuarios()

        if perfil_logado == "Gestor":
            usuarios = [
                usuario for usuario in usuarios
                if usuario["perfil"] != "Administrador"
            ]

        if not usuarios:
            conteudo.controls.append(

                ft.Container(

                    padding=20,

                    content=ft.Column(

                        [

                            ft.Icon(

                                ft.Icons.PEOPLE_ALT,

                                size=60

                            ),

                            ft.Text(

                                "Nenhuma conta cadastrada.",

                                size=18,

                                weight=ft.FontWeight.BOLD,
                                color=TEXTO

                            )

                        ],

                        horizontal_alignment=ft.CrossAxisAlignment.CENTER

                    )

                )

            )
            return

        for usuario in usuarios:
            opcoes_perfil = [
                ft.dropdown.Option("Gestor"),
                ft.dropdown.Option("Operador"),
                ft.dropdown.Option("Estoquista"),
                ft.dropdown.Option("Olheiro"),
            ]

            if perfil_logado == "Administrador":
                opcoes_perfil.insert(0, ft.dropdown.Option("Administrador"))

            perfil_dropdown = ft.Dropdown(

                width=260,

                label="Perfil",

                value=usuario["perfil"] or "Operador",
                options=opcoes_perfil
            )

            status_dropdown = ft.Dropdown(

                width=220,

                label="Status",

                value=usuario["status"] or "PENDENTE",
                options=[
                    ft.dropdown.Option("ATIVO"),
                    ft.dropdown.Option("PENDENTE"),
                    ft.dropdown.Option("DESABILITADO"),
                ]
            )

            card_usuario = ft.Card(

                elevation=5,

                content=ft.Container(

                    expand=True,

                    padding=25,
                    content=ft.Column(
                        spacing=15,
                        controls=[
                            ft.Row(

                                wrap=True,

                                spacing=20,

                                run_spacing=20,

                                alignment=ft.MainAxisAlignment.CENTER,

                                controls=[
                                    ft.Column(
                                        spacing=6,
                                        controls=[
                                            ft.Text(
                                                usuario["nome"],
                                                size=20,
                                                weight=ft.FontWeight.BOLD
                                            ),
                                            ft.Text(usuario["email"]),
                                            ft.Text(f"Telefone: {usuario['telefone'] or 'Não informado'}"),
                                            ft.Text(f"Cadastrado em: {usuario['data_cadastro'] or 'Não informado'}"),
                                        ]
                                    ),
                                    ft.Container(

                                        width=160,

                                        height=50,

                                        padding=10,

                                        alignment=ft.Alignment(0, 0),

                                        bgcolor=(

                                            ft.Colors.GREEN_100
                                            if usuario["status"] == "ATIVO"
                                            else ft.Colors.RED_100
                                            if usuario["status"] == "DESABILITADO"
                                            else ft.Colors.ORANGE_100
                                        ),
                                        border_radius=8,
                                        content=ft.Text(

                                            usuario["status"],

                                            size=16,

                                            weight=ft.FontWeight.BOLD

                                        )
                                    )
                                ]
                            ),

                            ft.Row(

                                wrap=True,

                                spacing=15,

                                run_spacing=15,

                                alignment=ft.MainAxisAlignment.CENTER,

                                controls=[

                                    perfil_dropdown,
                                    status_dropdown,
                                    botao_primario(

                                        "Salvar Alterações",

                                        icon=ft.Icons.SAVE,

                                        width=220,

                                        height=50,
                                        on_click=lambda e, uid=usuario["id"], p=perfil_dropdown, s=status_dropdown: salvar_alteracoes(e, uid, p, s)
                                    )
                                ]
                            )
                        ]
                    )
                )
            )

            conteudo.controls.append(

                ft.Container(

                    content=card_usuario,

                    margin=10

                )

            )

    carregar()

    return ft.Container(

        expand=True,

        bgcolor=BRANCO,

        alignment=ft.Alignment(0, 0),

        padding=15,

        content=ft.Container(

            width=min(page.width - 30, 1100),

            alignment=ft.Alignment(0, -1),

            content=conteudo

        )

    )