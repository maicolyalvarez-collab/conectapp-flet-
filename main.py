import flet as ft
from controllers.app_controller import AppController

def main(page: ft.Page):

    # VENTANA
    page.title = "CONECTAPP"

    # TEMA
    page.theme_mode = ft.ThemeMode.DARK

    # FONDO GENERAL
    page.bgcolor = "#070B14"

    # ESPACIADO
    page.padding = 0

    # CENTRAR
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # SCROLL
    page.scroll = "auto"

    # TAMAÑO
    page.window_width = 1600
    page.window_height = 900

    app_controller = AppController(page)
    app_controller.iniciar()

ft.app(
    target=main,
    assets_dir="assets")