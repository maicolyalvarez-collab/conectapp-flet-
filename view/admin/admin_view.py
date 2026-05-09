#home administrador

import flet as ft

class HomeAdminView:
    def build(self):

        print("BUILD HOME ADMIN EJECUTADO")

        return ft.Container(
            expand=True,
            bgcolor="#121212",
            padding=20,

            content=ft.Column(
                spacing=20,
                controls=[
                    #header
                    ft.Container(
                        content=ft.Text(
                            "PANEL DE ADMINISTRACIÓN",
                            size=30,
                            weight="bold",
                            color="WHITE"
                        ),
                        padding=10,
                    ),

                    #CARDS DE INFORMACION

                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            self.card("USUARIOS", 
                                    "Gestiona los usuarios de la plataforma", 
                                    #ft.icons.PERSON, 
                                    #self.ir_usuarios
                                    ),

                            self.card("VENTAS", "Gestiona las ventas de la plataforma", 
                                    #ft.icons.RECEIPT, 
                                    #self.ir_ventas
                                    ),
                            self.card("ACTIVOS", 
                                    "Gestiona los activos de la plataforma",
                                    #ft.icons.STORAGE, 
                                    #self.ir_activos
                                    ),
                        ]
                    ),


                    #ACTIVIDAD

                    ft.Container(
                        bgcolor="#1e1e1e",
                        border_radius=20,
                        padding=15,
                        content=ft.Column(
                            controls=[
                                ft.Text("ACTIVIDAD RECIENTE", 
                                        size=20, 
                                        weight="bold", 
                                        color="white"),

                                ft.Text("- NUEVO USUARIO: Maicol", 
                                        color="white70"),

                                ft.Text("- VENTA REGISTRADA: #12345", 
                                        color="white70"),
                            ],
                        )
                    )
                ]
            )
        )
    
    #CARD REUTILIZABLE

    def card(self,titulo, valor):
        return ft.Container(
            width=250,
            height=150,
            bgcolor="#1e1e1e",
            border_radius=20,
            padding=15,

            # 🔥 AQUÍ VA EL SHADOW
            shadow=ft.BoxShadow(
                blur_radius=15,
                color="white",   # ⚠️ mejor negro para efecto realista
                spread_radius=1
            ),

            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,

                controls=[
                    ft.Text(
                        titulo,
                        size=18,
                        weight="bold",
                        color="white"
                    ),

                    ft.Text(
                        valor,
                        size=12,
                        color="white70"
                    )
                ]
            )   
        )
    
    def caja(self,titulo,valor):
        return ft.Container(
            content= ft.Column([
                ft.Text(titulo),
                ft.Text(valor, size=18)
            ]),
            bgcolor="white",
            padding=10,
            width=140
        )