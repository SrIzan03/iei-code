def get_db_connection():
    import psycopg2
    from psycopg2 import sql

    conn = psycopg2.connect(
        dbname="postgres",
        user="root",
        password="root",
        host="localhost",
        port="5431"
    )
    return conn

def get_monuments(filters):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = sql.SQL("SELECT * FROM Monumento WHERE TRUE")
    query_conditions = []

    if filters.get("nombre"):
        query_conditions.append(sql.SQL("nombre ILIKE %s").format(sql.Placeholder()))
    if filters.get("tipo"):
        query_conditions.append(sql.SQL("tipo ILIKE %s").format(sql.Placeholder()))
    if filters.get("localidad_codigo"):
        query_conditions.append(sql.SQL("localidad_codigo = %s").format(sql.Placeholder()))

    if query_conditions:
        query += sql.SQL(" AND ").join(query_conditions)

    cursor.execute(query, tuple(filters.values()))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def create_monumento(monumento_data):
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = sql.SQL("""
        INSERT INTO Monumento (nombre, tipo, direccion, codigo_postal, longitud, latitud, descripcion, localidad_codigo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """)
    
    cursor.execute(insert_query, (
        monumento_data['nombre'],
        monumento_data['tipo'],
        monumento_data['direccion'],
        monumento_data['codigo_postal'],
        monumento_data['longitud'],
        monumento_data['latitud'],
        monumento_data['descripcion'],
        monumento_data['localidad_codigo']
    ))

    conn.commit()
    cursor.close()
    conn.close()