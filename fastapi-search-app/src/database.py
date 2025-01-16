from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://root:root@localhost:5431/postgres"  # Change this to your database URL

engine = create_engine(DATABASE_URL)

def get_connection():
    connection = engine.connect()
    return connection

def close_connection(connection):
    connection.close()