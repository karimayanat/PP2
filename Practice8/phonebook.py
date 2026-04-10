from connect import connect

def insert_or_update():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()

def search_contacts():
    pattern = input("Enter search pattern: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def show_paginated():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()


def delete_contact():
    value = input("Enter name or phone to delete: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()
    cur.close()
    conn.close()

def menu():
    while True:
        print("\nPHONEBOOK MENU")
        print("1. Insert / Update contact")
        print("2. Search contacts")
        print("3. Show paginated")
        print("4. Delete contact")
        print("0. Exit")
        choice = input("Choose: ")
        if choice == "1":
            insert_or_update()
        elif choice == "2":
            search_contacts()
        elif choice == "3":
            show_paginated()
        elif choice == "4":
            delete_contact()
        elif choice == "0":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()