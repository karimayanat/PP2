import csv
from connect import connect
conn = connect()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20)
);
""")
conn.commit()
cur.close()
conn.close()

def insert_from_csv(contacts.csv):
    conn = connect()
    cur = conn.cursor()
    with open(contacts.csv, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (row['name'], row['phone'])
            )
    conn.commit()
    cur.close()
    conn.close()

def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()

def update_contact():
    name = input("Enter name to update: ")
    new_phone = input("Enter new phone: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE contacts SET phone=%s WHERE name=%s",
        (new_phone, name)
    )
    conn.commit()
    cur.close()
    conn.close()

def query_contacts():
    filter_name = input("Enter name filter(or leave empty): ")
    conn = connect()
    cur = conn.cursor()
    if filter_name:
        cur.execute(
            "SELECT * FROM contacts",
            ('%' + filter_name + '%',)
        )
    else:
        cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def delete_contact():
    value = input("Enter name or phone to delete: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM contacts WHERE name=%s OR phone=%s",
        (value, value)
    )
    conn.commit()
    cur.close()
    conn.close()

def menu():
    while True:
        print("1. Insert from CSV")
        print("2. Insert from console")
        print("3. Update contact")
        print("4. Query contacts")
        print("5. Delete contact")
        print("0. Exit")
        choise = input("Choose: ")
        if choise == "1":
            insert_from_csv("contacts.csv")
        elif choise == "2":
            insert_from_console()
        elif choise == "3":
            update_contact()
        elif choise == "4":
            query_contacts()
        elif choise == "5":
            delete_contact()
        elif choise == "0":
            break
        else:
            print("Invalid choise")

if __name__ == "__main__":
    menu()