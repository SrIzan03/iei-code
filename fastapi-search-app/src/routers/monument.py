from fastapi import APIRouter, HTTPException, Query
import psycopg2
from psycopg2 import sql
from typing import List, Optional

router = APIRouter()

DATABASE_URL = "postgresql://root:root@localhost:5431/postgres"

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@router.get("/monuments/", response_model=List[dict])
def search_monuments(
    codigo_postal: Optional[int] = Query(None),
    tipo: Optional[str] = Query(None),
    localidad: Optional[str] = Query(None),
    provincia: Optional[str] = Query(None)
):
    query = """
        SELECT Monumento.* 
        FROM Monumento
        JOIN Localidad ON Monumento.localidad_codigo = Localidad.codigo
        JOIN Provincia ON Localidad.provincia_codigo = Provincia.codigo
        WHERE TRUE
    """
    params = []

    if codigo_postal:
        query += " AND Monumento.codigo_postal ILIKE %s"
        params.append(f"%{codigo_postal}%")
    if tipo:
        query += " AND Monumento.tipo ILIKE %s"
        params.append(f"%{tipo}%")
    if localidad:
        query += " AND Localidad.nombre ILIKE %s"
        params.append(f"%{localidad}%")
    if provincia:
        query += " AND Provincia.nombre ILIKE %s"
        params.append(f"%{provincia}%")

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            monuments = [dict(zip(columns, row)) for row in results]
        return monuments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()