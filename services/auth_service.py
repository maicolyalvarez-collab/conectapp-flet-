from dao.usuarios_dao import UsuariosDAO


class AuthService:

    def __init__(self):
        self.dao = UsuariosDAO()

    def login(self, email, password):

        usuario = self.dao.buscar_por_email(email)

        # VALIDAR USUARIO
        if not usuario:
            return None

        # VALIDAR PASSWORD
        if str(usuario.password).strip() != str(password).strip():
            return None

        return usuario    