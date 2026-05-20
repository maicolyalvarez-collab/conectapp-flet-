from dao.usuarios_dao import UsuariosDAO
from models.usuario import Usuario

class UsuarioService:

    def __init__(self):
        self.dao = UsuariosDAO()

    def crear_usuario(self, nombre, email, password, rol, tipo_servicio):
        
        existente = self.dao.buscar_por_email(email)

        if existente:
            print(f"Usuario ya existe: {email}")
            return

        usuario = Usuario(nombre, email, password, rol, tipo_servicio)
        self.dao.crear(usuario)