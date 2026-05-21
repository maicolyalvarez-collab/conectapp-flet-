import flet as ft
from controllers.app_controller import AppController

def main(page: ft.Page):

    page.title = "CONECTAPP"

    page.theme_mode = ft.ThemeMode.DARK

    page.bgcolor = "#070B14"

    page.padding = 0

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.scroll = "auto"

    page.window_width = 1600
    page.window_height = 900

    app_controller = AppController(page)
    app_controller.iniciar()

ft.run(
    main,
    assets_dir="assets")