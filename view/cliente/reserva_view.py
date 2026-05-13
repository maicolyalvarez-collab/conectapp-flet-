import flet as ft
from datetime import datetime
from dao.reservas_dao import ReservasDAO
from models.reserva import Reserva
from dao.notificaciones_dao import NotificacionesDAO


class ReservaView:

    def __init__(self, page: ft.Page, usuario_actual):
        self.page = page
        self.usuario_actual = usuario_actual

        # estado del flujo
        self.paso = 1

        # datos de la reserva
        self.servicio_seleccionado = None
        self.prestador_seleccionado = None
        self.fecha = None
        self.hora = None

        #horarios base
        self.horarios_fijos = ["09:00", "14:00"]

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

    def obtener_horarios_disponibles(self):

        dao = ReservasDAO()

        # ya es lista de strings
        ocupados = dao.obtener_por_prestador_y_fecha(
            self.prestador_seleccionado,
            self.fecha
        )

        resultado = []

        for h in self.horarios_fijos:

            resultado.append({
                "hora": h,
                "disponible": h not in ocupados
            })

        return resultado
    
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

        view = GestionarReservaView(self.page, self.usuario_actual)

        self.page.controls.clear()
        self.page.add(view.build())
        self.page.update()
        
    def volver(self, e):
        from view.cliente.home_cliente_view import HomeClienteView

        self.page.clean()
        self.page.add(HomeClienteView(self.page, self.usuario_actual).build())
        self.page.update()

    
    # LINE 
    
    def line(self):
        pasos = ["Servicio", "Prestador", "Fecha", "Hora", "Confirmacion", "Éxito"]

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

        # EJEMPLO: esto luego lo conectas a BD
        prestadores = [
            {"id": 1, "nombre": "Ana López", "tipo": "Básico"},
            {"id": 2, "nombre": "Carlos Ruiz", "tipo": "Avanzado"},
            {"id": 3, "nombre": "Laura Gómez", "tipo": "Pro"},
        ]

        # filtrar por servicio seleccionado
        filtrados = [
            p for p in prestadores
            if p["tipo"] == self.servicio_seleccionado
        ]

        def seleccionar_prestador(e):
            self.prestador_seleccionado = e.control.data
            self.recargar()

        cards = []

        for p in filtrados:

            seleccionado = self.prestador_seleccionado == p["id"]

            card = ft.Container(

                data=p["id"],

                width=160,
                height=120,

                bgcolor="#2563eb" if seleccionado else "#1e293b",

                border_radius=15,

                shadow=ft.BoxShadow(
                    blur_radius=20,
                    color="#38bdf8" if seleccionado else "black"
                ),

                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[

                        ft.Icon(ft.Icons.PERSON, color="white"),

                        ft.Text(
                            p["nombre"],
                            color="white",
                            weight="bold"
                        )
                    ]
                ),

                on_click=seleccionar_prestador
            )

            cards.append(card)

        return ft.Column(

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Text("Selecciona un prestador", size=25, color="white"),
                ft.Text(
                    f"Servicio: {self.servicio_seleccionado}",
                    color="white70"
                ),

                ft.Container(height=20),

                ft.Row(
                    wrap=True,
                    spacing=15,
                    run_spacing=15,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=cards
                ),

                ft.Container(height=30),

                ft.Row(

                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,

                    controls=[

                        ft.OutlinedButton(
                            "Atrás",
                            on_click=self.atras
                        ),

                        ft.Button(
                            "Continuar",
                            on_click=self.validar_paso_2
                        )
                    ]
                ),
                self.mensaje
            ]
        )
    
    # VALIDAR PASO 2

    def validar_paso_2(self, e):

        if not self.prestador_seleccionado:
            self.mensaje.value = "Selecciona un prestador"
            self.page.update()
            return

        self.mensaje.value = ""
        self.siguiente()

    # PASO 3 (FECHA)

    def paso_3(self):

        return ft.Column(

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Text(
                    "Selecciona la fecha",
                    size=30,
                    weight="bold",
                    color="white"
                ),

                ft.Text(
                    f"Prestador: {self.prestador_seleccionado}",
                    color="white70"
                ),

                ft.Container(height=20),

                ft.Button(
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

                ft.Container(height=30),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[

                        ft.OutlinedButton(
                            "Atrás",
                            on_click=self.atras
                        ),

                        ft.Button(
                            "Continuar",
                            on_click=self.validar_paso_3
                        )
                    ]
                ),

                self.mensaje
            ]
        )


    # VALIDAR PASO 3
    def validar_paso_3(self, e):

        if not self.fecha:
            self.mensaje.value = "Debes seleccionar una fecha"
            self.mensaje.color = "red"
            self.page.update()
            return

        fecha_sel = datetime.strptime(self.fecha, "%Y-%m-%d").date()
        hoy = datetime.now().date()

        #no fechas pasadas
        if fecha_sel < hoy:
            self.mensaje.value = "No puedes seleccionar una fecha pasada"
            self.page.update()
            return

        #solo lunes a viernes
        if fecha_sel.weekday() > 4:
            self.mensaje.value = "Solo se permiten días entre semana"
            self.page.update()
            return

        self.mensaje.value = ""

        # avanzar a horarios
        self.siguiente()

    # PASO 4 CONFIRMACIÓN 

    def paso_4(self):

        horarios = self.obtener_horarios_disponibles()

        cards = []

        def seleccionar_hora(e):

            self.hora = e.control.data

            for c in cards:
                c.bgcolor = "#1e293b"

            e.control.bgcolor = "#2563eb"

            self.page.update()

        for h in horarios:

            card = ft.Container(

                data=h["hora"],

                width=150,
                height=120,

                border_radius=15,

                bgcolor="#1e293b" if h["disponible"] else "#3a3a3a",
                opacity=1 if h["disponible"] else 0.4,

                shadow=ft.BoxShadow(
                    blur_radius=18,
                    color="black"
                ),

                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[

                        ft.Icon(ft.Icons.ACCESS_TIME, color="white"),

                        ft.Text(
                            h["hora"],
                            color="white",
                            weight="bold"
                        ),

                        ft.Text(
                            "Disponible" if h["disponible"] else "Ocupado",
                            color="#22c55e" if h["disponible"] else "red",
                            size=12
                        )
                    ]
                ),

                on_click=seleccionar_hora if h["disponible"] else None
            )

            cards.append(card)

        return ft.Column(

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Text("Selecciona horario", size=28, color="white"),

                ft.Text(f"Prestador: {self.prestador_seleccionado}", color="white70"),

                ft.Text(f"Fecha: {self.fecha}", color="white70"),

                ft.Container(height=20),

                ft.Row(
                    wrap=True,
                    spacing=15,
                    run_spacing=15,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=cards
                ),

                ft.Container(height=30),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[

                        ft.OutlinedButton("Atrás", on_click=self.atras),

                        ft.Button("Continuar", on_click=self.validar_paso_4)
                    ]
                ),

                self.mensaje
            ]
        )
    def validar_paso_4(self, e):

        if not self.hora:
            self.mensaje.value = "Selecciona un horario"
            self.mensaje.color = "red"
            self.page.update()
            return

        self.mensaje.value = ""
        self.siguiente()
    
    # PASO 5 CONFIRMAR RESERVA

    def paso_5(self):

        return ft.Column(

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Text(
                    "Confirmar reserva",
                    size=30,
                    weight="bold",
                    color="white"
                ),

                ft.Container(
                    width=420,
                    padding=20,
                    border_radius=20,
                    bgcolor="#1e293b",

                    content=ft.Column(

                        spacing=15,

                        controls=[

                            ft.Text(
                                "Resumen",
                                size=22,
                                weight="bold",
                                color="white"
                            ),

                            ft.Divider(color="white24"),

                            ft.Text(
                                f"Servicio: {self.servicio_seleccionado}",
                                color="white70",
                                size=16
                            ),

                            ft.Text(
                                f"Prestador: {self.prestador_seleccionado}",
                                color="white70",
                                size=16
                            ),

                            ft.Text(
                                f"Fecha: {self.fecha}",
                                color="white70",
                                size=16
                            ),

                            ft.Text(
                                f"Hora: {self.hora}",
                                color="white70",
                                size=16
                            ),
                        ]
                    )
                ),

                ft.Container(height=25),

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

                        ft.Button(
                            "Confirmar Reserva",
                            icon=ft.Icons.CHECK,
                            on_click=self.guardar_reserva,

                            style=ft.ButtonStyle(
                                bgcolor="#2563eb",
                                color="white",
                                padding=20
                            )
                        )
                    ]
                ),

                self.mensaje
            ]
        )


    # GUARDAR RESERVA

    def guardar_reserva(self, e):

        if not hasattr(self.page, "usuario_actual"):
            return

        dao = ReservasDAO()

        # VALIDAR SI YA EXISTE ESA RESERVA
        ocupadas = dao.obtener_por_prestador_y_fecha(
            self.prestador_seleccionado,
            self.fecha
        )

        if self.hora in ocupadas:

            self.mensaje.value = "Ese horario ya fue reservado"
            self.mensaje.color = "red"

            self.page.update()
            return

        nueva = Reserva(

            servicio=self.servicio_seleccionado,

            prestador_id=self.prestador_seleccionado,

            fecha=self.fecha,

            hora=self.hora,

            cliente_id=self.page.usuario_actual.id
        )

        # GUARDAR EN BD
        dao.agregar_reserva(nueva)

        # CREAR NOTIFICACIÓN
        notificacion = NotificacionesDAO()

        notificacion.crear_notificacion(

            self.page.usuario_actual.id,

            f"Tu reserva con {self.prestador_seleccionado} fue agendada para el {self.fecha} a las {self.hora}"
        )

        # IR A ÉXITO
        self.paso = 6

        self.recargar()
    
    # PASO 6 → ÉXITO

    def paso_exito(self):

        return ft.Column(

            expand=True,

            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Container(
                    width=420,
                    padding=30,
                    border_radius=25,
                    bgcolor="#1e293b",

                    shadow=ft.BoxShadow(
                        blur_radius=25,
                        color="black"
                    ),

                    content=ft.Column(
                        spacing=25,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                        controls=[

                            # ICONO
                            ft.Container(
                                width=100,
                                height=100,
                                border_radius=50,
                                bgcolor="#22c55e",
                                alignment=ft.Alignment.CENTER,

                                content=ft.Icon(
                                    ft.Icons.CHECK,
                                    size=50,
                                    color="white"
                                )
                            ),

                            # TITULO
                            ft.Text(
                                "¡Reserva confirmada!",
                                size=28,
                                weight="bold",
                                color="white"
                            ),

                            # SUBTEXTO
                            ft.Text(
                                "Tu servicio fue agendado correctamente",
                                color="white70",
                                text_align=ft.TextAlign.CENTER
                            ),

                            ft.Divider(color="white24"),

                            # RESUMEN
                            ft.Container(
                                padding=20,
                                border_radius=15,
                                bgcolor="#111827",

                                content=ft.Column(
                                    spacing=12,

                                    controls=[

                                        ft.Text(
                                            "Resumen",
                                            size=20,
                                            weight="bold",
                                            color="white"
                                        ),

                                        ft.Text(
                                            f"Servicio: {self.servicio_seleccionado}",
                                            color="white70"
                                        ),

                                        ft.Text(
                                            f"Prestador: {self.prestador_seleccionado}",
                                            color="white70"
                                        ),

                                        ft.Text(
                                            f"Fecha: {self.fecha}",
                                            color="white70"
                                        ),

                                        ft.Text(
                                            f"Hora: {self.hora}",
                                            color="white70"
                                        )
                                    ]
                                )
                            ),

                            # MENSAJE
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,

                                controls=[

                                    ft.Icon(
                                        ft.Icons.EMAIL,
                                        color="#38bdf8",
                                        size=18
                                    ),

                                    ft.Text(
                                        "Revisa tus notificaciones",
                                        color="white54",
                                        size=12
                                    )
                                ]
                            ),

                            # BOTONES
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=15,

                                controls=[

                                    ft.Button(
                                        "Inicio",
                                        icon=ft.Icons.HOME,
                                        on_click=self.volver,

                                        style=ft.ButtonStyle(
                                            bgcolor="#2563eb",
                                            color="white",
                                            padding=18
                                        )
                                    ),

                                    ft.OutlinedButton(
                                        "Mis reservas",
                                        icon=ft.Icons.CALENDAR_MONTH,
                                        on_click=self.ir_reservas,

                                        style=ft.ButtonStyle(
                                            color="white",
                                            side=ft.BorderSide(1, "#38bdf8"),
                                            padding=18
                                        )
                                    )
                                ]
                            )
                        ]
                    )
                )
            ]
        )
   
    # BUILD
    
    def build(self):

        if self.paso == 1:
            contenido = self.paso_1()

        elif self.paso == 2:
            contenido = self.paso_2()

        elif self.paso == 3:
            contenido = self.paso_3()

        elif self.paso == 4:
            contenido = self.paso_4()
        
        elif self.paso ==5:
            contenido = self.paso_5()
        
        elif self.paso == 6:
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
