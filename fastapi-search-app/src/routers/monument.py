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
    nombre: Optional[str] = Query(None),
    tipo: Optional[str] = Query(None),
    localidad_codigo: Optional[int] = Query(None)
):
    query = "SELECT * FROM Monumento WHERE TRUE"
    params = []

    if nombre:
        query += " AND nombre ILIKE %s"
        params.append(f"%{nombre}%")
    if tipo:
        query += " AND tipo ILIKE %s"
        params.append(f"%{tipo}%")
    if localidad_codigo is not None:
        query += " AND localidad_codigo = %s"
        params.append(localidad_codigo)

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