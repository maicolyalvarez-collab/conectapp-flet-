from database.conexion import ConexionDB

def init_db():
    conn = ConexionDB.get_conexion()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        rol TEXT NOT NULL,
        tipo_servicio TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        prestador_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        hora TEXT NOT NULL,
        servicio TEXT NOT NULL,
        estado TEXT NOT NULL DEFAULT 'CONFIRMADA',

        comentario_reserva TEXT,
        
        calificada TEXT DEFAULT 'NO CALIFICADA',

        FOREIGN KEY (cliente_id) REFERENCES usuarios(id),
        FOREIGN KEY (prestador_id) REFERENCES usuarios(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS horarios_base_empleados (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        prestador_id INTEGER NOT NULL,

        dia_semana TEXT NOT NULL,
        
        fecha TEXT NOT NULL,

        hora TEXT NOT NULL,
        
        estado TEXT DEFAULT 'DISPONIBLE',
        
        UNIQUE(prestador_id, fecha, hora),

        FOREIGN KEY (prestador_id)
        REFERENCES usuarios(id)

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calificaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reserva_id INTEGER,
        cliente_id INTEGER,
        prestador_id INTEGER,
        rating INTEGER,
        comentario_calificacion TEXT,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (reserva_id) REFERENCES reservas(id),

        FOREIGN KEY (cliente_id) REFERENCES usuarios(id),

        FOREIGN KEY (prestador_id) REFERENCES usuarios(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notificaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        usuario_id INTEGER NOT NULL,

        mensaje TEXT NOT NULL,

        leida INTEGER DEFAULT 0,

        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sesion (
        usuario_id INTEGER
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada correctamente")