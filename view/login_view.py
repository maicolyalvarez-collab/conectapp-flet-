import flet as ft
from services.auth_service import AuthService
from dao.sesion_dao import SesionDAO

auth_service = AuthService()
sesion_dao = SesionDAO()


def login_view(page: ft.Page):
    print("CARGANDO LOGIN VIEW")

    page.clean()
    page.bgcolor = "#000205"

    user_input = ft.TextField(
        hint_text="Correo Electrónico",
        width=280
    )

    pass_input = ft.TextField(
        hint_text="Contraseña",
        width=280,
        password=True
    )

    error_text = ft.Text("", color="red")

    def login_click(e):

        email = user_input.value
        password = pass_input.value

        usuario = auth_service.login(email, password)

        if not usuario:
            error_text.value = "Correo o contraseña incorrectos"
            page.update()
            return

        sesion_dao.guardar(usuario.id)

        page.usuario_actual = usuario

        page.clean()
        

        if usuario.rol == "admin":
            from view.admin.home_admin_view import HomeAdminView
            page.add(HomeAdminView(page, usuario).build())

        elif usuario.rol == "empleado":
            from view.empleado.empleado_view import HomeEmpleadoView
            page.add(HomeEmpleadoView(page, usuario).build())

        elif usuario.rol == "cliente":
            from view.cliente.home_cliente_view import HomeClienteView
            page.add(HomeClienteView(page, usuario).build())

        page.update()

    page.add(
        ft.Container(
            ft.Column(
                [
                    ft.Text(
                        "Iniciar sesión",
                        size=30,
                        weight="bold",
                        color="white"
                    ),

                    user_input,
                    pass_input,

                    ft.Button(
                        "Entrar",
                        on_click=login_click,
                        bgcolor="blue",
                        color="white"
                    ),

                    error_text
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            ),
            bgcolor="#2f3643",
            border_radius=20,
            padding=25,
            width=320,
            height=400,
            shadow=ft.BoxShadow(
                blur_radius=15,
                color="white",
                spread_radius=3
            )
        )
    )