import flet as ft


class HomeAdminView:

    def __init__(self, page, usuario_actual):

        print("CARGANDO HOME ADMIN VIEW")

        self.page = page
        self.usuario_actual = usuario_actual

    # =====================================================
    # NAVEGACIONES
    # =====================================================

    def ir_prestadores(self, e):

        print("GESTION PRESTADORES")

        self.page.snack_bar = ft.SnackBar(
            ft.Text("Entrando a Gestión de Prestadores")
        )

        self.page.snack_bar.open = True
        self.page.update()

    def ir_clientes(self, e):

        print("GESTION CLIENTES")

        self.page.snack_bar = ft.SnackBar(
            ft.Text("Entrando a Gestión de Clientes")
        )

        self.page.snack_bar.open = True
        self.page.update()

    def ir_horarios(self, e):

        print("GESTION HORARIOS")

        self.page.snack_bar = ft.SnackBar(
            ft.Text("Entrando a Gestión de Horarios")
        )

        self.page.snack_bar.open = True
        self.page.update()

    def ir_reservas(self, e):

        print("GESTION RESERVAS")

        self.page.snack_bar = ft.SnackBar(
            ft.Text("Entrando a Gestión de Reservas")
        )

        self.page.snack_bar.open = True
        self.page.update()

    def ir_reportes(self, e):

        print("GESTION REPORTES")

        self.page.snack_bar = ft.SnackBar(
            ft.Text("Entrando a Reportes")
        )

        self.page.snack_bar.open = True
        self.page.update()

    def cerrar_sesion(self, e):

        print("CERRANDO SESION")

        self.page.clean()

        self.page.add(
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Text(
                    "LOGIN VIEW",
                    size=30,
                    weight=ft.FontWeight.BOLD
                )
            )
        )

        self.page.update()

    # =====================================================
    # COMPONENTES
    # =====================================================

    def card_dashboard(self, titulo, valor, icono):

        return ft.Container(

            width=220,
            height=120,

            bgcolor="white",

            border_radius=20,

            padding=20,

            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.BLACK12,
                offset=ft.Offset(0, 4)
            ),

            content=ft.Column(

                alignment=ft.MainAxisAlignment.CENTER,

                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[

                    ft.Icon(
                        icono,
                        size=35,
                        color="#2563EB"
                    ),

                    ft.Text(
                        titulo,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color="#374151"
                    ),

                    ft.Text(
                        valor,
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="#2563EB"
                    )
                ]
            )
        )

    def boton_admin(self, texto, icono, funcion, color="#2563EB"):

        return ft.Container(

            width=350,

            content=ft.ElevatedButton(

                content=ft.Row(

                    alignment=ft.MainAxisAlignment.CENTER,

                    controls=[

                        ft.Icon(icono, color="white"),

                        ft.Text(
                            texto,
                            color="white",
                            size=16,
                            weight=ft.FontWeight.BOLD
                        )
                    ]
                ),

                bgcolor=color,

                height=55,

                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12)
                ),

                on_click=funcion
            )
        )

    # =====================================================
    # UI PRINCIPAL
    # =====================================================

    def build(self):

        return ft.Container(

            expand=True,

            bgcolor="#F3F4F6",

            padding=20,

            content=ft.Column(

                scroll=ft.ScrollMode.AUTO,

                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[

                    # =========================================
                    # TITULO
                    # =========================================

                    ft.Container(

                        margin=20,

                        content=ft.Column(

                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                            controls=[

                                ft.Text(
                                    "PANEL ADMINISTRADOR",
                                    size=34,
                                    weight=ft.FontWeight.BOLD,
                                    color="#111827"
                                ),

                                ft.Text(
                                    f"Bienvenido {self.usuario_actual.nombre}",
                                    size=18,
                                    color="#6B7280"
                                )
                            ]
                        )
                    ),

                    # =========================================
                    # DASHBOARD
                    # =========================================

                    ft.Row(

                        wrap=True,

                        alignment=ft.MainAxisAlignment.CENTER,

                        spacing=20,

                        controls=[

                            self.card_dashboard(
                                "Prestadores",
                                "0",
                                ft.Icons.PEOPLE
                            ),

                            self.card_dashboard(
                                "Clientes",
                                "0",
                                ft.Icons.PERSON
                            ),

                            self.card_dashboard(
                                "Reservas Hoy",
                                "0",
                                ft.Icons.CALENDAR_MONTH
                            )
                        ]
                    ),

                    # =========================================
                    # MENU ADMIN
                    # =========================================

                    ft.Container(

                        margin=40,

                        content=ft.Column(

                            spacing=18,

                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                            controls=[

                                self.boton_admin(
                                    "Gestionar Prestadores",
                                    ft.Icons.PEOPLE,
                                    self.ir_prestadores
                                ),

                                self.boton_admin(
                                    "Gestionar Clientes",
                                    ft.Icons.PERSON,
                                    self.ir_clientes
                                ),

                                self.boton_admin(
                                    "Gestionar Horarios",
                                    ft.Icons.ACCESS_TIME,
                                    self.ir_horarios
                                ),

                                self.boton_admin(
                                    "Gestionar Reservas",
                                    ft.Icons.CALENDAR_MONTH,
                                    self.ir_reservas
                                ),

                                self.boton_admin(
                                    "Reportes",
                                    ft.Icons.BAR_CHART,
                                    self.ir_reportes
                                ),

                                self.boton_admin(
                                    "Cerrar Sesión",
                                    ft.Icons.LOGOUT,
                                    self.cerrar_sesion,
                                    color="#DC2626"
                                )
                            ]
                        )
                    )
                ]
            )
        )