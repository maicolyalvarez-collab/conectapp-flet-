class Calificacion:

    def __init__(
        self,
        reserva_id,
        cliente_id,
        prestador_id,
        rating,
        comentario,
        id=None
    ):

        self.id = id
        self.reserva_id = reserva_id
        self.cliente_id = cliente_id
        self.prestador_id = prestador_id
        self.rating = rating
        self.comentario = comentario