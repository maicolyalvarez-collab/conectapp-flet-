import flet as ft

from view.admin.menu import MenuAdmin
from view.admin.barra import BarraAdmin
from view.admin.admin_view import HomeAdmin

class Admin:

    def __init__(self,page):
        self.page = page
        self.contenido = ft.Column()
    
    def cambiar_vista(self,vista):
        self.contenido.controls.clear()

        if vista == "admin_view":
            self.contenido.controls.append(HomeAdmin().build())
        
        self.page.update()

    def build(self):
        
        menu = MenuAdmin(self.cambiar_vista)
        barra = BarraAdmin()

        self.cambiar_vista("admin_view") #tal vez un error

        self.page.add(
            ft.Row([
                menu.build(),
                ft.Column([
                    barra.build(),
                    self.contenido
                ], expand=True)
            ], expand=True)
        )
