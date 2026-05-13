import flet as ft

def crear_drawer_cliente(page):
    page.drawer = ft.NavigationDrawer(
        bgcolor="#1a1c20",  # Un gris oscuro que resalte del fondo negro
        width=300,          # Ancho fijo para que no sea invisible
        controls=[
            # ... tus controles aquí ...
        ]
    )