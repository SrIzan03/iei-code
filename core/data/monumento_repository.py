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
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (m.nombre, m.tipo, m.direccion, m.codigo_postal, float(m.longitud), float(m.latitud), m.descripcion, m.localidad_cod),
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
            WHERE m.nombre = %s
            """,
            (nombre,)
        )
        return cur.fetchone()
    finally:
        cur.close()

def get_all_monuments():
    _, cur = get_connection_cursor()
    try:
        cur.execute(
            """
            SELECT *
            FROM Monumento
            """
        )
        return cur.fetchall()
    finally:
        cur.close()

def get_filtered_monuments(localidad=None, codigo_postal=None, provincia=None, tipo=None):
    _, cur = get_connection_cursor()
    try:
        query = """
            SELECT m.nombre, m.tipo, m.direccion, m.codigo_postal, 
                   m.longitud, m.latitud, m.descripcion, l.nombre as localidad,
                   p.nombre as provincia
            FROM Monumento m
            JOIN Localidad l ON m.localidad_codigo = l.codigo
            JOIN Provincia p ON l.provincia_codigo = p.codigo
            WHERE 1=1
        """
        params = []

        if localidad:
            query += " AND l.nombre ILIKE %s"
            params.append(f"%{localidad}%")
        if codigo_postal:
            query += " AND m.codigo_postal LIKE %s"
            params.append(f"%{codigo_postal}%")
        if provincia:
            query += " AND p.nombre ILIKE %s"
            params.append(f"%{provincia}%")
        if tipo:
            query += " AND m.tipo = %s"
            params.append(tipo)

        cur.execute(query, params)
        return cur.fetchall()
    finally:
        cur.close()
