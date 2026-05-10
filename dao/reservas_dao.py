from database.conexion import ConexionDB
from models.reserva import Reserva
import sqlite3

class ReservasDAO:
    def __init__(self):
        self.conexion =sqlite3.connect("CONECTAPP.db")
        self.cursor = self.conexion.cursor()

    def agregar_reserva(self,reserva: Reserva):
        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO reservas (servicio, prestador_id, fecha, hora, estado, cliente_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            reserva.servicio,
            reserva.prestador_id,
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
                       
            SELECT id, servicio, prestador_id, fecha, hora, estado, cliente_id, calificada
            FROM reservas
            WHERE cliente_id = ?
            ORDER BY fecha DESC
        """, (cliente_id,))

        filas = cursor.fetchall()
        conn.close()

        reservas = []

        for f in filas:
            reservas.append(
                Reserva(
                    id=f[0],
                    servicio=f[1],
                    prestador_id=f[2],
                    fecha=f[3],
                    hora=f[4],
                    estado=f[5],
                    cliente_id=f[6],
                    calificada=bool(f[7])
                )
            )
        return reservas
    
    def obtener_por_prestador_y_fecha(self, prestador_id, fecha):

        conn = self.conexion
        cursor = conn.cursor()

        query = """
            SELECT hora
            FROM reservas
            WHERE prestador_id = ?
            AND fecha = ?
        """

        cursor.execute(query, (prestador_id, fecha))

        filas = cursor.fetchall()

        # devolver solo lista de horas
        return [f[0] for f in filas]
    
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