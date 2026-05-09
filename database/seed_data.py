from services.usuario_service import UsuarioService


class SeedData:

    def __init__(self):
        # Servicio que maneja la lógica de usuarios
        self.service = UsuarioService()

    
    # CREAR USUARIOS DE PRUEBA
    
    def crear_usuarios(self):

        usuarios = [
            ("Jose", "admin@correo.com", "123", "admin"),
            ("Maicol", "emp@correo.com", "123", "empleado"),
            ("Santiago", "cli@correo.com", "123", "cliente"),
        ]

        # Iteramos y creamos cada usuario
        for nombre, email, password, rol in usuarios:
            self.service.crear_usuario(nombre, email, password, rol)
            try:
                self.service.crear_usuario(nombre, email, password, rol)
            except Exception:
                print(f"Usuario ya existe: {email}")

        print("Datos de prueba insertados correctamente")

    
    # MÉTODO PRINCIPAL
    
    def run(self):
        self.crear_usuarios()



# EJECUCIÓN

if __name__ == "__main__":
    seeder = SeedData()
    seeder.run()