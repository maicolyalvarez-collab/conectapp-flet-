from database.conexion import ConexionDB

class NotificacionesDAO:


    def crear_notificacion(self, cliente_id, mensaje):

        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO notificaciones
            (cliente_id, mensaje)

            VALUES (?, ?)
        """, (

            cliente_id,
            mensaje

        ))

        conn.commit()
        conn.close()

    def obtener_notificaciones(self, cliente_id):

        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT mensaje
            FROM notificaciones
            WHERE cliente_id = ?
            ORDER BY id DESC
        """, (cliente_id,))

        datos = cursor.fetchall()

        conn.close()

        return datos