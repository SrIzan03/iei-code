from database import get_connection_cursor
from models import Provincia

def create_provincia(p: Provincia):
    conn, cur = get_connection_cursor()
    try:
        cur.execute(
            """
            INSERT INTO Provincia (nombre)
            VALUES (?)
            """,
            (p.nombre,)
        )
        p.codigo = cur.lastrowid
    finally:
        conn.commit()

def get_provincia_by_codigo(codigo: int):
    _, cur = get_connection_cursor()
    try:
        cur.execute(
            """
            SELECT *
            FROM Provincia AS p
            WHERE p.codigo = ?
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
            WHERE p.nombre = ?
            """,
            (nombre,)
        )
        row = cur.fetchone()
        if row:
            return Provincia(codigo=row[0], nombre=row[1])
        return None
    finally:
        cur.close()