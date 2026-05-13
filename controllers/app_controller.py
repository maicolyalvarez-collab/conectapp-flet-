import flet as ft

from dao.sesion_dao import SesionDAO
from dao.usuarios_dao import UsuariosDAO
from view.login_view import login_view
from view.cliente.home_cliente_view import HomeClienteView


class AppController:

    def __init__(self, page: ft.Page):
        self.page = page
        self.sesion_dao = SesionDAO()
        self.usuarios_dao = UsuariosDAO()

    def iniciar(self):

        self.page.title = "CONECTAPP"
        self.page.bgcolor = ft.Colors.BLACK
        self.page.vertical_alignment = "center"
        self.page.horizontal_alignment = "center"

        # 🔐 revisar sesión
        usuario_id = self.sesion_dao.obtener()

        if usuario_id:

            usuario = self.usuarios_dao.obtener_por_id(usuario_id)

            if usuario:
                self.page.usuario_actual = usuario
                self.page.clean()
                self.page.add(HomeClienteView(self.page, usuario).build())
                return

            # si la sesión está rota
            self.sesion_dao.cerrar()

        # si no hay sesión
        login_view(self.page)