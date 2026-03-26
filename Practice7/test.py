import psycopg2

try:
    conn = psycopg2.connect(
        dbname="phonebook_db",
        user="postgres",
        password="1234",
        host="127.0.0.1",
        port=5432
    )
    print("OK")
except Exception as e:
    print(e)