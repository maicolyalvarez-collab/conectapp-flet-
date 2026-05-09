from dao.usuarios_dao import UsuariosDAO
from models.usuario import Usuario

class UsuarioService:

    def __init__(self):
        self.dao = UsuariosDAO()

    def crear_usuario(self, nombre, email, password, rol):
        # verificar si ya existe
        existente = self.dao.buscar_por_email(email)

        if existente:
            print(f"Usuario ya existe: {email}")
            return

        usuario = Usuario(nombre, email, password, rol)
        self.dao.crear(usuario)