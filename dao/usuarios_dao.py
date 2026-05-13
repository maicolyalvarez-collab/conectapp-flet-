from database.conexion import ConexionDB
from models.usuario import Usuario


class UsuariosDAO:

    # ---------------- LISTAR TODOS ----------------
    def listar_todos(self):
        conn = ConexionDB.get_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            return cursor.fetchall()
        finally:
            conn.close()

    # ---------------- LISTAR PRESTADORES ----------------
    def listar_prestadores(self):
        conn = ConexionDB.get_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nombre, email, rol
                FROM usuarios
                WHERE rol = 'prestador'
            """)
            return cursor.fetchall()
        finally:
            conn.close()

    # ---------------- CREAR USUARIO ----------------
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

    # ---------------- BUSCAR POR EMAIL (LOGIN) ----------------
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
                return Usuario(
                    fila[1],  # id
                    fila[2],  # nombre
                    fila[3],  # email
                    fila[4],  # password
                    fila[0]   # rol
                )

            return None

        finally:
            conn.close()

    # ---------------- BUSCAR POR ID (SESIÓN) ----------------
    def obtener_por_id(self, usuario_id):
        conn = ConexionDB.get_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nombre, email, password, rol
                FROM usuarios
                WHERE id = ?
            """, (usuario_id,))

            fila = cursor.fetchone()

            if fila:
                return Usuario(
                    fila[1],  # id
                    fila[2],  # nombre
                    fila[3],  # email
                    fila[4],  # password
                    fila[0]   # rol
                )
            print(fila)

            return None

        finally:
            conn.close()