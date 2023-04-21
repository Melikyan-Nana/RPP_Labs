import pandas as pd
import sqlite3


def create_table_users():
    conn = sqlite3.connect('users')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL,
                   name varchar(100),
                   email varchar(100),
                   PRIMARY KEY (id));""")
    conn.commit()
    conn.close()


def add_user(id, name, email):
    conn = sqlite3.connect('users')
    cursor = conn.cursor()
    cursor.execute("""insert into users (id, name, email) VALUES  (:id, :name, :email) """, {"id": id, "name": name, "email": email})
    conn.commit()
    conn.close()


def select_users():
    conn = sqlite3.connect('users')
    cursor = conn.cursor()
    cursor.execute("""select * from users """)
    df = pd.DataFrame(cursor.fetchall(), columns=['id', 'name', 'email'])
    print(df)
    conn.commit()
    conn.close()


def select_user_id(id):
    conn = sqlite3.connect('users')
    cursor = conn.cursor()
    cursor.execute("""select * from users
                        where id=:id""", {"id": id})
    print(cursor.fetchone())
    conn.commit()
    conn.close()


def delete_user_by_id(id):
    conn = sqlite3.connect('users')
    cursor = conn.cursor()
    cursor.execute("""delete  from users
                        where id=:id""", {"id": id})
    conn.commit()
    conn.close()


def drop_function():
    conn = sqlite3.connect('users')
    cursor = conn.cursor()
    cursor.execute("""drop table users""")
    conn.commit()
    conn.close()


def main():
    create_users()
    add_user(1, 'Нана', 'Nana@mail.ru')
    add_user(2, 'Кристина', 'Kris@mail.ru')
    add_user(3, 'Нана', 'Nana2002@mail.ru')
    add_user(4, 'Кристина', 'Kristina2002@mail.ru')
    select_users()
    select_user_by_id(4)
    delete_user_by_id(4)
    select_users()
    # drop_function()

main()
