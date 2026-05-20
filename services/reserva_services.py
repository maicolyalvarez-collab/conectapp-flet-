from datetime import datetime


class ReservaService:

    @staticmethod
    def validar_fecha(fecha):

        fecha_sel = datetime.strptime(
            fecha,
            "%Y-%m-%d"
        ).date()

        hoy = datetime.now().date()

        # no fechas pasadas
        if fecha_sel < hoy:

            return False, (
                "No puedes seleccionar "
                "una fecha pasada"
            )

        # lunes a viernes
        if fecha_sel.weekday() > 4:

            return False, (
                "Solo se permiten "
                "días entre semana"
            )

        return True, ""