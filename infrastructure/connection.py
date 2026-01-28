import os
import psycopg

def get_connection():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", 5432),
        dbname=os.getenv("POSTGRES_DB", "agents"),
        user=os.getenv("POSTGRES_USER", "agents"),
        password=os.getenv("POSTGRES_PASSWORD", "agents"),
    )
