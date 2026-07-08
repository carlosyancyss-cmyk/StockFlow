from pathlib import Path
import flet as ft


def salvar_arquivo(page: ft.Page, arquivo: str | Path):

    print(">>> ENTROU EM salvar_arquivo")

    arquivo = Path(arquivo)

    if not arquivo.exists():

        page.snack_bar = ft.SnackBar(
            content=ft.Text("Arquivo não encontrado.")
        )
        page.snack_bar.open = True
        page.update()
        return

    # Windows
    if page.platform == ft.PagePlatform.WINDOWS:

        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Arquivo salvo em:\n{arquivo}")
        )

        page.snack_bar.open = True
        page.update()
        return

    # Android
    page.launch_url(str(arquivo))

    page.snack_bar = ft.SnackBar(
        content=ft.Text("Abrindo arquivo...")
    )

    page.snack_bar.open = True
    page.update()