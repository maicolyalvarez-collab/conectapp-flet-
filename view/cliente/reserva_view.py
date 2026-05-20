import flet as ft
from datetime import datetime
from dao.reservas_dao import ReservasDAO
from models.reserva import Reserva
from dao.notificaciones_dao import NotificacionesDAO
from dao.horarios_base_prestadores_dao import obtener_horarios_disponibles


class ReservaView:

    def __init__(self, page: ft.Page, usuario_actual):
        self.page = page
        self.usuario_actual = usuario_actual

        self.paso = 1

        self.servicio_seleccionado = None
        self.prestador_seleccionado = None

        self.fecha = None
        self.hora = None

        self.comentario =""


        self.fecha_text = ft.Text(
            "Fecha no seleccionada", 
            color="white70"
        )

        self.hora_text = ft.Text(
            "Hora no seleccionada", 
            color="white70"
        )

        self.mensaje = ft.Text(
            "", 
            color="red"
        )

        # pickers
        self.date_picker = ft.DatePicker(
            on_change=self.seleccionar_fecha
        )

        self.time_picker = ft.TimePicker(
            on_change=self.seleccionar_hora
        )

        self.page.overlay.extend([
            self.date_picker, 
            self.time_picker
        ])
    
        
    def cambiar_vista(self, vista):

        self.page.clean()

        self.page.add(vista)

        self.page.update()

    
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

        fecha_obj = datetime.strptime(
            self.fecha,
            "%Y-%m-%d"
        )

        dias = [
            "lunes",
            "martes",
            "miercoles",
            "jueves",
            "viernes",
            "sabado",
            "domingo"
        ]

        dia_semana = dias[
            fecha_obj.weekday()
        ]

        return obtener_horarios_disponibles(

            self.prestador_seleccionado,

            self.fecha,

            dia_semana
        )

    
    def tiene_horarios_disponibles(self):

        horarios = self.obtener_horarios_disponibles()

        return any(
            h["disponible"]
            for h in horarios
        )
    
    
    def abrir_fecha(self):
        self.date_picker.open = True
        self.page.update()

    def abrir_hora(self):
        self.time_picker.open = True
        self.page.update()

    def seleccionar_fecha(self, e):
        if e.control.value:

            self.fecha = e.control.value.strftime(
                "%Y-%m-%d"
            )

            self.fecha_text.value = (
                f"Fecha: {self.fecha}"
            )

            self.page.update()

    def seleccionar_hora(self, e):

        if e.control.value:

            self.hora = e.control.value.strftime(
                "%H:%M"
            )

            self.hora_text.value = (
                f"Hora: {self.hora}"
            )

            self.page.update()
    
    def volver(self, e):
        from view.cliente.home_cliente_view import HomeClienteView

        self.cambiar_vista(
            HomeClienteView(
                self.page,
                self.usuario_actual
            ).build()
        )

    def ir_reservas(self, e):
        from view.cliente.gestionar_reserva_view import GestionarReservaView


        self.cambiar_vista(

            GestionarReservaView(
                self.page,
                self.usuario_actual
            ).build()
        )
        
    
    def cancelar_reserva(self, e):

        from view.cliente.home_cliente_view import HomeClienteView

        self.cambiar_vista(

            HomeClienteView(
                self.page,
                self.usuario_actual
            ).build()
        )

        self.page.update()

    def botones_navegacion(
        self,

        continuar=None,

        mostrar_atras=True,

        mostrar_cancelar=True,

        mostrar_continuar=True,

        texto_continuar="Continuar"
    ):

        botones = []

        if mostrar_atras:

            botones.append(

                ft.OutlinedButton(

                    "Atrás",

                    icon=ft.Icons.ARROW_BACK,

                    on_click=self.atras,

                    width=150,
                    height=50,

                    style=ft.ButtonStyle(
                        color="white",
                        side=ft.BorderSide(
                            1.5,
                            "#38bdf8"
                        ),

                        shape=ft.RoundedRectangleBorder(
                            radius=14
                        ),

                        padding=20
                    )
                )
            )

        if mostrar_cancelar:

            botones.append(

                ft.Button(

                    "Cancelar",

                    icon=ft.Icons.CLOSE,

                    on_click=self.cancelar_reserva,

                    width=150,
                    height=50,

                    style=ft.ButtonStyle(

                        bgcolor="#111827",

                        color="#ef4444",

                        side=ft.BorderSide(
                            1.2,
                            "#7f1d1d"
                        ),

                        shape=ft.RoundedRectangleBorder(
                            radius=14
                        ),

                        overlay_color="#450a0a",

                        padding=20
                    )
                )
            )

        if mostrar_continuar and continuar:

            botones.append(

                ft.Container(

                    border_radius=14,

                    content=ft.Button(

                        texto_continuar,

                        icon=ft.Icons.ARROW_FORWARD,

                        on_click=continuar,

                        width=150,
                        height=50,

                        style=ft.ButtonStyle(

                            bgcolor="#111827",

                            color="white",

                            side=ft.BorderSide(
                                1.2,
                                "#374151"
                            ),

                            overlay_color="#2563eb",

                            shape=ft.RoundedRectangleBorder(
                                radius=14
                            ),

                            padding=20
                        )
                    )
                )
            )

        return ft.Row(

            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            controls=botones
        )
    
    
    def line(self):
        pasos = ["Servicio", 
                "Prestador", 
                "Fecha", 
                "Hora",
                "Comentario", 
                "Confirmacion",
                "Éxito"]

        items = []

        for i, nombre in enumerate(pasos, start=1):

            completado = self.paso > i

            actual = self.paso == i

            color = ( 
                "#38bdf8" 
                if (completado or actual) 
                else "#374151"
            )

            texto = ( 
                "✔" 
                if completado 
                else str(i)
            )

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
                        bgcolor= ("#38bdf8" 
                            if self.paso > i 
                            else "#374151"
                        )
                    )
                )

        return ft.Row(items, alignment=ft.MainAxisAlignment.CENTER)
    
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
                color=(
                    "#38bdf8" 
                    if seleccionado 
                    else "black"
                )
            ),
            on_click=lambda e: self.seleccionar_servicio(nombre)
        )

    def paso_1(self):
        return ft.Column(
            [
                ft.Text("Selecciona un plan", size=25, color="white"),
                
                ft.Container(height=40),

                ft.Row(
                    [
                        self.card("Limpieza general", "$250.000"),
                        self.card("Limpieza profunda", "$400.000"),
                        self.card("Limpieza en alturas", "$450.000"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                ft.Container(height=40),

                self.botones_navegacion(
                    continuar=self.validar_paso_1,
                    mostrar_atras=False
                ),

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


    def paso_2(self):

        from dao.usuarios_dao import UsuariosDAO

        dao = UsuariosDAO()
        filas = dao.listar_por_servicio(self.servicio_seleccionado)

        empleados = [
            {
                "id": fila[0],
                "nombre": fila[1],
                "tipo": fila[2]
            }
            for fila in filas
        ]

        def seleccionar_empleado(e):
            self.prestador_seleccionado = e.control.data
            self.recargar()

        cards = []

        for p in empleados:

            seleccionado = self.prestador_seleccionado == p["id"]

            cards.append(
                ft.Container(

                    data=p["id"],

                    width=160,
                    height=120,

                    bgcolor=(
                        "#2563eb" 
                        if seleccionado 
                        else "#1e293b"
                    ),

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
                            ),

                            ft.Text(
                                p["tipo"],
                                color="white70",
                                size=10
                            )
                        ]
                    ),
                    on_click=seleccionar_empleado
                )
            )

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

                self.botones_navegacion(
                    continuar=self.validar_paso_2
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

                self.botones_navegacion(
                    continuar=self.validar_paso_3
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

        from services.reserva_services import ReservaService

        valido, mensaje = (
            ReservaService.validar_fecha(
                self.fecha
            )
        )

        if not valido:

            self.mensaje.value = mensaje

            self.page.update()

            return

        if not self.tiene_horarios_disponibles():

            self.mensaje.value = (
                "No hay horarios disponibles "
                "para este prestador en esa fecha"
            )

            self.mensaje.color = "red"

            self.page.update()

            return

        self.siguiente()

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

                self.botones_navegacion(
                    continuar=self.validar_paso_4
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

        ahora = datetime.now()

        fecha_reserva = datetime.strptime(
            self.fecha,
            "%Y-%m-%d"
        ).date()

        hora_reserva = datetime.strptime(
            self.hora.strip().replace(" AM", "").replace(" PM", ""),
            "%H:%M"
        ).time()

        if fecha_reserva == ahora.date():

            fecha_hora_reserva = datetime.combine(
                fecha_reserva,
                hora_reserva
            )

            if fecha_hora_reserva <= ahora:

                self.mensaje.value = (
                    "No puedes reservar horarios pasados"
                )

                self.mensaje.color = "red"

                self.page.update()
                return

        self.mensaje.value = ""
        self.siguiente()
    
    def paso_5(self):

        comentario_input = ft.TextField(
            label="Comentario para el prestador",
            multiline=True,
            min_lines=4,
            max_lines=6,
            width=420,
            border_color="#38bdf8",
            color="white"
        )

        def continuar(e):

            self.comentario = comentario_input.value

            self.siguiente()

        return ft.Column(

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Text(
                    "¿Deseas dejar un comentario?",
                    size=28,
                    weight="bold",
                    color="white"
                ),

                ft.Text(
                    "Puedes agregar detalles adicionales para el prestador",
                    color="white70"
                ),

                ft.Container(height=20),

                comentario_input,

                ft.Container(height=30),

                self.botones_navegacion(
                    continuar=continuar
                )
            ]
        )
    

    def paso_6(self):

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

                self.botones_navegacion(
                    continuar=self.guardar_reserva,
                    texto_continuar="Confirmar Reserva"
                ),

                self.mensaje
            ]
        )


    def paso_7(self):

        return ft.Column(

            expand=True,
            scroll=ft.ScrollMode.ALWAYS,

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

                            ft.Text(
                                "¡Reserva confirmada!",
                                size=28,
                                weight="bold",
                                color="white"
                            ),

                            ft.Text(
                                "Tu servicio fue agendado correctamente",
                                color="white70",
                                text_align=ft.TextAlign.CENTER
                            ),

                            ft.Divider(color="white24"),

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
        self.paso = 7

        self.recargar()
   
    # BUILD
    
    def build(self):

        pasos = {

            1: self.paso_1,
            2: self.paso_2,
            3: self.paso_3,
            4: self.paso_4,
            5: self.paso_5,
            6: self.paso_6,
            7: self.paso_7
        }

        contenido = pasos[self.paso]()


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
