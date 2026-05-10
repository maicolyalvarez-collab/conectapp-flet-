from database.conexion import ConexionDB

def init_db():
    conn = ConexionDB.get_conexion()
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        rol TEXT NOT NULL
    )
    """)

    # Tabla de reservas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        prestador_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        hora TEXT NOT NULL,
        servicio TEXT NOT NULL,
        estado TEXT NOT NULL DEFAULT 'CONFIRMADA',

        rating INTEGER,
        comentario TEXT,
        calificada INTEGER DEFAULT 0,

        FOREIGN KEY (cliente_id) REFERENCES usuarios(id),
        FOREIGN KEY (prestador_id) REFERENCES usuarios(id)
    )
    """)

    # Tabla de horarios por prestador
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS horarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prestador_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        hora TEXT NOT NULL,
        estado TEXT NOT NULL DEFAULT 'DISPONIBLE',
        FOREIGN KEY (prestador_id) REFERENCES usuarios(id)
    )
    """)

    #tabla de notificaciones
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notificaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        mensaje TEXT
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada correctamente")
