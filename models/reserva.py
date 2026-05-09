class Reserva:
    def __init__(self, servicio, fecha, hora, cliente_id, estado="Confirmada", id=None, calificada=False):
        self.id = id
        self.servicio = servicio
        self.fecha = fecha
        self.hora = hora
        self.estado = estado
        self.cliente_id = cliente_id
        self.calificada = calificada

