from database import get_connection_cursor

def create_monumento(
    codigo: int, 
    nombre: str, 
    tipo: str, 
    direccion: str, 
    codigo_postal: str, 
    longitud: float, 
    latitud: float, 
    descripcion: str, 
    localidad_codigo: int
) -> None:
    conn, cur = get_connection_cursor()
    with cur:
        cur.execute(
            """
            INSERT INTO Monumento (
                codigo, 
                nombre, 
                tipo, 
                direccion, 
                codigo_postal, 
                longitud, 
                latitud, 
                descripcion, 
                localidad_codigo
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (codigo, nombre, tipo, direccion, codigo_postal, longitud, latitud, descripcion, localidad_codigo),
        )
    with conn:
        conn.commit()

def get_monumento_by_codigo(codigo: int):
    _, cur = get_connection_cursor()
    with cur:
        cur.execute(
            """
            SELECT *
            FROM Monumento AS m
            WHERE m.codigo = ?
            """,
            codigo
        )
        return cur.fetchone()
    
def get_monumento_by_nombre(nombre: str):
    _, cur = get_connection_cursor()
    with cur:
        cur.execute(
            """
            SELECT *
            FROM Monumento AS m
            WHERE m.nombre = ?
            """,
            nombre
        )
        return cur.fetchone()
