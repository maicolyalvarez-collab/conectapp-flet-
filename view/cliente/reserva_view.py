import flet as ft
from dao.reservas_dao import ReservasDAO
from models.reserva import Reserva
from dao.notificaciones_dao import NotificacionesDAO


class ReservaView:

    def __init__(self, page: ft.Page):
        self.page = page

        # estado del flujo
        self.paso = 1

        # datos de la reserva
        self.servicio_seleccionado = None
        self.fecha = ""
        self.hora = ""

        # textos dinámicos
        self.fecha_text = ft.Text("Fecha no seleccionada", color="white70")
        self.hora_text = ft.Text("Hora no seleccionada", color="white70")
        self.mensaje = ft.Text("", color="red")

        # pickers
        self.date_picker = ft.DatePicker(on_change=self.seleccionar_fecha)
        self.time_picker = ft.TimePicker(on_change=self.seleccionar_hora)

        self.page.overlay.extend([self.date_picker, self.time_picker])

    
    # CONTROL DE FLUJO
    
    def siguiente(self):
        self.paso += 1
        self.recargar()

    def atras(self):
        self.paso -= 1
        self.recargar()

    def recargar(self):
        self.page.clean()
        self.page.add(self.build())
        self.page.update()

    #
    # PICKERS
    
    def abrir_fecha(self):
        self.date_picker.open = True
        self.page.update()

    def abrir_hora(self):
        self.time_picker.open = True
        self.page.update()

    def seleccionar_fecha(self, e):
        if e.control.value:
            self.fecha = e.control.value.strftime("%Y-%m-%d")
            self.fecha_text.value = f"Fecha: {self.fecha}"
            self.page.update()

    def seleccionar_hora(self, e):
        if e.control.value:
            self.hora = e.control.value.strftime("%H:%M")
            self.hora_text.value = f"Hora: {self.hora}"
            self.page.update()

    def ir_reservas(self, e):
        from view.cliente.gestionar_reserva_view import GestionarReservaView

        self.page.clean()
        self.page.add(GestionarReservaView(self.page, self.usuario_actual).build())
        self.page.update()

    
    # LINE 
    
    def line(self):
        pasos = ["Servicio", "Fecha", "Confirmar", "Confirmacion"]

        items = []
        for i, nombre in enumerate(pasos, start=1):

            completado = self.paso > i
            actual = self.paso == i

            color = "#38bdf8" if (completado or actual) else "#374151"

            texto = "✔" if completado else str(i)

            items.append(
                ft.Column(
                    [
                        ft.Container(
                            width=35,
                            height=35,
                            border_radius=50,
                            bgcolor=color,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Text(
                                texto,
                                color="black" if (completado or actual) else "white",
                                weight="bold"
                            ),
                        ),
                        ft.Text(nombre, size=11, color="white70")
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

            if i < len(pasos):
                items.append(
                    ft.Container(
                        width=50,
                        height=2,
                        bgcolor="#38bdf8" if self.paso > i else "#374151"
                    )
                )

        return ft.Row(items, alignment=ft.MainAxisAlignment.CENTER)

    
    # PASO 1
    
    def seleccionar_servicio(self, nombre):
        self.servicio_seleccionado = nombre
        self.recargar()

    def card(self, nombre, precio):
        seleccionado = self.servicio_seleccionado == nombre

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(nombre, color="white", weight="bold"),
                    ft.Text(precio, color="white70")
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),

            width=140,
            height=120,
            bgcolor="#1e293b",
            border_radius=15,

            shadow=ft.BoxShadow(
                blur_radius=20,
                color="#38bdf8" if seleccionado else "black"
            ),
            on_click=lambda e: self.seleccionar_servicio(nombre)
        )

    def paso_1(self):
        return ft.Column(
            [
                ft.Text("Selecciona un plan", size=25, color="white"),

                ft.Row(
                    [
                        self.card("Básico", "$20.000"),
                        self.card("Avanzado", "$35.000"),
                        self.card("Pro", "$50.000"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                ft.Button("Continuar", on_click=self.validar_paso_1),

                self.mensaje
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def validar_paso_1(self, e):

        if not self.servicio_seleccionado:
            self.mensaje.value = "Selecciona un servicio"
            self.page.update()
            return

        self.mensaje.value = ""
        self.siguiente()

    
    # PASO 2
    
  # PASO 2

    def paso_2(self):

        horarios = [
            "08:00 AM",
            "09:00 AM",
            "10:00 AM",
            "11:00 AM",
            "02:00 PM",
            "03:00 PM",
            "04:00 PM",
            "05:00 PM",
        ]

        cards_horarios = []

        def seleccionar_horario(e):

            self.hora = e.control.data
            self.hora_text.value = f"Hora: {self.hora}"

            # RESET VISUAL
            for c in cards_horarios:
                c.bgcolor = "#1e293b"

                c.shadow = ft.BoxShadow(
                    blur_radius=18,
                    color="black"
                )

            # CARD SELECCIONADA
            e.control.bgcolor = "#2563eb"

            e.control.shadow = ft.BoxShadow(
                blur_radius=25,
                color="#38bdf8"
            )

            self.page.update()

        # CREAR TARJETAS
        for hora in horarios:

            seleccionado = self.hora == hora

            card = ft.Container(

                data=hora,

                width=140,
                height=120,

                border_radius=18,

                bgcolor="#2563eb" if seleccionado else "#1e293b",

                shadow=ft.BoxShadow(
                    blur_radius=25 if seleccionado else 18,
                    color="#38bdf8" if seleccionado else "black"
                ),

                animate=300,

                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                    controls=[

                        ft.Icon(
                            ft.Icons.ACCESS_TIME_FILLED,
                            color="#38bdf8",
                            size=28
                        ),

                        ft.Text(
                            hora,
                            color="white",
                            size=18,
                            weight="bold"
                        ),

                        ft.Text(
                            "Disponible",
                            color="#22c55e",
                            size=12
                        )
                    ]
                ),

                on_click=seleccionar_horario
            )

            cards_horarios.append(card)

        return ft.Column(

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Text(
                    "Selecciona fecha y hora",
                    size=30,
                    weight="bold",
                    color="white"
                ),

                ft.Text(
                    "Elige el horario que prefieras",
                    color="white54"
                ),

                ft.Container(height=15),

                # BOTON FECHA
                ft.ElevatedButton(
                    "Elegir fecha",
                    icon=ft.Icons.CALENDAR_MONTH,
                    on_click=lambda e: self.abrir_fecha(),

                    style=ft.ButtonStyle(
                        bgcolor="#2563eb",
                        color="white",
                        padding=15
                    )
                ),

                self.fecha_text,

                ft.Container(height=25),

                # TARJETAS HORARIOS
                ft.Row(
                    wrap=True,
                    spacing=15,
                    run_spacing=15,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=cards_horarios
                ),

                ft.Container(height=30),

                # BOTONES
                ft.Row(

                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,

                    controls=[

                        ft.OutlinedButton(
                            "Atrás",
                            on_click=lambda e: self.atras(),

                            style=ft.ButtonStyle(
                                color="white",
                                side=ft.BorderSide(1, "#38bdf8"),
                                padding=15
                            )
                        ),

                        ft.ElevatedButton(
                            "Continuar",
                            icon=ft.Icons.ARROW_FORWARD,
                            on_click=self.validar_paso_2,

                            style=ft.ButtonStyle(
                                bgcolor="#2563eb",
                                color="white",
                                padding=15
                            )
                        )
                    ]
                ),

                self.mensaje
            ]
        )
    # VALIDAR PASO 2

    def validar_paso_2(self, e):

        # VALIDAR FECHA
        if not self.fecha:

            self.mensaje.value = "Selecciona una fecha"
            self.mensaje.color = "red"

            self.page.update()
            return

        # VALIDAR HORA
        if not self.hora:

            self.mensaje.value = "Selecciona un horario"
            self.mensaje.color = "red"

            self.page.update()
            return

        # LIMPIAR MENSAJE
        self.mensaje.value = ""

        # SIGUIENTE PASO
        self.siguiente()

    
    # PASO 3 
    
    def paso_3(self):
        return ft.Column(
            [
                ft.Text("Confirmación", size=25, color="white"),

                ft.Container(
                    padding=15,
                    bgcolor="#1e1e1e",
                    border_radius=15,
                    content=ft.Column(
                        [
                            ft.Text(f"SERVICIO: {self.servicio_seleccionado}", color="white"),
                            ft.Text(f"FECHA: {self.fecha}", color="white70"),
                            ft.Text(f"HORA: {self.hora}", color="white70"),
                        ]
                    )
                ),

                ft.Row(
                    [
                        ft.TextButton("Atrás", on_click=self.atras),
                        ft.Button("Confirmar", on_click=self.guardar_reserva)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    
    # GUARDAR
    
    # GUARDAR

    def guardar_reserva(self, e):

        if not hasattr(self.page, "usuario_actual"):
            return

        dao = ReservasDAO()

        nueva = Reserva(
            servicio=self.servicio_seleccionado,
            fecha=self.fecha,
            hora=self.hora,
            cliente_id=self.page.usuario_actual.id
        )

        # GUARDAR RESERVA
        dao.agregar_reserva(nueva)

        # CREAR NOTIFICACION
        noti_dao = NotificacionesDAO()

        noti_dao.crear_notificacion(

            self.page.usuario_actual.id,

            f"Tu reserva de {self.servicio_seleccionado} fue agendada para {self.fecha} a las {self.hora}"
        )

        # MOSTRAR EXITO
        self.paso = 4
        self.recargar()

    
    # PASO 4 CONFIRMACIÓN 
    
    def paso_exito(self):
        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,

            controls=[

                # CONTENEDOR PRINCIPAL
                ft.Container(
                    width=320,
                    padding=25,
                    border_radius=20,
                    bgcolor="#1a1a2e", 

                    shadow=ft.BoxShadow(
                        blur_radius=25,
                        color="white"
                    ),

                    content=ft.Column(
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                        controls=[

                            # ICONO
                            ft.Container(
                                width=90,
                                height=90,
                                border_radius=50,
                                bgcolor="#04873B",
                                alignment=ft.Alignment.CENTER,
                                content=ft.Icon(ft.Icons.CHECK, size=45, color="white"),
                                shadow=ft.BoxShadow(
                                    blur_radius=20,
                                    color="#004E20"
                                )
                            ),

                            # TEXTO PRINCIPAL
                            ft.Text(
                                "¡Reserva confirmada!",
                                size=24,
                                weight="bold",
                                color="white"
                            ),

                            # TEXTO SECUNDARIO
                            ft.Text(
                                "Tu servicio fue agendado correctamente",
                                size=13,
                                color="white70",
                                text_align=ft.TextAlign.CENTER
                            ),

                            # 🔹 SUB-CONTENEDOR (DETALLES)
                            ft.Container(
                                padding=15,
                                border_radius=15,
                                bgcolor="#111827",

                                content=ft.Column(
                                    spacing=8,
                                    controls=[
                                        ft.Text("Detalles", weight="bold", color="white"),

                                        ft.Text(f"SERVICIO: {self.servicio_seleccionado}", color="white70"),
                                        ft.Text(f"FECHA: {self.fecha}", color="white70"),
                                        ft.Text(f"HORA: {self.hora}", color="white70"),
                                    ]
                                )
                            ),

                            # MENSAJE DE CORREO
                            ft.Container(
                                padding=10,
                                border_radius=10,
                                bgcolor="#2a2a2a",

                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Icon(ft.Icons.EMAIL, size=18, color="#7B61FF"),
                                        ft.Text(
                                            "Revisa tu correo",
                                            color="white70",
                                            size=12
                                        )
                                    ]
                                )
                            ),

                            # BOTÓN PRINCIPAL
                            ft.Button(
                                "Volver al inicio",
                                on_click=self.volver,
                                style=ft.ButtonStyle(
                                    bgcolor="#7B61FF",
                                    color="white",
                                    padding=15,
                                    shape=ft.RoundedRectangleBorder(radius=10)
                                )
                            ),

                            # BOTÓN SECUNDARIO
                            ft.TextButton(
                                "Ver mis reservas",
                                on_click=self.ir_reservas
                            )
                        ]
                    )
                )
            ]
        )

    def volver(self, e):
        from view.cliente.home_cliente_view import HomeClienteView

        self.page.clean()
        self.page.add(HomeClienteView(self.page).build())
        self.page.update()

   
    # BUILD
    
    def build(self):

        if self.paso == 1:
            contenido = self.paso_1()
        elif self.paso == 2:
            contenido = self.paso_2()
        elif self.paso == 3:
            contenido = self.paso_3()
        elif self.paso == 4:
            contenido = self.paso_exito()

        return ft.Container(
            content=ft.Column(
                [
                    self.line(),
                    contenido
                ],
                spacing=40,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            expand=True,
            bgcolor="#121212",
            padding=40
        )