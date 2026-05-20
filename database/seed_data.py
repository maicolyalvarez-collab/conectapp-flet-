from models.usuario import Usuario
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

                usuario = Usuario(
                    nombre,
                    email,
                    password,
                    rol,
                    tipo_servicio
                )

                usuario_id = self.usuario_dao.crear(usuario)

                print(f"Usuario creado: {email}")

                #usuario_db = self.usuario_dao.buscar_por_email(email)

                if usuario_id is None:

                    print(f"❌ No se encontró usuario: {email}")
                    continue

                if rol == "empleado":
                    crear_horarios_base(usuario_id)
                    print(f"Horarios creados para: {nombre}")

            except Exception as e :
                
                print(f"ERROR REAL en {email}: {e}")

        print("Seed ejecutado correctamente")

    def run(self):
        self.crear_usuarios()


if __name__ == "__main__":
    seeder = SeedData()
    seeder.run()