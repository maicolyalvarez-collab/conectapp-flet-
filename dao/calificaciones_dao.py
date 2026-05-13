from database.conexion import ConexionDB


class CalificacionesDAO:

    def crear_calificacion(
        self,
        reserva_id,
        cliente_id,
        prestador_id,
        rating,
        comentario
    ):

        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO calificaciones
            (reserva_id, cliente_id, prestador_id, rating, comentario)
            VALUES (?, ?, ?, ?, ?)
        """, (
            reserva_id,
            cliente_id,
            prestador_id,
            rating,
            comentario
        ))

        conn.commit()
        conn.close()