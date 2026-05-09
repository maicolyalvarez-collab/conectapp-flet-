#logica

from dao.usuarios_dao import UsuariosDAO

class AuthService:

    def __init__(self):
        self.dao = UsuariosDAO()

    def login(self, email, password):
        usuario = self.dao.buscar_por_email(email)

        if not usuario:
            return None

        if usuario.password != password:
            return None

        return usuario