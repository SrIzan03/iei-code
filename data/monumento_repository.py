from database import get_connection_cursor
from models import Monumento

def create_monumento(m: Monumento) -> None:
    conn, cur = get_connection_cursor()
    try:
        cur.execute(
            """
            INSERT INTO Monumento (
                nombre, 
                tipo, 
                direccion, 
                codigo_postal, 
                longitud, 
                latitud, 
                descripcion, 
                localidad_codigo
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (m.nombre, m.tipo, m.direccion, m.codigo_postal, m.longitud, m.latitud, m.descripcion, m.localidad_cod),
        )
    finally:
        conn.commit()
    
def get_monumento_by_nombre(nombre: str):
    _, cur = get_connection_cursor()
    try:
        cur.execute(
            """
            SELECT *
            FROM Monumento AS m
            WHERE m.nombre = ?
            """,
            (nombre,)
        )
        return cur.fetchone()
    finally:
        cur.close()
