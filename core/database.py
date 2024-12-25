import os
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def get_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME', 'my_database'),
        user=os.getenv('DB_USER', 'my_user'),
        password=os.getenv('DB_PASSWORD', 'my_password'),
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432')
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn

def create_database():
    conn = get_connection()
    with conn:
        with open('DB_INIT.sql', 'r') as file:
            sql_script = file.read()
        with conn.cursor() as cur: 
            cur.execute(sql.SQL(sql_script))

def get_connection_cursor():
    conn = get_connection()
    return (conn, conn.cursor())

def clean_database():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DROP SCHEMA IF EXISTS public CASCADE;")
            cur.execute("CREATE SCHEMA public;")
        conn.commit()
    except Exception as e:
        print(f"An error occurred while cleaning the database: {e}")
        conn.rollback()
    finally:
        conn.close()

# CRUD operations
# def create_user(name: str, email: str):
#     conn = get_connection()
#     with conn:
#         conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))

# def get_user(user_id: int):
#     conn = get_connection()
#     with conn:
#         user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
#     return dict(user) if user else None