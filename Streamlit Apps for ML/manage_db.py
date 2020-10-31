import sqlite3

conn = sqlite3.connect("usersdata.db")
c = conn.cursor()

def create_usertable():
    c.execute(sql="""
    CREATE TABLE IF NOT EXISTS users_table(username TEXT, password TEXT)
    """)

def add_user_data(username, password):
    c.execute("""
    INSERT INTO users_table(username, password) VALUES (?, ?)
    """, (username, password))
    conn.commit()

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