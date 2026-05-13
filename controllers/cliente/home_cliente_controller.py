from dao.notificaciones_dao import NotificacionesDAO

class HomeClienteController:

    def __init__(self, page):
        self.page = page
        self.dao = NotificacionesDAO()

    def obtener_notificaciones(self, usuario_id):

        datos = self.dao.obtener_notificaciones(usuario_id)

        # 🔥 lógica de datos (opcional)
        return datos