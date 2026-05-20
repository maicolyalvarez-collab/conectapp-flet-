from database.conexion import ConexionDB
from models.reserva import Reserva
from dao.calificaciones_dao import CalificacionesDAO
from dao.notificaciones_dao import NotificacionesDAO


class ReservasDAO:

    def __init__(self):

        self.conn = ConexionDB.get_conexion()
        self.cursor = self.conn.cursor()

    def agregar_reserva(self, reserva: Reserva):

        self.cursor.execute("""
            INSERT INTO reservas (
                servicio,
                prestador_id,
                fecha,
                hora,
                estado,
                cliente_id,
                comentario_reserva,
                calificada
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            reserva.servicio,
            reserva.prestador_id,
            reserva.fecha,
            reserva.hora,
            reserva.estado,
            reserva.cliente_id,
            reserva.comentario_reserva,
            "NO CALIFICADA"
        ))

        self.conn.commit()

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
                comentario_reserva,
                calificada
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
                    comentario_reserva=f[7],
                    calificada=f[8]
                )
            )

        return reservas

    def obtener_por_prestador_y_fecha(self, prestador_id, fecha):

        self.cursor.execute("""
            SELECT hora
            FROM reservas
            WHERE prestador_id = ?
            AND fecha = ?
        """, (prestador_id, fecha))

        filas = self.cursor.fetchall()

        return [f[0] for f in filas]


    def actualizar_estado(self, reserva_id, nuevo_estado):
        print("ACTUALIZANDO ESTADO")

        # ACTUALIZAR ESTADO
        self.cursor.execute("""
            UPDATE reservas
            SET estado = ?
            WHERE id = ?
        """, (nuevo_estado, reserva_id))

        # OBTENER CLIENTE_ID
        self.cursor.execute("""
            SELECT cliente_id
            FROM reservas
            WHERE id = ?
        """, (reserva_id,))

        resultado = self.cursor.fetchone()

        # VALIDAR RESULTADO
        if resultado:

            cliente_id = resultado[0]

            mensaje = f"Tu reserva fue {nuevo_estado}"

            # CREAR NOTIFICACION
            noti_dao = NotificacionesDAO()

            noti_dao.crear_notificacion(
                cliente_id,
                mensaje
            )

        # GUARDAR CAMBIOS
        self.conn.commit()

    def cancelar_reserva(self, id_reserva):

        self.actualizar_estado(
            id_reserva,
            "CANCELADA"
        )

    # GUARDAR CALIFICACION
    def guardar_calificacion(
        self,
        id_reserva,
        rating,
        comentario
    ):

        # OBTENER IDS
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

            # CREAR CALIFICACION
            dao.crear_calificacion(
                id_reserva,
                cliente_id,
                prestador_id,
                rating,
                comentario
            )

            # MARCAR COMO CALIFICADA
            self.cursor.execute("""
                UPDATE reservas
                SET calificada = 'CALIFICADA'
                WHERE id = ?
            """, (id_reserva,))

            self.conn.commit()
