import json
import csv
from connect import connect


def get_group_id(cur, group_name):
    cur.execute("""
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """, (group_name,))

    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]



def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    conn = connect()
    cur = conn.cursor()

    group_id = get_group_id(cur, group)

    cur.execute("""
        INSERT INTO contacts(username, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (name, email, birthday, group_id))

    contact_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO phones(contact_id, phone, type)
        VALUES (%s, %s, %s)
    """, (contact_id, phone, ptype))

    conn.commit()
    cur.close()
    conn.close()

    print("Added.")



def view_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.username, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
    """)

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()



def search_by_email():
    email = input("Email part: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT username, email
        FROM contacts
        WHERE email ILIKE %s
    """, (f"%{email}%",))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def filter_by_group():
    group = input("Group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.username, c.email, g.name
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name ILIKE %s
    """, (group,))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def sort_contacts():
    field = input("Sort by (username/birthday/created_at): ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT username, email, birthday, created_at
        FROM contacts
        ORDER BY {field}
    """)

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()



def pagination():
    limit = 5
    offset = 0

    while True:
        conn = connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT username, email, birthday
            FROM contacts
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()

        for r in rows:
            print(r)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        else:
            break

        cur.close()
        conn.close()


def add_phone():
    name = input("Username: ")
    phone = input("Phone: ")
    ptype = input("Type: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s,%s,%s)", (name, phone, ptype))

    conn.commit()
    cur.close()
    conn.close()




def move_group():
    name = input("Username: ")
    group = input("New group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s,%s)", (name, group))

    conn.commit()
    cur.close()
    conn.close()



def search_all():
    q = input("Search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (q,))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


# export json

def export_json():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.username, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
    """)
    
    contact_rows = cur.fetchall()

    data = []

    for row in contact_rows:

        cur.execute("""
          SELECT phone, type
          FROM phones
          WHERE contact_id = %s
          """, (row[0],))
          
        phones=cur.fetchall()


        data.append({
            "username": row[1],
            "email": row[2],
            "birthday": str(row[3]),
            "group": row[4],
            "phones": [{"phone": p[0], "type": p[1]} for p in phones]
        })

    with open("contacts.json", "w") as f:
        json.dump(data, f, indent=4)

    cur.close()
    conn.close()


# import  json

def import_json():
    with open("contacts.json") as f:
        data = json.load(f)

    conn = connect()
    cur = conn.cursor()

    for c in data:
        name = c["username"]

        cur.execute("SELECT * FROM contacts WHERE username=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} exists. skip/overwrite: ")
            if choice == "skip":
                continue
            elif choice == "overwrite":
                cur.execute("DELETE FROM contacts WHERE username=%s", (name,))

        group_id = get_group_id(cur, c["group"])

        cur.execute("""
            INSERT INTO contacts(username, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (c["username"], c["email"], c["birthday"], group_id))

        contact_id = cur.fetchone()[0]

        for p in c["phones"]:
          cur.execute("""
              INSERT INTO phones(contact_id, phone, type)
              VALUES (%s, %s, %s)
              ON CONFLICT (contact_id, phone) DO NOTHING
          """, (contact_id, p["phone"], p["type"]))



    conn.commit()
    cur.close()
    conn.close()


# import csv

def import_csv():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.csv") as f:
        reader = csv.DictReader(f)

        for row in reader:
            group_id = get_group_id(cur, row["group"])

            cur.execute("""
                INSERT INTO contacts(username, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                RETURNING id
            """, (row["username"], row["email"], row["birthday"], group_id))

            result = cur.fetchone()
            if result is None:
                cur.execute("SELECT id FROM contacts WHERE username = %s", (row["username"],))
                contact_id = cur.fetchone()[0]
            else:
                contact_id = result[0]
 
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
                ON CONFLICT (contact_id, phone) DO NOTHING
            """, (contact_id, row["phone"], row.get("type", "mobile")))

    conn.commit()
    cur.close()
    conn.close()


# menu

def main():
    while True:
        print("""
1 Add contact
2 View contacts
3 Search email
4 Filter group
5 Sort
6 Pagination
7 Add phone
8 Move group
9 Search all
10 Export JSON
11 Import JSON
12 Import CSV
0 Exit
""")

        c = input("Choice: ")

        if c == "1": add_contact()
        elif c == "2": view_contacts()
        elif c == "3": search_by_email()
        elif c == "4": filter_by_group()
        elif c == "5": sort_contacts()
        elif c == "6": pagination()
        elif c == "7": add_phone()
        elif c == "8": move_group()
        elif c == "9": search_all()
        elif c == "10": export_json()
        elif c == "11": import_json()
        elif c == "12": import_csv()
        elif c == "0": break


if __name__ == "__main__":
    main()