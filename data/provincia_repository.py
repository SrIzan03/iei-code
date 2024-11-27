from database import get_connection_cursor

def create_provincia(codigo: int, nombre: str) -> None:
    conn, cur = get_connection_cursor()
    with cur:
        cur.execute(
            """
            INSERT INTO Provincia (codigo, nombre)
            VALUES (?, ?)
            """,
            (codigo, nombre),
        )
    with conn:
        conn.commit()

def get_provincia_by_codigo(codigo: int):
    _, cur = get_connection_cursor()
    with cur:
        cur.execute(
            """
            SELECT *
            FROM Provincia AS p
            WHERE p.codigo = ?
            """,
            codigo
        )
        return cur.fetchone()

def get_provincia_by_nombre(nombre: str):
    _, cur = get_connection_cursor()
    with cur:
        cur.execute(
            """
            SELECT *
            FROM Provincia AS p
            WHERE p.nombre = ?
            """,
            nombre
        )
        return cur.fetchone()
