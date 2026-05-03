import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import DB_CONFIG

def create_database():
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            database="postgres",
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_CONFIG["database"],))
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f'CREATE DATABASE {DB_CONFIG["database"]}')
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(e)

if __name__ == "__main__":
    create_database()