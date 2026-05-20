from database.conexion import ConexionDB

class SesionDAO:

    def guardar(self, usuario_id):
        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM sesion")

        cursor.execute(
            "INSERT INTO sesion (usuario_id) VALUES (?)",
            (usuario_id,)
        )

        conn.commit()

    def obtener(self):
        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()

        cursor.execute("SELECT usuario_id FROM sesion")
        fila = cursor.fetchone()


        return fila[0] if fila else None

    def cerrar(self):
        conn = ConexionDB.get_conexion()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM sesion")

        conn.commit()