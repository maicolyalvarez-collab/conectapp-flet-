from database.conexion import ConexionDB


class HorariosDAO:

    # INSERTAR HORARIOS
    def insertar_horario(self, prestador_id, fecha, hora):
        conn = ConexionDB.get_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO horarios (prestador_id, fecha, hora, estado)
                VALUES (?, ?, ?, 'DISPONIBLE')
            """, (prestador_id, fecha, hora))
            conn.commit()
        finally:
            conn.close()

    # OBTENER HORARIOS POR PRESTADOR Y FECHA
    def obtener_horarios(self, prestador_id, fecha):
        conn = ConexionDB.get_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, hora, estado
                FROM horarios
                WHERE prestador_id = ? AND fecha = ?
            """, (prestador_id, fecha))
            return cursor.fetchall()
        finally:
            conn.close()

    # MARCAR HORARIO COMO OCUPADO
    def ocupar_horario(self, prestador_id, fecha, hora):
        conn = ConexionDB.get_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE horarios
                SET estado = 'OCUPADO'
                WHERE prestador_id = ? AND fecha = ? AND hora = ?
            """, (prestador_id, fecha, hora))
            conn.commit()
        finally:
            conn.close()