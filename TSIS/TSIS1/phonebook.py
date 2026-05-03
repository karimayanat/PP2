import json
import csv
from connect import connect

def import_csv():
    conn = connect()
    cur = conn.cursor()
    with open("contacts.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["name"]
            email = row["email"]
            birthday = row["birthday"]
            group_name = row["group"]
            phone = row["phone"]
            phone_type = row["phone_type"]

            cur.execute(
                "INSERT INTO groups(name) VALUES(%s) ON CONFLICT (name) DO NOTHING",
                (group_name,)
            )
            cur.execute("SELECT id FROM groups WHERE name=%s", (group_name,))
            group_id = cur.fetchone()[0]

            cur.execute(
                "SELECT id FROM contacts WHERE name=%s AND email=%s",
                (name, email)
            )
            contact = cur.fetchone()

            if contact:
                contact_id = contact[0]
            else:
                cur.execute("""
                    INSERT INTO contacts(name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (name, email, birthday, group_id))
                contact_id = cur.fetchone()[0]

            cur.execute("""
                SELECT 1 FROM phones
                WHERE contact_id=%s AND phone=%s
            """, (contact_id, phone))

            if not cur.fetchone():
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (contact_id, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("CSV imported successfully")

def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("INSERT INTO groups(name) VALUES(%s) ON CONFLICT (name) DO NOTHING", (group,))
    cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
    group_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (name, email, birthday, group_id))

    contact_id = cur.fetchone()[0]

    while True:
        add_phone = input("Add phone? (y/n): ")
        if add_phone.lower() != "y":
            break

        phone = input("Phone: ")
        ptype = input("Type (home/work/mobile): ")

        cur.execute(
            "INSERT INTO phones(contact_id, phone, type) VALUES (%s, %s, %s)",
            (contact_id, phone, ptype)
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added")

def search_contacts():
    q = input("Search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    rows = cur.fetchall()

    for r in rows:
        print(r)

    cur.close()
    conn.close()

def filter_by_group():
    group = input("Group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group,))

    for r in cur.fetchall():
        print(r)

    cur.close()
    conn.close()

def sort_contacts():
    field = input("Sort by (name/birthday/created_at): ")

    if field not in ["name", "birthday", "created_at"]:
        print("Invalid field")
        return

    conn = connect()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT name, email, birthday
        FROM contacts
        ORDER BY {field}
    """)

    for r in cur.fetchall():
        print(r)

    cur.close()
    conn.close()

def paginate():
    limit = 3
    offset = 0

    while True:
        conn = connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT name, email
            FROM contacts
            ORDER BY id
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()

        if not rows:
            print("No more data")
        else:
            for r in rows:
                print(r)

        action = input("next / prev / quit: ")

        if action == "next":
            offset += limit
        elif action == "prev":
            offset = max(0, offset - limit)
        else:
            break

        cur.close()
        conn.close()

def move_group():
    name = input("Contact name: ")
    group = input("New group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s, %s)", (name, group))

    conn.commit()
    cur.close()
    conn.close()

def add_phone():
    name = input("Contact name: ")
    phone = input("Phone: ")
    ptype = input("Type: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))

    conn.commit()
    cur.close()
    conn.close()

def export_json():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
    """)

    data = cur.fetchall()

    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, default=str)

    cur.close()
    conn.close()

    print("Exported to contacts.json")

def import_json():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for name, email, birthday, group in data:

        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} exists (skip/overwrite): ")
            if choice == "skip":
                continue
            cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

        cur.execute("INSERT INTO contacts(name,email,birthday) VALUES(%s,%s,%s)",
                    (name, email, birthday))

    conn.commit()
    cur.close()
    conn.close()

    print("Imported JSON")

def delete_contact():
    value = input("Name or phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))

    conn.commit()
    cur.close()
    conn.close()

def menu():
    while True:
        print("\n1. Import CSV")
        print("2. Add contact")
        print("3. Search")
        print("4. Filter by group")
        print("5. Sort contacts")
        print("6. Pagination")
        print("7. Move to group")
        print("8. Add phone")
        print("9. Export JSON")
        print("10. Import JSON")
        print("11. Delete contact")
        print("0. Exit")
        choice = input("Choose: ")
        if choice == "1":
            import_csv()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            search_contacts()
        elif choice == "4":
            filter_by_group()
        elif choice == "5":
            sort_contacts()
        elif choice == "6":
            paginate()
        elif choice == "7":
            move_group()
        elif choice == "8":
            add_phone()
        elif choice == "9":
            export_json()
        elif choice == "10":
            import_json()
        elif choice == "11":
            delete_contact()
        elif choice == "0":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()