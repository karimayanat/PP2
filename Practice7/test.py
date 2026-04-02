import psycopg2

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="12345",
        host="127.0.0.1",
        port=5433
    )
    print("OK")
except Exception as e:
    print(e)