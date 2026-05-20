from database.conexion import ConexionDB

class CalificacionesDAO:

    def crear_calificacion(
        self,
        reserva_id,
        cliente_id,
        prestador_id,
        rating,
        comentario_calificacion
    ):
        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO calificaciones
            (
                reserva_id,
                cliente_id,
                prestador_id,
                rating,
                comentario_calificacion
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            reserva_id,
            cliente_id,
            prestador_id,
            rating,
            comentario_calificacion
        ))

        conn.commit()
        

    def listar_por_cliente(self, cliente_id):
        """Devuelve todas las calificaciones hechas por un cliente."""
        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.id, c.reserva_id, c.rating, c.comentario_calificacion, c.fecha,
                   u.nombre AS prestador_nombre
            FROM calificaciones c
            JOIN usuarios u ON c.prestador_id = u.id
            WHERE c.cliente_id = ?
            ORDER BY c.fecha DESC
        """, (cliente_id,))

        resultados = cursor.fetchall()
        
        return resultados

    def listar_por_prestador(self, prestador_id):
        """Devuelve todas las calificaciones recibidas por un prestador."""
        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.id, c.reserva_id, c.rating, c.comentario_calificacion, c.fecha,
                   u.nombre AS cliente_nombre
            FROM calificaciones c
            JOIN usuarios u ON c.cliente_id = u.id
            WHERE c.prestador_id = ?
            ORDER BY c.fecha DESC
        """, (prestador_id,))

        resultados = cursor.fetchall()
        
        return resultados
