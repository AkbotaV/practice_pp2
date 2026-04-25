import psycopg2
from config import load_config

def connect():
  try:
    config=load_config()
    conn=psycopg2.connect(**config)
    print("Conneected to the PostgreSQL server.")
    return conn
  except (psycopg2.DatabaseError, Exception) as error:
    print(f"Error:{error}")
    return None

if __name__ == '__main__':
    connection = connect()
    if connection is not None:
        connection.close()
        print('Connection closed.')