from database import get_connection_cursor
from models import Localidad

def create_localidad(l: Localidad) -> None:
    conn, cur = get_connection_cursor()
    try:
        cur.execute(
            """
            INSERT INTO Localidad (nombre, provincia_codigo)
            VALUES (%s, %s)
            RETURNING codigo
            """,
            (l.nombre, l.provincia_cod,),
        )
        l.codigo = cur.fetchone()[0]
    finally:
        conn.commit()
        cur.close()

def get_localidad_by_codigo(codigo: int):
    _, cur = get_connection_cursor()
    try:
        cur.execute(
            """
            SELECT *
            FROM Localidad AS l
            WHERE l.codigo = %s
            """,
            codigo
        )
    finally:
        return cur.fetchone()
    
def get_localidad_by_nombre(nombre: str) -> Localidad:
    _, cur = get_connection_cursor()
    try:
        cur.execute(
            """
            SELECT *
            FROM Localidad AS l
            WHERE l.nombre = %s
            """,
            (nombre,)
        )
        row = cur.fetchone()
        if row:
            return Localidad(codigo=row[0], nombre=row[1], provincia_cod=row[2])
        return None
    finally:
        cur.close()