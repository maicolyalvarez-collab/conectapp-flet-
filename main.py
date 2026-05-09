import flet as ft

from view.login_view import login_view


def main(page: ft.Page):

    page.title = "ADELANTO PGC"
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    login_view(page)
    #cargar_vista(page, usuario) # Cargar la vista según el rol del usuario

ft.run(main)