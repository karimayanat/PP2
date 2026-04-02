import psycopg2
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="12345",
    host="127.0.0.1",
    port=5433
)
conn.autocommit = True
cur = conn.cursor()
cur.execute("CREATE DATABASE phonebook_db")
print("Database created")
cur.close()
conn.close()