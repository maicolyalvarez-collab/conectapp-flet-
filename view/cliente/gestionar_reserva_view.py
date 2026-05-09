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
            bgcolor="black",   # opcional: color de fondo
            duration=3000     # opcional: tiempo en ms
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
        self.manager.actualizar_estado(reserva.id, "COMPLETADA")
        self.recargar()


    # ABRIR CALIFICACIÓN

    def abrir_calificacion(self, reserva):
        print("ABRIENDO CALIFICACION")

        self.rating = 0
        self.estrellas = []

        # FUNCIÓN SELECCIONAR

        def seleccionar_estrella(index):
            self.rating = index + 1
            print("RATING:", self.rating)

            #ACTUALIZAR CONTENIDO
            for i in range(5):

                self.estrellas[i].icon = ft.Icons.STAR if i <= index else ft.Icons.STAR_BORDER
            
            self.page.update()

            self.page.update()

        # CREAR ESTRELLAS

        for i in range(5):
            estrella = ft.IconButton(
            
                icon=ft.Icons.STAR_BORDER,
                icon_color="yellow",
                icon_size=30,
                on_click=lambda e, idx=i: seleccionar_estrella(idx)
                
            )
            self.estrellas.append(estrella)

        # contenedor visual
        self.row_estrellas = ft.Row(
            self.estrellas,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5
        )

        # comentario
        self.comentario = ft.TextField(label="Comentario")

        # dialogo
        dialog = ft.AlertDialog(
            title=ft.Text("Califica el servicio"),
            content=ft.Container(   # aquí controlo el tamaño
                content=ft.Column(
                    [self.row_estrellas, self.comentario],
                    tight=True,
                    spacing=10
                ),
                width=300,   # ahora sí funciona porque está en Container
            ),
            actions=[
                ft.TextButton("Enviar", on_click=lambda e: self.guardar_calificacion(reserva))
            ],
            modal=True
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()


    # GUARDAR CALIFICACIÓN

    def guardar_calificacion(self, reserva):
        print("CLICK ENVIAR")

        if self.rating == 0:
            # Mostrar mensaje de error
            self.page.snack_bar = ft.SnackBar(ft.Text("Selecciona al menos una estrella"))
            self.page.snack_bar.open = True
            self.page.update()
            return

        #GUARDAR EN BD 
        self.manager.guardar_calificacion(
            reserva.id,
            self.rating,
            self.comentario.value
        )

        #marcar la reserva como calificada
        reserva.calificada = True

        # Mostrar mensaje de confirmación
        self.mostrar_mensaje("Gracias por tu reseña :)")

        #cerrar el dialogo

        for d in self.page.overlay:
            if isinstance(d, ft.AlertDialog) and d.open:
                d.open = False

        self.page.update()
 
        self.recargar()


    # VOLVER

    def volver(self, e):
        from view.cliente.home_cliente_view import HomeClienteView
        self.page.clean()
        self.page.add(HomeClienteView(self.page, self.usuario).build())
        self.page.update()


    # CANCELAR

    def confirmar_cancelacion(self, reserva):

        dialog = ft.AlertDialog()

        def aceptar(e):
            self.manager.cancelar_reserva(reserva.id)
            dialog.open = False
            self.page.update()

            self.mostrar_mensaje("RESERVA CANCELADA CORRECTAMENTE")
            self.recargar()

        def cancelar(e):
            dialog.open = False
            self.page.update()

        dialog.title = ft.Text("Confirmación")
        dialog.content = ft.Text("¿Deseas cancelar la reserva?")
        dialog.actions = [
            ft.TextButton("Sí", on_click=aceptar),
            ft.TextButton("No", on_click=cancelar),
        ]

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()


    # TARJETA DE RESERVA

    def tarjeta_reserva(self, reserva):

        estado = reserva.estado.upper()
        botones = []

        # FINALIZAR
        if estado == "CONFIRMADA":
            botones.append(
                ft.TextButton(
                    "Finalizar (test)",
                    on_click=lambda e: self.finalizar_reserva(reserva)
                )
            )

        # CALIFICAR
        if estado == "COMPLETADA":
            if not reserva.calificada:
                botones.append(
                    ft.TextButton(
                        "Calificar",
                        on_click=lambda e: self.abrir_calificacion(reserva)
                    )
                )
            else:
                botones.append(
                    ft.Text("CALIFICADO", color="white", weight="bold")
                )

        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(reserva.servicio, color="white", weight="bold"),
                            ft.Text(f"Fecha: {reserva.fecha}", color="white70"),
                            ft.Text(
                                reserva.estado,
                                color="green" if estado == "COMPLETADA" or estado == "confirmada" else "red"
                            )
                        ]
                    ),
                    ft.Column(
                        botones + [
                            ft.TextButton(
                                "Cancelar",
                                on_click=lambda e: self.confirmar_cancelacion(reserva)
                            ) if estado == "CONFIRMADA" else ft.Container()
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=10,
            bgcolor="#1e1e1e",
            border_radius=15,
        )


    # BUILD

    def build(self):

        if not hasattr(self.page, "usuario_actual"):
            return ft.Text("Usuario no autenticado", color="red")

        cliente_id = self.page.usuario_actual.id

        reservas = self.manager.obtener_reservas_por_cliente(cliente_id)

        lista = ft.ListView(
            expand=True,
            spacing=10,
            controls=[self.tarjeta_reserva(r) for r in reservas],
        )

        layout = ft.Column(
            [
                ft.Text("Mis Reservas", size=30, weight="bold", color="white"),
                lista,
                ft.Button(
                    "Volver",
                    on_click=self.volver,
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(2, "white"),
                        color="white"
                    )
                )
            ],
            spacing=20,
            expand=True
        )

        return ft.Container(
            content=layout,
            expand=True,
            bgcolor="#121212",
            padding=20
        )