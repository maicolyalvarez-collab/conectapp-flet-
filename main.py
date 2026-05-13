import flet as ft
from controllers.app_controller import AppController


def main(page: ft.Page):

    page.title = "CONECTAPP"
    app_controller = AppController(page)
    app_controller.iniciar()

ft.run(main)