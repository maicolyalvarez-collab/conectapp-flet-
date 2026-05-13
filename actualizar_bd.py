from database.conexion import ConexionDB

conn = ConexionDB.get_conexion()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS calificaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reserva_id INTEGER,
    cliente_id INTEGER,
    prestador_id INTEGER,
    rating INTEGER,
    comentario TEXT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Tabla calificaciones creada")

