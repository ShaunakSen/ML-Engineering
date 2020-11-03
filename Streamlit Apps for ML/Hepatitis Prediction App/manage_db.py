import os
import psutil 
import sqlite3

### code to handle already open DB connections: credits: https://stackoverflow.com/questions/35368117/how-do-i-check-if-a-sqlite3-database-is-connected-in-python
def is_open(path):
    for proc in psutil.process_iter():
        try:
            files = proc.open_files()
            if files:
                for _file in files:
                    if _file.path == path:
                        return True    
        except psutil.NoSuchProcess as err:
            print(err)
    return False


# path = os.path.abspath('usersdata.db')


def create_usertable():
    conn = sqlite3.connect('usersdata.db')
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users_table(username TEXT, password TEXT)
    """)
    conn.close()

def add_user_data(username, password):
    conn = sqlite3.connect('usersdata.db')
    c = conn.cursor()
    c.execute("""
    INSERT INTO users_table(username, password) VALUES (?, ?)
    """, (username, password))
    conn.commit()
    conn.close()

def login_user(username, password):
    c.execute("""
    SELECT * FROM users_table WHERE username = ? AND password = ?
    """, (username, password))

    data = c.fetchall()
    return data ## returns a list

def view_all_users():
    c.execute("""
    SELECT * FROM users_table
    """)
    data = c.fetchall()
    return data
