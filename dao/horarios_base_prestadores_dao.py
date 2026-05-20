from database.conexion import ConexionDB
from datetime import datetime, timedelta

def crear_horarios_base(prestador_id):

    conn = ConexionDB.get_conexion()
    cursor = conn.cursor()

    try:

        # <-- MODIFICAR AQUÍ
        # ELIMINAR HORARIOS ANTERIORES
        cursor.execute("""
        DELETE FROM horarios_base_empleados
        WHERE prestador_id = ?
        """, (prestador_id,))

        dias = [
            "lunes",
            "martes",
            "miercoles",
            "jueves",
            "viernes"
        ]

        horas = [
            "09:00",
            "14:00"
        ]

        # <-- MODIFICAR AQUÍ
        # CREAR FECHAS REALES
        hoy = datetime.now()

        # <-- MODIFICAR AQUÍ
        # GENERAR 30 DIAS
        for i in range(30):

            fecha_obj = hoy + timedelta(days=i)

            # 0=lunes 6=domingo
            weekday = fecha_obj.weekday()

            # <-- MODIFICAR AQUÍ
            # IGNORAR SABADO Y DOMINGO
            if weekday > 4:
                continue

            dia = dias[weekday]

            # <-- MODIFICAR AQUÍ
            # FORMATO YYYY-MM-DD
            fecha_str = fecha_obj.strftime("%Y-%m-%d")

            for hora in horas:

                cursor.execute("""
                    INSERT INTO horarios_base_empleados (
                        prestador_id,
                        dia_semana,
                        fecha,
                        hora,
                        estado
                    )
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    prestador_id,
                    dia,
                    fecha_str,  # <-- MODIFICAR AQUÍ
                    hora,
                    "DISPONIBLE"
                ))

                print(
                    f"INSERT OK -> "
                    f"{prestador_id} "
                    f"{fecha_str} "
                    f"{dia} "
                    f"{hora}"
                )

        conn.commit()

    except Exception as e:

        conn.rollback()

        print(
            "ERROR EN HORARIOS:",
            e
        )

def marcar_ocupado(
    prestador_id,
    fecha,
    hora
):

    conn = ConexionDB.get_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE horarios_base_empleados
        SET estado = 'OCUPADO'

        WHERE prestador_id = ?
        AND fecha = ?
        AND hora = ?
    """, (
        prestador_id,
        fecha,
        hora
    ))

    print(
        "FILAS ACTUALIZADAS:",
        cursor.rowcount
    )
        # <-- AGREGAR AQUÍ
    # MOSTRAR DATOS REALES EN BD
    cursor.execute("""
        SELECT
            prestador_id,
            fecha,
            hora,
            estado

        FROM horarios_base_empleados

        WHERE prestador_id = ?
    """, (prestador_id,))

    print(
        "DATOS BD:",
        cursor.fetchall()
    )

    conn.commit()

    print(
        "HORARIO OCUPADO:",
        prestador_id,
        fecha,
        hora
    )

def marcar_disponible(
    prestador_id,
    fecha,
    hora
):

    conn = ConexionDB.get_conexion()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE horarios_base_empleados
        SET estado = 'DISPONIBLE'

        WHERE prestador_id = ?
        AND fecha = ?
        AND hora = ?
    """, (
        prestador_id,
        fecha,
        hora
    ))

    conn.commit()

    print(
        "HORARIO DISPONIBLE:",
        prestador_id,
        fecha,
        hora
    )

def obtener_horarios_disponibles(
    prestador_id,
    fecha
):

    conn = ConexionDB.get_conexion()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT DISTINCT hora, estado
    FROM horarios_base_empleados

    WHERE prestador_id = ?
    AND fecha = ?
    """, (
        prestador_id,
        fecha
    ))

    horarios = cursor.fetchall()

    cursor.execute("""
    SELECT hora
    FROM reservas

    WHERE prestador_id = ?
    AND fecha = ?
    AND estado IN (
                'CONFIRMADA', 
                'FINALIZADA'
    )
    """, (
        prestador_id,
        fecha
    ))

    reservas = cursor.fetchall()

    horas_ocupadas = [
        reserva[0]
        for reserva in reservas
    ]

    resultado = []

    for horario in horarios:

        hora = horario[0]

        estado_bd = horario[1]

        disponible = (
            estado_bd == "DISPONIBLE"
            and hora not in horas_ocupadas
        )

        resultado.append({

            "hora": hora,

            "estado":
                "DISPONIBLE"
                if disponible
                else "OCUPADO"

        })

    return resultado