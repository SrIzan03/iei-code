from database import get_connection
from models.models import Provincia


def create_provincia(provincia: Provincia):
    conn = get_connection()
    with conn:
        conn.execute("INSERT INTO PROVINCIA")
