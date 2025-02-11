import sqlite3
from sqlite3 import Error

def create_connection(db_file):
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       return conn
   except sqlite3.Error as e:
       print(e)
   return conn

def execute_sql(conn, sql):
   try:
       c = conn.cursor()
       c.execute(sql)
   except Error as e:
       print(e)

def add_person(conn, members):
   sql = '''INSERT INTO members(first_name, last_name, department, position)
             VALUES(?,?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, members)
   conn.commit()
   return cur.lastrowid

def update(conn, table, id, **kwargs):
   parameters = [f"{k} = ?" for k in kwargs]
   parameters = ", ".join(parameters)
   values = tuple(v for v in kwargs.values())
   values += (id, )

   sql = f''' UPDATE {table}
             SET {parameters}
             WHERE id = ?'''
   try:
       cur = conn.cursor()
       cur.execute(sql, values)
       conn.commit()
       print("OK")
   except sqlite3.OperationalError as e:
       print(e)


def delete_where(conn, table, **kwargs):
   qs = []
   values = tuple()
   for k, v in kwargs.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)

   sql = f'DELETE FROM {table} WHERE {q}'
   cur = conn.cursor()
   cur.execute(sql, values)
   conn.commit()
   print("Deleted")       


def select_where(conn, table, **query):

   cur = conn.cursor()
   qs = []
   values = ()
   for k, v in query.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)
   cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
   rows = cur.fetchall()
   return rows

if __name__ == "__main__":
   
 create_tasks_sql = """

   CREATE TABLE IF NOT EXISTS members(
      id integer PRIMARY KEY,
      first_name VARCHAR(250) NOT NULL,
      last_name VARCHAR(250) NOT NULL,
      department VARCHAR(150) NOT NULL,
      position VARCHAR(150) NOT NULL
   );
   """
 db_file = "database.db"

 conn = create_connection(db_file)
 if conn is not None:
       execute_sql(conn, create_tasks_sql)


members = (
    
       "Jan",
       "Niezbedny",
       "Rzeczy zaginione",
       "Poszukiwacz",
   )
add_person(conn, members)
members = (
    
       "Alicja",
       "Niezbedny",
       "Duzych Podrozy",
       "Specjalista ds. poszukiwania przygod",
   )
add_person(conn, members)
members = (
    
       "Karol",
       "Wielki",
       "Malych Podrozy",
       "Praktykant",
   )
add_person(conn, members)

conn.commit()

update(conn, "members", 2, Last_name = "Wielki")
select_where(conn, "members", Last_name = "Wielki")
print(select_where(conn, "members", Last_name = "Wielki"))
delete_where(conn, "members", id=1)
conn.close()
