from database.conexion import ConexionDB
from models.reserva import Reserva
from dao.calificaciones_dao import CalificacionesDAO


class ReservasDAO:

    def __init__(self):

        self.conn = ConexionDB.get_conexion()
        self.cursor = self.conn.cursor()

    # ---------------- AGREGAR RESERVA ----------------
    def agregar_reserva(self, reserva: Reserva):

        self.cursor.execute("""
            INSERT INTO reservas (
                servicio,
                prestador_id,
                fecha,
                hora,
                estado,
                cliente_id,
                comentario_reserva
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            reserva.servicio,
            reserva.prestador_id,
            reserva.fecha,
            reserva.hora,
            reserva.estado,
            reserva.cliente_id,
            reserva.comentario_reserva
        ))

        self.conn.commit()

    # ---------------- OBTENER RESERVAS CLIENTE ----------------
    def obtener_reservas_por_cliente(self, cliente_id):

        self.cursor.execute("""
            SELECT
                id,
                servicio,
                prestador_id,
                fecha,
                hora,
                estado,
                cliente_id,
                comentario_reserva
            FROM reservas
            WHERE cliente_id = ?
            ORDER BY fecha DESC
        """, (cliente_id,))

        filas = self.cursor.fetchall()

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
                    comentario_reserva=f[7]
                )
            )

        return reservas

    # ---------------- HORAS OCUPADAS ----------------
    def obtener_por_prestador_y_fecha(self, prestador_id, fecha):

        self.cursor.execute("""
            SELECT hora
            FROM reservas
            WHERE prestador_id = ?
            AND fecha = ?
        """, (prestador_id, fecha))

        filas = self.cursor.fetchall()

        return [f[0] for f in filas]

    # ---------------- ACTUALIZAR ESTADO ----------------
    def actualizar_estado(self, id_reserva, nuevo_estado):

        # actualizar estado
        self.cursor.execute("""
            UPDATE reservas
            SET estado = ?
            WHERE id = ?
        """, (nuevo_estado, id_reserva))

        # obtener cliente
        self.cursor.execute("""
            SELECT cliente_id
            FROM reservas
            WHERE id = ?
        """, (id_reserva,))

        resultado = self.cursor.fetchone()

        if resultado:

            cliente_id = resultado[0]

            # crear notificación
            mensaje = f"Tu reserva ahora está: {nuevo_estado}"

            self.cursor.execute("""
                INSERT INTO notificaciones (cliente_id, mensaje)
                VALUES (?, ?)
            """, (cliente_id, mensaje))

        self.conn.commit()

    # ---------------- CANCELAR RESERVA ----------------
    def cancelar_reserva(self, id_reserva):

        self.actualizar_estado(id_reserva, "Cancelada")

    # ---------------- GUARDAR CALIFICACIÓN ----------------
    def guardar_calificacion(self, id_reserva, rating, comentario):

        # obtener cliente y prestador
        self.cursor.execute("""
            SELECT cliente_id, prestador_id
            FROM reservas
            WHERE id = ?
        """, (id_reserva,))

        datos = self.cursor.fetchone()

        if datos:

            cliente_id = datos[0]
            prestador_id = datos[1]

            dao = CalificacionesDAO()

            dao.crear_calificacion(
                id_reserva,
                cliente_id,
                prestador_id,
                rating,
                comentario
            )

    # ---------------- CERRAR CONEXIÓN ----------------
    def cerrar(self):

        self.conn.close()