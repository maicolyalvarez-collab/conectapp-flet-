import flet as ft
from dao.reservas_dao import ReservasDAO


class GestionarReservaView:

    def __init__(self, page, usuario):

        self.page = page
        self.usuario = usuario
        self.manager = ReservasDAO()

    # MENSAJE EMERGENTE

    def mostrar_mensaje(self, texto):

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(texto),
            bgcolor="black",
            duration=3000
        )

        self.page.snack_bar.open = True
        self.page.update()

    # RECARGAR VISTA

    def recargar(self):

        self.page.clean()
        self.page.add(self.build())
        self.page.update()

    # FINALIZAR RESERVA

    def finalizar_reserva(self, reserva):

        self.manager.actualizar_estado(
            reserva.id,
            "COMPLETADA"
        )

        self.recargar()

    # ABRIR CALIFICACIÓN

    def abrir_calificacion(self, reserva):

        self.rating = 0
        self.estrellas = []

        # SELECCIONAR ESTRELLAS

        def seleccionar_estrella(index):

            self.rating = index + 1

            for i in range(5):

                self.estrellas[i].icon = (
                    ft.Icons.STAR
                    if i <= index
                    else ft.Icons.STAR_BORDER
                )

            self.page.update()

        # CREAR ESTRELLAS

        for i in range(5):

            estrella = ft.IconButton(

                icon=ft.Icons.STAR_BORDER,
                icon_color="yellow",
                icon_size=30,

                on_click=lambda e, idx=i:
                seleccionar_estrella(idx)

            )

            self.estrellas.append(estrella)

        # FILA ESTRELLAS

        self.row_estrellas = ft.Row(

            self.estrellas,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5
        )

        # CAMPO COMENTARIO

        self.comentario = ft.TextField(
            label="Comentario"
        )

        # DIALOGO

        dialog = ft.AlertDialog(

            title=ft.Text("Califica el servicio"),

            content=ft.Container(

                width=300,

                content=ft.Column(

                    [
                        self.row_estrellas,
                        self.comentario
                    ],

                    tight=True,
                    spacing=10
                )
            ),

            actions=[

                ft.TextButton(
                    "Enviar",
                    on_click=lambda e:
                    self.guardar_calificacion(reserva)
                )
            ],

            modal=True
        )

        self.page.overlay.append(dialog)

        dialog.open = True

        self.page.update()

    # GUARDAR CALIFICACIÓN

    def guardar_calificacion(self, reserva):

        if self.rating == 0:

            self.page.snack_bar = ft.SnackBar(
                ft.Text("Selecciona al menos una estrella")
            )

            self.page.snack_bar.open = True
            self.page.update()

            return

        # GUARDAR EN BD

        self.manager.guardar_calificacion(

            reserva.id,
            self.rating,
            self.comentario.value
        )

        # MARCAR CALIFICADA

        reserva.calificada = True

        # MENSAJE

        self.mostrar_mensaje(
            "Gracias por tu reseña :)"
        )

        # CERRAR DIALOGO

        for d in self.page.overlay:

            if isinstance(d, ft.AlertDialog) and d.open:

                d.open = False

        self.page.update()

        self.recargar()

    # VOLVER

    def volver(self, e):

        from view.cliente.home_cliente_view import HomeClienteView

        self.page.clean()

        self.page.add(
            HomeClienteView(
                self.page,
                self.usuario
            ).build()
        )

        self.page.update()

    # CANCELAR RESERVA

    def confirmar_cancelacion(self, reserva):

        dialog = ft.AlertDialog()

        # ACEPTAR

        def aceptar(e):

            self.manager.cancelar_reserva(
                reserva.id
            )

            dialog.open = False

            self.page.update()

            self.mostrar_mensaje(
                "RESERVA CANCELADA CORRECTAMENTE"
            )

            self.recargar()

        # CANCELAR

        def cancelar(e):

            dialog.open = False
            self.page.update()

        dialog.title = ft.Text("Confirmación")

        dialog.content = ft.Text(
            "¿Deseas cancelar la reserva?"
        )

        dialog.actions = [

            ft.TextButton(
                "Sí",
                on_click=aceptar
            ),

            ft.TextButton(
                "No",
                on_click=cancelar
            )
        ]

        self.page.overlay.append(dialog)

        dialog.open = True

        self.page.update()

    # TARJETA RESERVA

    def tarjeta_reserva(self, reserva):

        estado = reserva.estado.upper()

        botones = []

        # COLORES ESTADO

        color_estado = {

            "CONFIRMADA": "#38bdf8",
            "COMPLETADA": "#22c55e",
            "CANCELADA": "#ef4444"

        }.get(estado, "white")

        # FINALIZAR

        if estado == "CONFIRMADA":

            botones.append(

                ft.TextButton(

                    "Finalizar (test)",

                    on_click=lambda e:
                    self.finalizar_reserva(reserva)
                )
            )

        # CALIFICAR

        if estado == "COMPLETADA":

            if not reserva.calificada:

                botones.append(

                    ft.TextButton(

                        "Calificar",

                        on_click=lambda e:
                        self.abrir_calificacion(reserva)
                    )
                )

            else:

                botones.append(

                    ft.Text(

                        "CALIFICADO",

                        color="white",
                        weight="bold"
                    )
                )

        return ft.Container(

            padding=15,
            border_radius=18,
            bgcolor="#1e1e1e",

            content=ft.Row(

                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                controls=[

                    # INFO RESERVA

                    ft.Column(
                        spacing=5,
                        controls=[

                            ft.Text(
                                reserva.servicio,
                                color="white",
                                weight="bold",
                                size=18
                            ),

                            ft.Text(
                                f"Prestador ID: {reserva.prestador_id}",
                                color="#38bdf8"
                            ),

                            ft.Text(
                                f"Fecha: {reserva.fecha}",
                                color="white70"
                            ),

                            ft.Text(
                                f"Hora: {reserva.hora}",
                                color="white70"
                            ),

                            ft.Container(

                                padding=8,
                                border_radius=10,
                                bgcolor=color_estado,

                                content=ft.Text(
                                    estado,
                                    color="black",
                                    weight="bold"
                                )
                            )
                        ]
                    ),

                    # BOTONES
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        controls=
                        botones +
                        [

                            ft.TextButton(
                                "Cancelar",
                                on_click=lambda e:
                                self.confirmar_cancelacion(reserva)
                            )

                            if estado == "CONFIRMADA"

                            else ft.Container()
                        ]
                    )
                ]
            )
        )

    # BUILD

    def build(self):

        if not hasattr(self.page, "usuario_actual"):

            return ft.Text(
                "Usuario no autenticado",
                color="red"
            )

        cliente_id = self.page.usuario_actual.id

        reservas = self.manager.obtener_reservas_por_cliente(
            cliente_id
        )

        lista = ft.ListView(

            expand=True,
            spacing=10,

            controls=[
                self.tarjeta_reserva(r)
                for r in reservas
            ]
        )

        layout = ft.Column(

            spacing=20,
            expand=True,

            controls=[

                ft.Text(
                    "Mis Reservas",
                    size=30,
                    weight="bold",
                    color="white"
                ),
                lista,

                ft.Button(
                    "Volver",
                    on_click=self.volver,
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(
                            2,"white"
                        ),
                        color="white"
                    )
                )
            ]
        )

        return ft.Container(

            content=layout,
            expand=True,
            bgcolor="#121212",
            padding=20
        )