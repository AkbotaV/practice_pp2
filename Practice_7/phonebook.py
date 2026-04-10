import psycopg2
import csv
from connect import connect


def create_table():
  conn=connect()
  cur=conn.cursor()
  cur.execute("""
  CREATE TABLE IF NOT EXISTS phonebook(
  id SERIAL PRIMARY KEY,
  username VARCHAR(100) NOT NULL,
  phone VARCHAR(20) NOT NULL UNIQUE
  )
  """)
  conn.commit()
  cur.close()
  conn.close()

  print("Table crreated succesfully.")


def insert_from_csv():
  conn=connect()
  cur=conn.cursor()

  with open("contacts.csv","r",encoding='utf-8') as f:
    reader=csv.reader(f)
    next(reader)

    for row in reader:
      username=row[0]
      phone=row[1]
      cur.execute("INSERT INTO phonebook(username,phone) VALUES(%s,%s) ON CONFLICT (phone) DO NOTHING",(username,phone))
  conn.commit()
  cur.close()
  conn.close()
  print("Data inserted from CSV successfully!")


def insert_from_console():
  username=input("enter username: ")
  phone=input("enter phone: ")

  conn=connect()
  cur=conn.cursor()
  cur.execute("INSERT INTO phonebook(username,phone) VALUES(%s,%s) ON CONFLICT (phone) DO NOTHING",(username,phone))
  conn.commit()
  cur.close()
  conn.close()



def update_contact():
  current_user=input("Enter current username: ")
  new_user=input("Enter new username: ")
  new_phone=input("Enter new phone: ")

  conn=connect()
  cur=conn.cursor()
  cur.execute("UPDATE phonebook SET username=%s, phone=%s WHERE username=%s",(new_user,new_phone,current_user))
  conn.commit()
  cur.close()
  conn.close()

def query_contact():
  choice=input("Search by: 1.Name or 2.Phone? Type 1 or 2: ")
  conn=connect()
  cur=conn.cursor()

  if choice=="1":
    name=input("Enter name: ")
    cur.execute("SELECT * FROM phonebook WHERE username ILIKE %s",(f"%{name}%",))

  elif choice=="2":
    prefix=input("Enter phone prefix: ")
    cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s",(f"{prefix}%",))
  else:
    print("invalid choice")
    cur.close()
    conn.close()
    return  

  rows=cur.fetchall()
  if rows:
    for row in rows:
      print(row)
  else:
        print("No contacts found.")

  cur.close()
  conn.close()

def delete_contact():
  value=input("Enter name or phone: ")
  conn=connect()
  cur=conn.cursor()
  
  cur.execute("DELETE FROM phonebook WHERE username = %s OR phone = %s",(value,value))
  conn.commit()
  print("Contact deleted successfully!")
  cur.close()
  conn.close()

def view_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("Table is empty.")

    cur.close()
    conn.close()

def main():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1 - Create table")
        print("2 - Insert from csv")
        print("3 - Insert from console")
        print("4 - Update contact")
        print("5 - Search contact")
        print("6 - Delete contact")
        print("7 - View all contacts")
        print("0 - Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            insert_from_console()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            query_contact()
        elif choice == "6":
            delete_contact()
        elif choice == "7":
            view_table()
        elif choice == "0":
            print("Program finished.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()