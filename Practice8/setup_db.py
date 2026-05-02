from connect import connect

def execute_sql_file(filename, cursor):
    with open(filename, 'r', encoding='utf-8') as f:
        cursor.execute(f.read())

def setup():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20)
    );
    """)

    execute_sql_file("functions.sql", cur)
    execute_sql_file("procedures.sql", cur)

    conn.commit()
    cur.close()
    conn.close()

    print("Setup done using SQL files")

if __name__ == "__main__":
    setup()