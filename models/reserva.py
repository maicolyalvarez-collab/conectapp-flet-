class Reserva:

    def __init__(self, servicio,
                prestador_id, fecha,
                hora, cliente_id,
                estado="CONFIRMADA",
                id=None, calificada=False
                ):

        self.id = id
        self.servicio = servicio
        self.prestador_id = prestador_id
        self.fecha = fecha
        self.hora = hora
        self.estado = estado
        self.cliente_id = cliente_id
        self.calificada = calificada

