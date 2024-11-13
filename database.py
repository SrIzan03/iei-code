# database.py
import sqlite3

def get_connection():
    conn = sqlite3.connect("my_database.db")
    return conn

def create_database():
    conn = get_connection()
    with conn:
        with open('DB_INIT.sql', 'r') as file:
            sql_script = file.read()
        conn.executescript(sql_script)

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