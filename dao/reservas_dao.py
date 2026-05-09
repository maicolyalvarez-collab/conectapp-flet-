from database.conexion import ConexionDB
from models.reserva import Reserva

class ReservasDAO:

    def agregar_reserva(self,reserva: Reserva):
        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO reservas (servicio, fecha, hora, estado, cliente_id)
        VALUES (?, ?, ?, ?, ?)
        """, (
            reserva.servicio,
            reserva.fecha, 
            reserva.hora, 
            reserva.estado, 
            reserva.cliente_id
        ))

        conn.commit()
        conn.close()
    
    def obtener_reservas_por_cliente(self, cliente_id):
        conn =ConexionDB.get_conexion()
        cursor= conn.cursor()
    
        cursor.execute("""
                       
            SELECT id, servicio, fecha, hora, estado, cliente_id, calificada
            FROM reservas
            WHERE cliente_id = ?
        """, (cliente_id,))

        filas = cursor.fetchall()
        conn.close()

        reservas = []

        for f in filas:
            reservas.append(
                Reserva(
                    id=f[0],
                    servicio=f[1],
                    fecha=f[2],
                    hora=f[3],
                    estado=f[4],
                    cliente_id=f[5],
                    calificada=bool(f[6])
                )
            )
        return reservas
    
    def cancelar_reserva(self, id_reserva):
        conn =ConexionDB.get_conexion()
        cursor = conn.cursor()

        cursor.execute(""" 
            UPDATE reservas
            SET estado= "Cancelada"
            WHERE id = ?
        """, (id_reserva,))
        
        conn.commit()
        conn.close
    
    def actualizar_estado(self, id_reserva, nuevo_estado):

        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()

        #ACTUALIZAR ESTADO
        cursor.execute("""
            UPDATE reservas
            SET estado = ?
            WHERE id = ?
        """, (nuevo_estado, id_reserva))

        # OBTENER CLIENTE DE ESA RESERVA
        cursor.execute("""
            SELECT cliente_id
            FROM reservas
            WHERE id = ?
        """, (id_reserva,))

        cliente_id = cursor.fetchone()[0]

        # CREAR NOTIFICACIÓN
        mensaje = f"Tu reserva ahora está: {nuevo_estado}"

        cursor.execute("""
            INSERT INTO notificaciones (cliente_id, mensaje)
            VALUES (?, ?)
        """, (cliente_id, mensaje))

        conn.commit()
        conn.close()

    def guardar_calificacion(self, id_reserva, rating, comentario):
        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE reservas
            SET rating = ?, comentario = ?, calificada = 1
            WHERE id = ?
        """, (rating, comentario, id_reserva))

        conn.commit()
        conn.close()