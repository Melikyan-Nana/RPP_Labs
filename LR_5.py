import sqlite3
import pandas as pd

def create_function():
    conn = sqlite3.connect('users')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL,
                   name varchar (100),
                   email varchar (100),
                   PRIMARY KEY (id));""")
    conn.commit()
    conn.close()


def insert_function(id, name, email):
    conn = sqlite3.connect('users')
    cursor = conn.cursor()
    cursor.execute("""insert into users (id, name, email) VALUES  (:id, :name, :email) """, {"id":id, "name":name, "email":email})
    conn.commit()
    conn.close()


def select_function():
    conn = sqlite3.connect('users')
    cursor = conn.cursor()
    cursor.execute("""select * from users """)
    df = pd.DataFrame(cursor.fetchall(), columns= ['id', 'name', 'email'])
    print (df)
    conn.commit()
    conn.close()

def select1_function(id):
    conn = sqlite3.connect('users')
    cursor = conn.cursor()
    cursor.execute("""select * from users
                        where id=:id""", {"id":id})
    print(cursor.fetchone())
    conn.commit()
    conn.close()

def delete_function(id):
    conn = sqlite3.connect('users')
    cursor = conn.cursor()
    cursor.execute("""delete  from users
                        where id=:id""", {"id":id})
    conn.commit()
    conn.close()

def drop_function():
    conn = sqlite3.connect('users')
    cursor = conn.cursor()
    cursor.execute("""drop table users""")
    conn.commit()
    conn.close()

	def main():
    create_function()
    insert_function(1, 'Нахшун', 'Nana@mail.ru')
    insert_function(2, 'Кристина', 'Kris@mail.ru')
    insert_function(3, 'Нахшун', 'Nana@mail.ru')
    insert_function(4, 'Кристина', 'Kris@mail.ru')
    select_function()
    select1_function(3)
    delete_function(3)
    select_function()
    # drop_function()

main()
