import flet as ft
from datetime import datetime

from dao.reservas_dao import ReservasDAO
from models.reserva import Reserva
from dao.notificaciones_dao import NotificacionesDAO
from dao.horarios_base_prestadores_dao import marcar_ocupado, obtener_horarios_disponibles
from dao.usuarios_dao import UsuariosDAO
from services.reserva_services import ReservaService


class ReservaView:

    def __init__(self, page: ft.Page, usuario_actual):
        self.page = page
        self.usuario_actual = usuario_actual

        self.paso = 1

        self.servicio_seleccionado = None
        self.prestador_seleccionado = None

        self.fecha = None
        self.hora = None

        self.hora_seleccionada = None

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

    # ---------------- HELPERS ----------------

    def fecha(self):
        if not self.fecha:
            return None
        return datetime.strptime(self.fecha, "%Y-%m-%d").date()

    def hora(self):
        if not self.hora:
            return None
        return datetime.strptime(self.hora.strip(), "%H:%M").time()

    def usuario_valido(self):
        return self.usuario_actual is not None
    
    def error(self, mensaje):

        self.mensaje.value = mensaje
        self.mensaje.color = "red"   # opcional pero recomendable centralizarlo
        self.page.update()
    
    def clear_error(self):
        self.mensaje.value = ""
        self.page.update()


    def obtener_empleados(self):

        dao = UsuariosDAO()
        filas = dao.listar_por_servicio(self.servicio_seleccionado)

        return [
            {"id": f[0], "nombre": f[1], "tipo": f[2]}
            for f in filas
        ]

    
    # ---------------- HORARIOS ----------------
    
    def obtener_horarios_disponibles(self):

        return obtener_horarios_disponibles(

            self.prestador_seleccionado,
            self.fecha
        )

    def obtener_horas_ocupadas(self):

        dao = ReservasDAO()

        ocupadas = dao.obtener_por_prestador_y_fecha(
            self.prestador_seleccionado,
            self.fecha
        )

        return ocupadas
    
    def tiene_horarios_disponibles(self):

        horarios = self.obtener_horarios_disponibles()

        return any(
            h["hora"] not in self.obtener_horas_ocupadas()
            for h in horarios
        )

    # ---------------- PICKERS ----------------
    
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
    
    # ---------------- NAVIGATION ----------------
    
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
    
    def _base_button_style(self, color, bg=None, border=None, overlay=None):
        return ft.ButtonStyle(
            color=color,
            bgcolor=bg,
            side=border,
            overlay_color=overlay,
            shape=ft.RoundedRectangleBorder(radius=14),
            padding=20
        )
    
    # ---------------- BOTONES ----------------

    def botones_navegacion(
        self,
        continuar=None,
        mostrar_atras=True,
        mostrar_cancelar=True,
        mostrar_continuar=True,
        texto_continuar="Continuar"
    ):

        botones = []

        def style(color, bg=None, border=None, overlay=None):
            return self._base_button_style(
                color,
                bg,
                border,
                overlay
            )

        # ATRÁS
        if mostrar_atras:
            botones.append(
                ft.OutlinedButton(
                    "Atrás",
                    icon=ft.Icons.ARROW_BACK,
                    on_click=self.atras,
                    width=150,
                    height=50,
                    style=style(
                        "white",
                        border=ft.BorderSide(1.5, "#38bdf8")
                    )
                )
            )

        # CANCELAR
        if mostrar_cancelar:
            botones.append(
                ft.Button(
                    "Cancelar",
                    icon=ft.Icons.CLOSE,
                    on_click=self.cancelar_reserva,
                    width=150,
                    height=50,
                    style=style(
                        "#ef4444",
                        bg="#111827",
                        border=ft.BorderSide(1.2, "#7f1d1d"),
                        overlay="#450a0a"
                    )
                )
            )

        # CONTINUAR
        if mostrar_continuar and continuar:
            botones.append(
                ft.Button(
                    texto_continuar,
                    icon=ft.Icons.ARROW_FORWARD,
                    on_click=continuar,
                    width=150,
                    height=50,
                    style=style(
                        "white",
                        bg="#111827",
                        border=ft.BorderSide(1.2, "#374151"),
                        overlay="#2563eb"
                    )
                )
            )

        return ft.Row(
            botones,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
    
    
    def line(self):
        pasos = [
            "Servicio", "Prestador", "Fecha", 
            "Hora", "Comentario", "Confirmacion", "Éxito"
        ]

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
                ft.Column([
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
                ])   
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
    
    #VALIDACIONES PASOS
    
    def validar_paso_1(self, e):                        

        if not self.servicio_seleccionado:
            self.error("Selecciona un servicio")
            return

        self.clear_error()
        self.siguiente()

    def validar_paso_2(self, e):

        if not self.prestador_seleccionado:
            self.error("Selecciona un prestador")
            return

        self.clear_error()
        self.siguiente()
    

    def validar_paso_3(self, e):

        if not self.fecha:
            self.mensaje.value = "Debes seleccionar fecha"
            self.mensaje.color = "red"
            self.page.update()
            return

        valido, mensaje = ReservaService.validar_fecha(self.fecha)

        if not valido:
            self.mensaje.value = mensaje
            self.mensaje.color = "red"
            self.page.update()
            return

        if not self.tiene_horarios_disponibles():
            self.mensaje.value = "No hay horarios disponibles"
            self.mensaje.color = "red"
            self.page.update()
            return

        self.clear_error()
        self.siguiente()
        
        
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
            self.hora,
            "%H:%M"
        ).time()

        fecha_hora_reserva = datetime.combine(
            fecha_reserva,
            hora_reserva
        )

        if fecha_reserva == ahora.date():

            # comparar solo si es hoy
            if fecha_hora_reserva < ahora:
                self.error("No puedes reservar horarios pasados")
                return

        if fecha_reserva < ahora.date():
            self.error("No puedes seleccionar fechas pasadas")
            return

        self.clear_error()
        self.siguiente()


        valido, mensaje = (
            ReservaService.validar_fecha(
                self.fecha
            )
        )

        if not valido:

            self.error(mensaje)

            return

        if not self.tiene_horarios_disponibles():

            self.error(
                "No hay horarios disponibles "
                "para este prestador en esa fecha"
            )

            self.clear_error()
            self.page.update()

            return

        self.siguiente()

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


    def paso_2(self):

        empleados = self.obtener_empleados()

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


    def paso_4(self):

        horarios = self.obtener_horarios_disponibles()

        cards = []

        def seleccionar_hora(e):

            self.hora_seleccionada = e.control.data
            self.hora = self.hora_seleccionada
            self.recargar()

        for h in horarios:

            estado =h["estado"]

            disponible = estado == "DISPONIBLE"
            finalizada = estado == "FINALIZADA"
            confirmada = estado == "CONFIRMADA"
            
            seleccionado = self.hora_seleccionada == h["hora"]
            
            card = ft.Container(

                data=h["hora"],

                width=150,
                height=120,

                border_radius=15,

                bgcolor=(
                    "#2563eb" if seleccionado

                    else "#1e293b" if disponible

                    else "#1d4ed8" if finalizada

                    else "#3a3a3a"
                ),

                opacity=1 if disponible else 0.4,

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
                            "Seleccionado" if seleccionado 

                            else "Disponible" if disponible 
                            else "Finalizada" if finalizada
                            else "Ocupado",

                            color=(
                                "#22c55e" if seleccionado

                                else "#22c55e" if disponible 

                                else "#60a5fa" if finalizada
                                
                                else "red"
                            ),
                            size=12
                        )
                    ]
                ),

                on_click=seleccionar_hora if disponible else None
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

        if self.hora not in [
            h["hora"]
            for h in self.obtener_horarios_disponibles()
            if h["estado"] == "DISPONIBLE"
        ]:
            
            self.error("Horario no disponible")
            return
                
        if dao.existe_reserva(
            self.prestador_seleccionado,
            self.fecha,
            self.hora
        ):
            self.error("Ese horario ya fue reservado")
            return

        nueva = Reserva(

            servicio=self.servicio_seleccionado,
            prestador_id=self.prestador_seleccionado,
            fecha=self.fecha,
            hora=self.hora,
            cliente_id=self.page.usuario_actual.id
        )

        dao.agregar_reserva(nueva)

        print("FECHA ENVIADA:", self.fecha)
        print("HORA ENVIADA:", self.hora)
        print("PRESTADOR:", self.prestador_seleccionado)

        marcar_ocupado(
            self.prestador_seleccionado,
            self.fecha,
            self.hora
        )


        notificacion = NotificacionesDAO()

        notificacion.crear_notificacion(

            self.page.usuario_actual.id,

            f"Tu reserva con {self.prestador_seleccionado} fue agendada para el {self.fecha} a las {self.hora}"
        )

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

            expand=True,

            bgcolor="#070B14",

            padding=40,

            content=ft.Container(

                width=1200,

                padding=40,

                border_radius=30,

                bgcolor="#0B1120",

                shadow=ft.BoxShadow(
                    blur_radius=30,
                    spread_radius=1,
                    color="#00000055",
                    offset=ft.Offset(0, 8)
                ),

                content=ft.Column(

                    [
                        self.line(),
                        contenido
                    ],

                    spacing=40,

                    alignment=ft.MainAxisAlignment.CENTER,

                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        )
