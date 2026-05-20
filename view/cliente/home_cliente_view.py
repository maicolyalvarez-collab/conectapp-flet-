import flet as ft
from controllers.cliente.home_cliente_controller import HomeClienteController
from controllers.logout_controller import cerrar_sesion

class HomeClienteView:

    def __init__(self, page: ft.Page, usuario_actual):
        self.page = page
        self.usuario_actual = usuario_actual
        self.controller = HomeClienteController(page)
        self.menu = None
    
    def cambiar_menu(self,vista):

        self.page.clean()
        self.page.add(vista)
        self.page.update()

    
    def abrir_menu(self, e):

        self.menu = ft.Container(
            width=320,
            height=self.page.height,
            bgcolor="#111827",
            padding=20,

            content=ft.Column(
                spacing=20,
                controls=[

                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                "Menú",
                                size=24,
                                weight="bold",
                                color="white"
                            ),

                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_color="white",
                                on_click=self.cerrar_menu
                            )
                        ]
                    ),

                    ft.Divider(color="white24"),

                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.CALENDAR_MONTH, color="white"),
                        title=ft.Text("Reservar", color="white"),

                        on_click=lambda e: self.navegar_y_cerrar(
                            self.ir_reservar
                        )
                    ),

                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.CALENDAR_MONTH, color="white"),
                        title=ft.Text("Mis reservas", color="white"),

                        on_click=lambda e: self.navegar_y_cerrar(
                            self.ir_gestionar
                        )
                    ),

                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.NOTIFICATIONS, color="white"),
                        title=ft.Text("Notificaciones", color="white"),

                        on_click=lambda e: self.navegar_y_cerrar(
                            self.ver_notificaciones
                        )
                    ),

                    ft.Divider(color="white24"),

                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LOGOUT, color="red"),
                        title=ft.Text("Cerrar sesión", color="red"),

                        on_click=lambda e: self.navegar_y_cerrar(
                            lambda page: cerrar_sesion(self.page)
                        )
                    )
                ]
            ),
            shadow=ft.BoxShadow(
                blur_radius=15,
                color="white",
                spread_radius=3
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
                            size=30,
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

    # ---------------- NAVIGATION ----------------
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
                ft.Text(d[0]) 
                for d in datos
            ]
        else:
            mensajes = [
                ft.Text("No tienes notificaciones", 
                    size=16
                )
            ]

        dialog = ft.AlertDialog(

            modal=True,

            title=ft.Row(
                [
                    ft.Text("Notificaciones", weight="bold"),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        bgcolor="red",
                        tooltip="cerrar",

                        on_click=lambda e: self.cerrar_dialogo(dialog)
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

    # ---------------- CARD ACCIONES ----------------
    def crear_card(
            self, 
            titulo, 
            descripcion, 
            icono, 
            accion
        ):

        return ft.Container(

            content=ft.Column(

                [
                    ft.Icon(
                        icono, 
                        size=40, 
                        color="white"
                    ),

                    ft.Text(
                        titulo, 
                        size=18, 
                        weight="bold", 
                        color="white"
                    ),

                    ft.Text(
                        descripcion, 
                        size=12, 
                        color="white70"
                    ),

                    ft.Button(

                        "Entrar", 

                        on_click=accion,

                        style=ft.ButtonStyle(
                            bgcolor="#2563eb",
                            color="white",

                            elevation=0,

                            shape=ft.RoundedRectangleBorder(
                                radius=14
                            )
                        )
                    )
                ],

                alignment=ft.MainAxisAlignment.CENTER,

                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),

            width=260,
            height=200,

            bgcolor="#1e1e1e",

            border_radius=20,
            padding=15,

            shadow=ft.BoxShadow(
                blur_radius=15,
                color="white",
                spread_radius=5
            )
        )
        
    # ---------------- BUILD ----------------
    def build(self):


        layout = ft.Column(
            [   
                
                self.build_topbar(),

                ft.Container(height=40),

                ft.Row(
                    [
                        ft.Text(
                            "Bienvenido a nuestro prototipo funcional",

                            size=32,
                            weight="bold",

                            color="white"
                        )
                    ],

                    alignment=ft.MainAxisAlignment.CENTER
                ),

                ft.Container(height=40),

                ft.Row(
                    [
                        ft.Text(
                            "¿Qué deseas hacer hoy?",
                            size=16,
                            color="white70"
                        )
                    ],

                    alignment=ft.MainAxisAlignment.CENTER
                ),

                ft.Container(height=10),

                ft.Row(
                    [
                        self.crear_card(
                            "Reservar",
                            "Agenda un servicio",
                            ft.Icons.CALENDAR_MONTH,
                            self.ir_reservar
                        ),
                        self.crear_card(
                            "Gestionar",
                            "Ver o cancelar",
                            ft.Icons.LIST,
                            self.ir_gestionar
                        ),
                    ],

                    alignment=ft.MainAxisAlignment.CENTER,

                    spacing=50
                ),

            ],
            alignment=ft.MainAxisAlignment.START,

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            spacing=20
        )

        return ft.Container(

            content=layout,

            padding=20,
            
            expand=True
        )