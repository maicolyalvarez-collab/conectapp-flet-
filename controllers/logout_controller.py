import flet as ft
from dao.sesion_dao import SesionDAO

sesion_dao = SesionDAO()


def cerrar_sesion(page: ft.Page):

    # borrar sesión de la BD
    sesion_dao.cerrar()

    # limpiar usuario en memoria
    page.usuario_actual = None

    # ir al login
    page.clean()

    from view.login_view import login_view
    login_view(page)