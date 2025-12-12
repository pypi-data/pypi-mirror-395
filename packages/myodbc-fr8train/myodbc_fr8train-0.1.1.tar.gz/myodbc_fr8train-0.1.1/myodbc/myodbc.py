import pyodbc
import os
from dotenv import load_dotenv


def build_connection(env: str = None, override: bool = False) -> pyodbc.Connection:
    if env:
        load_dotenv(env, override=override)
    else:
        load_dotenv(override=override)

    SQL_SERVER = os.getenv("SQL_HOST")
    SQL_PORT = int(os.getenv("SQL_PORT"))
    SQL_USER = os.getenv("SQL_USER")
    SQL_PASSWORD = os.getenv("SQL_PASSWORD")
    SQL_DATABASE = os.getenv("SQL_DATABASE")

    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={SQL_SERVER},{SQL_PORT};"
        f"DATABASE={SQL_DATABASE};"
        f"UID={SQL_USER};"
        f"PWD={SQL_PASSWORD};"
        "Encrypt=yes;"
        "HostNameInCertificate=svsql1.database.windows.net;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    return pyodbc.connect(conn_str)


class MyODBC:
    connection: pyodbc.Connection
    cursor: pyodbc.Cursor

    def __init__(self, env: str = None, override: bool = False):
        self.connection = build_connection(env, override)
        self.cursor = self.connection.cursor()

    def translate(self, cursor: pyodbc.Cursor, rows: list[pyodbc.Row]):
        return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    # SIMPLE QUERY
    def sq(self, query: str) -> list[dict]:
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return self.translate(self.cursor, rows)

    # COMPLEX QUERY
    def cq(self, query: str, params: list) -> list[dict]:
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        return self.translate(self.cursor, rows)
