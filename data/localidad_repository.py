from database import get_connection_cursor

def create_localidad(codigo: int, nombre: str, codigo_localidad) -> None:
    conn, cur = get_connection_cursor()
    with cur:
        cur.execute(
            """
            INSERT INTO Localidad (codigo, nombre, localidad_codigo)
            VALUES (?, ?, ?)
            """,
            (codigo, nombre, codigo_localidad),
        )
    with conn:
        conn.commit()

def get_localidad_by_codigo(codigo: int):
    _, cur = get_connection_cursor()
    with cur:
        cur.execute(
            """
            SELECT *
            FROM Localidad AS l
            WHERE l.codigo = ?
            """,
            codigo
        )
        return cur.fetchone()
    
def get_localidad_by_nombre(nombre: str):
    _, cur = get_connection_cursor()
    with cur:
        cur.execute(
            """
            SELECT *
            FROM Localidad AS l
            WHERE l.nombre = ?
            """,
            nombre
        )
        return cur.fetchone()
