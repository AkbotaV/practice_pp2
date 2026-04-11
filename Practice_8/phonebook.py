import psycopg2
from connect import connect

def search_contacts():
  pattern=input("Enter search pattern; ")
  conn=connect()
  cur=conn.cursor()
  cur.execute("SELECT * FROM get_contacts_by_pattern(%s)",(pattern,))
  rows=cur.fetchall()
  for row in rows:
    print(row)

  cur.close()
  conn.close()

def upsert_contacts():
  user=input("Enter user; ")
  phone=input("Enter phone; ")
  conn=connect()
  cur=conn.cursor()
  cur.execute("CALL insert_or_update(%s,%s)",(user,phone))
  conn.commit()
  cur.close()
  conn.close()

def del_contacts():
  user_or_phone=input("Enter user or phone: ")
  conn=connect()
  cur=conn.cursor()
  cur.execute("CALL delete_contact(%s)",(user_or_phone,))
  conn.commit()
  cur.close()
  conn.close()

def insert_many():
  print("Enter names and then phones: ")
  usernames=[]
  phones=[]
  while True:
    user=input()
    if user.lower() == "stop":
        break
    phone=input()
    usernames.append(user)
    phones.append(phone)
  conn=connect()
  cur=conn.cursor()
  cur.execute("CALL insert_many_users(%s,%s)",(usernames,phones))
  conn.commit()
  cur.close()
  conn.close()


def get_paginated():
  limit_v=int(input("Enter limit value: "))
  offset_v=int(input("Enter offset value: "))
  conn=connect()
  cur=conn.cursor()
  cur.execute("SELECT * FROM get_contacts_paginated(%s,%s)",(limit_v,offset_v))
  rows = cur.fetchall()

  for row in rows:
        print(row)

  cur.close()
  conn.close()


def main():
    while True:
        print("\n--- MENU ---")
        print("1 - Search contacts")
        print("2 - Insert or update")
        print("3 - Insert many")
        print("4 - Pagination")
        print("5 - Delete contact")
        print("0 - Exit")

        choice = input("Choose: ")

        if choice == "1":
            search_contacts()
        elif choice == "2":
            upsert_contacts()
        elif choice == "3":
            insert_many()
        elif choice == "4":
            get_paginated()
        elif choice == "5":
            del_contacts()
        elif choice == "0":
            break
        else:
            print("Invalid choice")



main()