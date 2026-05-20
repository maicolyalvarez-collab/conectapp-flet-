from database.conexion import ConexionDB
from models.usuario import Usuario


class UsuariosDAO:

    def listar_todos(self):

        conn = ConexionDB.get_conexion()

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios")

        return cursor.fetchall()

    def listar_empleados(self):

        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, email, rol
            FROM usuarios
            WHERE rol = 'empleado'
            """)
        
        return cursor.fetchall()

    def listar_por_servicio(self, servicio):
        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nombre, tipo_servicio
            FROM usuarios
            WHERE rol = 'empleado'
            AND tipo_servicio = ?
        """, (servicio,))

        return cursor.fetchall()

    def crear(self, usuario):
        conn = ConexionDB.get_conexion()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO usuarios (
                    nombre, 
                    email, 
                    password, 
                    rol,
                    tipo_servicio
                )
                           
                VALUES (?, ?, ?, ?, ?)
                           
            """, (
                usuario.nombre,
                usuario.email, 
                usuario.password, 
                usuario.rol,
                usuario.tipo_servicio
            ))

            usuario_id = cursor.lastrowid

            conn.commit()

            return usuario_id

        except Exception as e:

            conn.rollback()
            raise e

    def buscar_por_email(self, email):
        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nombre, email, password, rol, tipo_servicio
            FROM usuarios
            WHERE email = ?
        """, (email,))

        fila = cursor.fetchone()

        if fila:

            return Usuario(
                fila[1],
                fila[2],
                fila[3],
                fila[4],
                fila[5],
                fila[0]
            )

        return None

    def obtener_por_id(self, usuario_id):

        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nombre, email, password, rol, tipo_servicio
            FROM usuarios
            WHERE id = ?
        """, (usuario_id,))

        fila = cursor.fetchone()

        if fila:
            return Usuario(
                fila[1],
                fila[2],
                fila[3],
                fila[4],
                fila[5],
                fila[0]
            )

        return None
