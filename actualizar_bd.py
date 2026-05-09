from database.conexion import ConexionDB

conn = ConexionDB.get_conexion()
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE reservas ADD COLUMN rating INTEGER")
except:
    print("rating ya existe")

try:
    cursor.execute("ALTER TABLE reservas ADD COLUMN comentario TEXT")
except:
    print("comentario ya existe")

try:
    cursor.execute("ALTER TABLE reservas ADD COLUMN calificada INTEGER DEFAULT 0")
except:
    print("calificada ya existe")

conn.commit()
conn.close()

print("Base de datos actualizada correctamente")

