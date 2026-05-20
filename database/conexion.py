import os
import sqlite3

class ConexionDB:

    DB_NAME = "CONECTAPP.db"
    _conn = None

    @staticmethod
    def get_conexion():

        if ConexionDB._conn is None:

            ConexionDB._conn = sqlite3.connect(
                ConexionDB.DB_NAME,
                check_same_thread=False,
                timeout=10
            )

            ConexionDB._conn.row_factory = sqlite3.Row

        return ConexionDB._conn