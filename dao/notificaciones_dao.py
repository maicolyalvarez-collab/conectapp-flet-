from database.conexion import ConexionDB

class NotificacionesDAO:

    def crear_notificacion(self, usuario_id, mensaje):
        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO notificaciones
            (usuario_id, mensaje)
            VALUES (?, ?)
        """, (
            usuario_id,
            mensaje
        ))

        conn.commit()
        

    def obtener_notificaciones(self, usuario_id):
        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT mensaje, fecha, leida
            FROM notificaciones
            WHERE usuario_id = ?
            ORDER BY id DESC
        """, (usuario_id,))

        datos = cursor.fetchall()
        
        return datos
