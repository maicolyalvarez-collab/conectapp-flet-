import flet as ft
from dao.notificaciones_dao import NotificacionesDAO

class HomeClienteView:

    def __init__(self, page, usuario):
        self.page = page
        self.usuario = usuario

    # NAVEGACION

    def ir_reservar(self, e):
        print("RESERVAR")

        from view.cliente.reserva_view import ReservaView
        
        self.page.clean()
        self.page.add(ReservaView(self.page).build())
        self.page.update()

    def ir_gestionar(self, e):
        print("Gestionar")

        from view.cliente.gestionar_reserva_view import GestionarReservaView

        self.page.clean()
        self.page.add(GestionarReservaView(self.page, self.usuario).build())
        self.page.update()

    def cerrar_dialogo(self,dialog):
            dialog.open = False
            self.page.update()

    def ver_notificaciones(self, e):
        print("ENTRANDO A LA CAPMANA")
        dao = NotificacionesDAO()

        datos = dao.obtener_notificaciones(self.usuario.id)
        print(datos)

        mensajes = []


        if datos:
            for d in datos:
                mensajes.append(ft.Text(d[0]))

        else:
            mensajes.append(
                ft.Text(
                    "No tienes notificaciones", 
                    size=16
                )   
            ) 

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Text(
                    "Notificaciones",
                    weight="bold"
                    ),
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

    # COMPONENTE REUTILIZABLE 

    def crear_card(self, titulo, descripcion, icono, accion):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icono, size=40, color="white"),

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
                        bgcolor="#0276a8",
                        color="white"
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),

            width=260,
            height=200,
            bgcolor="#1e1e1e",
            border_radius=20,
            padding=15,

            shadow=ft.BoxShadow(
                blur_radius=15,
                color="white",
                spread_radius=1
            )
        )

    # CONSTRUCCIÓN DE LA VISTA 

    def build(self):

        print("CARGANDO HOME CLIENTE VIEW")

        layout = ft.Column(
            [
                # Encabezado con título centrado y campana a la derecha
                ft.Stack(
                    [
                        # Texto centrado
                        ft.Container(
                            content=ft.Text(
                                "Bienvenido a nuestro adelanto de PGC",
                                size=36,
                                weight="bold",
                                color="white"
                            ),
                            alignment=ft.Alignment.CENTER   #centro
                        ),

                        # Campana en la esquina superior derecha
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.Icons.NOTIFICATIONS,
                                icon_color="white",
                                icon_size=40,
                                on_click=self.ver_notificaciones
                            ),
                            alignment=ft.Alignment.TOP_RIGHT,
                            padding=10
                        )
                    ],
                    height=70
                ),

                # Pregunta centrada
                ft.Row(
                    [
                        ft.Text(
                            "¿Qué deseas hacer hoy?",
                            size=18,
                            color="white70"
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                

                # Botones de acción
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
                    spacing=15
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=30
        )

        return ft.Container(
            content=layout,
            padding=ft.Padding(top=5,left=25,right=25),
            #expand=True
        )