import flet as ft


# ========= COLORES =========

BACKGROUND = "#0F1117"
CARD = "#1A1D29"
PRIMARY = "#2563EB"

TEXT = "#FFFFFF"
TEXT_SECONDARY = "#9CA3AF"

BORDER = "#2A2F3D"


# ========= BOTONES =========

def menu_item(icon, text, on_click=None):

    return ft.Container(

        border_radius=12,
        padding=12,
        bgcolor=CARD,

        ink=True,

        content=ft.Row(

            controls=[

                ft.Icon(
                    icon,
                    color=TEXT,
                    size=22
                ),

                ft.Text(
                    text,
                    color=TEXT,
                    size=15,
                    weight="w500"
                )
            ]
        ),

        on_click=on_click
    )


# ========= DRAWER =========

def crear_drawer_cliente(page):

    page.drawer = ft.NavigationDrawer(

        bgcolor="#111827",
        width=280,

        controls=[

            ft.Container(

                padding=20,

                content=ft.Column(

                    spacing=20,

                    controls=[

                        # ===== LOGO =====

                        ft.Column(

                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                            controls=[

                                ft.Icon(
                                    ft.Icons.HOME_WORK_ROUNDED,
                                    size=70,
                                    color=PRIMARY
                                ),

                                ft.Text(
                                    "CONECTAPP",
                                    size=26,
                                    weight="bold",
                                    color=TEXT
                                ),

                                ft.Text(
                                    "Conectamos personas,\nimpulsamos trabajo",
                                    size=11,
                                    color=TEXT_SECONDARY,
                                    text_align="center"
                                )
                            ]
                        ),

                        ft.Divider(color=BORDER),

                        # ===== MENÚ =====

                        menu_item(
                            ft.Icons.HOME,
                            "Inicio"
                        ),

                        menu_item(
                            ft.Icons.CALENDAR_MONTH,
                            "Reservar servicio"
                        ),

                        menu_item(
                            ft.Icons.BOOK,
                            "Mis reservas"
                        ),

                        menu_item(
                            ft.Icons.STAR,
                            "Calificaciones"
                        ),

                        menu_item(
                            ft.Icons.MENU_BOOK,
                            "Manual de uso"
                        ),

                        menu_item(
                            ft.Icons.INFO,
                            "Acerca de"
                        ),

                        ft.Divider(color=BORDER),

                        menu_item(
                            ft.Icons.LOGOUT,
                            "Cerrar sesión"
                        )
                    ]
                )
            )
        ]
    )