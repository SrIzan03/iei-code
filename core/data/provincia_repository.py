from database import get_connection_cursor
from models import Provincia

def create_provincia(p: Provincia):
    conn, cur = get_connection_cursor()
    try:
        cur.execute(
            """
            INSERT INTO Provincia (nombre)
            VALUES (%s)
            RETURNING codigo
            """,
            (p.nombre,)
        )
        p.codigo = cur.fetchone()[0]
    finally:
        conn.commit()
        cur.close()

def get_provincia_by_codigo(codigo: int):
    _, cur = get_connection_cursor()
    try:
        cur.execute(
            """
            SELECT *
            FROM Provincia AS p
            WHERE p.codigo = %s
            """,
            codigo
        )
        return cur.fetchone()
    finally:
        cur.close()

def get_provincia_by_nombre(nombre: str) -> Provincia:
    _, cur = get_connection_cursor()
    try:
        cur.execute(
            """
            SELECT *
            FROM Provincia AS p
            WHERE p.nombre = %s
            """,
            (nombre,)
        )
        row = cur.fetchone()
        if row:
            return Provincia(codigo=row[0], nombre=row[1])
        return None
    finally:
        cur.close()