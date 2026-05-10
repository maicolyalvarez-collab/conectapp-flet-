from database.conexion import ConexionDB
from models.usuario import Usuario


class UsuariosDAO:

    # LISTAR TODOS LOS USUARIOS
    def listar_todos(self):
        conn = ConexionDB.get_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            filas = cursor.fetchall()
            return filas
        finally:
            conn.close()

    # LISTAR SOLO PRESTADORES
    def listar_prestadores(self):
        conn = ConexionDB.get_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nombre, email, rol
                FROM usuarios
                WHERE rol = 'prestador'
            """)
            filas = cursor.fetchall()
            return filas
        finally:
            conn.close()

    # CREAR USUARIO
    def crear(self, usuario):
        conn = ConexionDB.get_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO usuarios (nombre, email, password, rol)
                VALUES (?, ?, ?, ?)
            """, (usuario.nombre, usuario.email, usuario.password, usuario.rol))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            conn.close()

    # BUSCAR POR EMAIL (CLAVE PARA LOGIN)
    def buscar_por_email(self, email):
        conn = ConexionDB.get_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nombre, email, password, rol
                FROM usuarios
                WHERE email = ?
            """, (email,))

            fila = cursor.fetchone()

            if fila:
                return Usuario(fila[1], fila[2], fila[3], fila[4], fila[0])

            return None

        finally:
            conn.close()