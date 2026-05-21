import flet as ft
from controllers.cliente.home_cliente_controller import HomeClienteController
from controllers.logout_controller import cerrar_sesion


class HomeClienteView:

    def __init__(self, page: ft.Page, usuario_actual):
        self.page = page
        self.usuario_actual = usuario_actual
        self.controller = HomeClienteController(page)
        self.menu = None


    def cambiar_menu(self, vista):

        self.page.clean()
        self.page.add(vista)
        self.page.update()


    def abrir_menu(self, e):

        self.menu = ft.Container(

            width=320,
            height=self.page.height,

            bgcolor="#0B1120",

            padding=20,

            content=ft.Column(

                spacing=20,

                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[


                    ft.Image(
                        src="logo.png",
                        width=170
                    ),

                    

                    ft.Text(
                        "Servicios de limpieza",
                        size=12,
                        color="#9CA3AF"
                    ),

                    ft.Divider(color="white24"),


                    ft.Container(

                        width=280,

                        content=ft.Row(

                            alignment=ft.MainAxisAlignment.END,

                            controls=[

                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_color="white",
                                    on_click=self.cerrar_menu
                                )
                            ]
                        )
                    ),


                    ft.ListTile(

                        leading=ft.Icon(
                            ft.Icons.CALENDAR_MONTH,
                            color="white"
                        ),

                        title=ft.Text(
                            "Reservar",
                            color="white"
                        ),

                        on_click=lambda e: self.navegar_y_cerrar(
                            self.ir_reservar
                        )
                    ),

                    ft.ListTile(

                        leading=ft.Icon(
                            ft.Icons.LIST,
                            color="white"
                        ),

                        title=ft.Text(
                            "Mis reservas",
                            color="white"
                        ),

                        on_click=lambda e: self.navegar_y_cerrar(
                            self.ir_gestionar
                        )
                    ),

                    ft.ListTile(

                        leading=ft.Icon(
                            ft.Icons.NOTIFICATIONS,
                            color="white"
                        ),

                        title=ft.Text(
                            "Notificaciones",
                            color="white"
                        ),

                        on_click=lambda e: self.navegar_y_cerrar(
                            self.ver_notificaciones
                        )
                    ),

                    ft.Divider(color="white24"),

                    ft.ListTile(

                        leading=ft.Icon(
                            ft.Icons.LOGOUT,
                            color="red"
                        ),

                        title=ft.Text(
                            "Cerrar sesión",
                            color="red"
                        ),

                        on_click=lambda e: self.navegar_y_cerrar(
                            lambda page: cerrar_sesion(self.page)
                        )
                    )
                ]
            ),

            shadow=ft.BoxShadow(
                blur_radius=25,
                color="#00000055",
                spread_radius=1
            )
        )

        self.page.overlay.append(self.menu)

        self.page.update()
    def navegar_y_cerrar(self, funcion):

        self.cerrar_menu(None)

        funcion(self.page)

    def cerrar_menu(self, e):

        if self.menu and self.menu in self.page.overlay:

            self.page.overlay.remove(self.menu)

            self.menu = None

            self.page.update()

    def build_topbar(self):

        nombre = getattr(
            self.usuario_actual,
            "nombre",
            "Cliente"
        )

        return ft.Row(

            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

            controls=[

                ft.Row(

                    spacing=10,

                    controls=[

                        ft.IconButton(
                            icon=ft.Icons.MENU,
                            icon_color="white",
                            on_click=self.abrir_menu
                        ),

                        ft.Text(
                            f"👋 Hola, {nombre}",
                            size=34,
                            weight="bold",
                            color="white"
                        )
                    ]
                ),

                ft.IconButton(
                    icon=ft.Icons.NOTIFICATIONS,
                    icon_color="white",
                    on_click=self.ver_notificaciones
                )
            ]
        )

    def ir_reservar(self, e):

        from view.cliente.reserva_view import ReservaView

        self.cambiar_menu(
            ReservaView(
                self.page,
                self.usuario_actual
            ).build()
        )

    def ir_gestionar(self, e):

        from view.cliente.gestionar_reserva_view import GestionarReservaView

        self.cambiar_menu(
            GestionarReservaView(
                self.page,
                self.usuario_actual
            ).build()
        )

    def cerrar_dialogo(self, dialog):

        dialog.open = False
        self.page.update()

    def ver_notificaciones(self, e):

        datos = self.controller.obtener_notificaciones(
            self.usuario_actual.id
        )

        if datos:
            mensajes = [
                ft.Text(
                    d[0],
                    color="white"
                )
                for d in datos
            ]
        else:
            mensajes = [
                ft.Text(
                    "No tienes notificaciones",
                    size=16,
                    color="white"
                )
            ]

        dialog = ft.AlertDialog(

            modal=True,

            bgcolor="#1A1D29",

            title=ft.Row(

                [
                    ft.Text(
                        "Notificaciones",
                        weight="bold",
                        color="white"
                    ),

                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        bgcolor="red",
                        tooltip="cerrar",

                        on_click=lambda e:
                        self.cerrar_dialogo(dialog)
                    )
                ],

                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),

            content=ft.Container(

                content=ft.Column(

                    mensajes,

                    tight=True,
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO
                ),

                width=350,
                height=250,
                padding=10
            )
        )

        self.page.overlay.append(dialog)

        dialog.open = True

        self.page.update()


    def crear_card(
        self,
        titulo,
        descripcion,
        icono,
        accion
    ):

        return ft.Container(

            width=320,
            height=300,

            bgcolor="#111827",

            border_radius=30,

            padding=25,

            shadow=ft.BoxShadow(
                blur_radius=30,
                spread_radius=1,
                color="#00000055",
                offset=ft.Offset(0, 8)
            ),

            content=ft.Column(

                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                alignment=ft.MainAxisAlignment.CENTER,

                spacing=15,

                controls=[

                    ft.Container(

                        width=90,
                        height=90,

                        border_radius=25,

                        bgcolor="#2563EB22",

                        alignment=ft.Alignment(0, 0),

                        content=ft.Icon(
                            icono,
                            size=50,
                            color="#2563EB"
                        )
                    ),

                    ft.Text(
                        titulo,
                        size=26,
                        weight="bold",
                        color="white"
                    ),

                    ft.Text(
                        descripcion,
                        size=14,
                        color="#9CA3AF",
                        text_align=ft.TextAlign.CENTER
                    ),

                    ft.Container(height=5),

                    ft.ElevatedButton(

                        "Entrar",

                        on_click=accion,

                        style=ft.ButtonStyle(

                            bgcolor="#2563EB",
                            color="white",

                            padding=20,

                            shape=ft.RoundedRectangleBorder(
                                radius=16
                            )
                        )
                    )
                ]
            )
        )


    def info_card(self, icono, titulo, descripcion):

        return ft.Container(

            width=260,

            padding=20,

            border_radius=20,

            bgcolor="#111827",

            content=ft.Row(

                spacing=15,

                controls=[

                    ft.Container(

                        width=60,
                        height=60,

                        border_radius=20,

                        bgcolor="#2563EB22",

                        alignment=ft.Alignment(0, 0),

                        content=ft.Icon(
                            icono,
                            color="#2563EB",
                            size=30
                        )
                    ),

                    ft.Column(

                        spacing=5,

                        controls=[

                            ft.Text(
                                titulo,
                                size=16,
                                weight="bold",
                                color="white"
                            ),

                            ft.Text(
                                descripcion,
                                size=12,
                                color="#9CA3AF"
                            )
                        ]
                    )
                ]
            )
        )


    def build(self):

        self.page.bgcolor = "#070B14"

        info_cards = ft.Row(

            alignment=ft.MainAxisAlignment.CENTER,

            spacing=20,

            controls=[

                self.info_card(
                    ft.Icons.VERIFIED_USER,
                    "Profesionales verificados",
                    "Prestadores calificados."
                ),

                self.info_card(
                    ft.Icons.LOCK,
                    "Pagos seguros",
                    "Transacciones protegidas."
                ),

                self.info_card(
                    ft.Icons.STAR,
                    "Calidad garantizada",
                    "Servicios confiables."
                ),

                self.info_card(
                    ft.Icons.SUPPORT_AGENT,
                    "Soporte 24/7",
                    "Estamos para ayudarte."
                )
            ]
        )


        hero = ft.Container(

            width=1200,

            border_radius=30,

            padding=40,

            bgcolor="#0B1120",

            shadow=ft.BoxShadow(
                blur_radius=35,
                spread_radius=1,
                color="#00000066",
                offset=ft.Offset(0, 10)
            ),

            content=ft.Row(

                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                controls=[

                    ft.Column(

                        spacing=20,

                        controls=[

                            ft.Text(
                                "Confianza en cada servicio,\ntranquilidad en tu hogar.",
                                size=38,
                                weight="bold",
                                color="white"
                            ),

                            ft.Text(
                                "Reserva servicios de limpieza profesionales\n"
                                "de forma rápida, segura y moderna.",
                                size=18,
                                color="#9CA3AF"
                            ),

                            ft.ElevatedButton(

                                "Reservar ahora",

                                on_click=lambda e: self.ir_reservar(e),

                                style=ft.ButtonStyle(
                                    bgcolor="#2563EB",
                                    color="white",
                                    padding=20
                                )
                            )
                        ]
                    ),

                    ft.Container(

                        width=220,
                        height=220,

                        border_radius=30,

                        bgcolor="#2563EB22",

                        alignment=ft.Alignment(0, 0),

                        content=ft.Icon(
                            ft.Icons.CLEANING_SERVICES,
                            size=120,
                            color="#2563EB"
                        )
                    )
                ]
            )
        )


        contenido = ft.Column(

            scroll=ft.ScrollMode.AUTO,

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            spacing=25,

            controls=[

                self.build_topbar(),

                ft.Container(height=10),
                
                ft.Text(
                    "Bienvenido a",
                    size=30,
                    color="white"
                ),
                
                ft.Image(
                    src="logo.png",
                    width=280
                ),

                ft.Text(
                    "La solución segura y moderna para contratar\n"
                    "servicios de limpieza en viviendas vacacionales.",
                    size=18,
                    color="#9CA3AF",
                    text_align=ft.TextAlign.CENTER
                ),

                ft.Container(height=20),

                info_cards,

                ft.Container(height=20),

                hero,

                ft.Container(height=30),

                ft.Row(

                    alignment=ft.MainAxisAlignment.CENTER,

                    spacing=40,

                    controls=[

                        self.crear_card(
                            "Reservar",
                            "Agenda servicios de limpieza rápidos y seguros.",
                            ft.Icons.CALENDAR_MONTH,
                            lambda e: self.ir_reservar(e)
                        ),

                        self.crear_card(
                            "Gestionar",
                            "Consulta o cancela tus reservas fácilmente.",
                            ft.Icons.LIST,
                            lambda e: self.ir_gestionar(e)
                        )
                    ]
                ),

                ft.Container(height=30)
            ]
        )

        return ft.Container(

            expand=True,

            padding=30,

            content=contenido
        )