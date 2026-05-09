import sqlite3

class ConexionDB:

    DB_NAME = "BaseDeDatosPGC.db"

    @staticmethod
    def get_conexion():
        conn = sqlite3.connect(
            ConexionDB.DB_NAME,
            check_same_thread=False,
            timeout=10
        )
        conn.row_factory = sqlite3.Row
        return conn