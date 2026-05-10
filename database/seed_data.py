from services.usuario_service import UsuarioService


class SeedData:

    def __init__(self):
        self.service = UsuarioService()

    def crear_usuarios(self):

        usuarios = [
            ("Jose", "admin@correo.com", "123", "admin"),
            ("Maicol", "emp@correo.com", "123", "empleado"),
            ("Santiago", "cli@correo.com", "123", "cliente"),
        ]

        for nombre, email, password, rol in usuarios:

            try:
                self.service.crear_usuario(nombre, email, password, rol)
                print(f"Usuario creado: {email}")

            except Exception:
                print(f"Usuario ya existe: {email}")

        print("Seed ejecutado correctamente")

    def run(self):
        self.crear_usuarios()


if __name__ == "__main__":
    seeder = SeedData()
    seeder.run()