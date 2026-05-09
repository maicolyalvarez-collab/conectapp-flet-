#parte superior

import flet as ft

class BarraAdmin:
    def build(self):
        return ft.Row([
            ft.Text("PANEL ADMINISTRADOR",size=20),
            ft.Container(expand=True),
            ft.Button("salir")
        ])