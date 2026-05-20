from database.conexion import ConexionDB


def crear_horarios_base(prestador_id):

    conn = ConexionDB.get_conexion()
    cursor = conn.cursor()

    #evita horarios duplicados  
    cursor.execute("""
    SELECT COUNT(*) 
    FROM horarios_base_empleados
    WHERE prestador_id = ?
    """, (prestador_id,))

    if cursor.fetchone()[0] > 0:
        conn.close()
        return 

    dias = [
        "lunes",
        "martes",
        "miercoles",
        "jueves",
        "viernes"
    ]

    horas = [
        "09:00 AM",
        "02:00 PM"
    ]

    for dia in dias:
        for hora in horas:

            try:
                cursor.execute("""
                    INSERT INTO horarios_base_empleados (
                        prestador_id,
                        dia_semana,
                        hora
                    )
                    VALUES (?, ?, ?)
                """, (prestador_id, dia, hora))

            except:
                # si ya existe, lo ignoras
                pass

    conn.commit()

def obtener_horarios_disponibles(
    prestador_id,
    fecha,
    dia_semana
):

    conn = ConexionDB.get_conexion()
    cursor = conn.cursor()

    # HORARIOS BASE
    cursor.execute("""
    SELECT hora
    FROM horarios_base_empleados

    WHERE prestador_id = ?
    AND dia_semana = ?
    """, (
        prestador_id,
        dia_semana
    ))

    horarios = cursor.fetchall()

    # HORARIOS OCUPADOS
    cursor.execute("""
    SELECT hora
    FROM reservas

    WHERE prestador_id = ?
    AND fecha = ?
    AND estado = 'CONFIRMADA'
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

        disponible = hora not in horas_ocupadas

        resultado.append({

            "hora": hora,

            "disponible": disponible

        })

    return resultado