from services.usuario_service import UsuarioService
from dao.horarios_base_prestadores_dao import crear_horarios_base

class SeedData:

    def __init__(self):
        self.service = UsuarioService()
        self.usuario_dao = self.service.dao

    def crear_usuarios(self):

        usuarios = [

            ("Jose", "admin@correo.com", "123", "admin", None),

            (
                "Maicol",
                "emp@correo.com",
                "123",
                "empleado",
                "Limpieza general"
            ),

            (
                "Laura",
                "emp2@correo.com",
                "123",
                "empleado",
                "Limpieza profunda"
            ),

            (
                "Carlos",
                "emp3@correo.com",
                "123",
                "empleado",
                "Limpieza en alturas"
            ),

            ("Santiago", "cli@correo.com", "123", "cliente", None),

            ("Maicol", "cli2@correo.com", "123", "cliente", None)
        ]

        for nombre, email, password, rol, tipo_servicio in usuarios:

            try:

                self.service.crear_usuario(
                    nombre,
                    email,
                    password,
                    rol,
                    tipo_servicio
                )

                print(f"Usuario creado: {email}")

                # SI ES EMPLEADO
                if rol == "empleado":

                    usuario = (
                        self.usuario_dao
                        .buscar_por_email(email)
                    )

                    crear_horarios_base(usuario.id)

                    print(
                        f"Horarios creados para: {nombre}"
                    )

            except Exception as e :
                
                print(f"ERROR REAL en {email}: {e}")

        print("Seed ejecutado correctamente")

    def run(self):
        self.crear_usuarios()


if __name__ == "__main__":
    seeder = SeedData()
    seeder.run()