import flet as ft
from services.auth_service import AuthService

auth_service = AuthService()

def login_view(page: ft.Page):
    print("CARGANDO LOGIN VIEW")

    page.clean()
    page.bgcolor = "#000205" 

    #campos del usuario
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

        # guardar usuario logueado
        page.usuario_actual = usuario

        # redirección por rol
        page.clean()

        if usuario.rol == "admin":
            from view.admin.admin_view import HomeAdminView
            page.add(HomeAdminView().build())
            page.update()

        elif usuario.rol == "empleado":
            from view.empleado.empleado_view import HomeClienteView
            page.add(HomeClienteView().build())
            page.update()

        elif usuario.rol == "cliente":
            from view.cliente.home_cliente_view import HomeClienteView
            page.add(HomeClienteView(page, usuario).build())
            page.update()

    #contenedor principal del login
    page.add(
        ft.Container(
            ft.Column(
            [
                ft.Text("Iniciar sesión",
                    size=30, 
                    weight="bold",
                    color="white"
                ),

                #contraseñas de prueba
                ft.Text(
                    "admin, admin123",
                    size=12,
                    color="white70"
                ),

                user_input,
                pass_input,

                ft.Button(
                    "Entrar",
                    on_click=login_click,#conecta la funcion de login al boton
                    bgcolor="blue",#color del fondo
                    color="white" #color del texto
                ),

                error_text
            ],

            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,#centra verticalmente
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,#centra horizontalmente
            expand=True
        ),
        bgcolor="#2f3643", 
        border_radius=20,
        padding=25,#espaciado interno del contenedor
        width=320,
        height=400,

        shadow=ft.BoxShadow(
                blur_radius=15,
                color="white",
                spread_radius=3
            )
        )
    )
