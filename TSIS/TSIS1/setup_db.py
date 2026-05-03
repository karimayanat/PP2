from connect import connect

def execute_sql_file(filename, cursor):
    with open(filename, "r", encoding="utf-8") as f:
        cursor.execute(f.read())

def setup_database():
    conn = connect()
    cur = conn.cursor()

    print("Resetting database...")

    cur.execute("DROP TABLE IF EXISTS phones CASCADE;")
    cur.execute("DROP TABLE IF EXISTS contacts CASCADE;")
    cur.execute("DROP TABLE IF EXISTS groups CASCADE;")

    cur.execute("""
    CREATE TABLE groups (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        birthday DATE,
        group_id INTEGER REFERENCES groups(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE phones (
        id SERIAL PRIMARY KEY,
        contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
        phone VARCHAR(20) NOT NULL,
        type VARCHAR(10) CHECK (type IN ('home','work','mobile'))
    );
    """)

    print("Tables created")

    try:
        execute_sql_file("functions.sql", cur)
        print("Functions loaded")
    except Exception as e:
        print("Functions load error:", e)

    try:
        execute_sql_file("procedures.sql", cur)
        print("Procedures loaded")
    except Exception as e:
        print("Procedures load error:", e)

    conn.commit()
    cur.close()
    conn.close()

    print("Database setup completed successfully!")

if __name__ == "__main__":
    setup_database()