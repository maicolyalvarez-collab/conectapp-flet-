#side bar
import flet as ft

class MenuAdmin:
    def __init__(self,cambiar):
        self.cambiar = cambiar

    def build(self):
        return ft.Column([
            ft.Text("ADMIN"),
            ft.Button("HOME", on_click=lambda e : self.cambiar("admin_view")),
            ft.Button("Gestionar Usuarios", on_click=lambda e : self.cambiar("gestionar_usuarios")),
            ft.Button("Reportes", on_click=lambda e : self.cambiar("reportes"))

        ], width=180)