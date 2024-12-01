import sqlite3

from model.user import User


def create_user(name, email, password):
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    query = f"INSERT INTO user (name, email, password) VALUES ('{name}', '{email}', '{password}')"  
    print(query)
    c.execute(query)
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    query = f"SELECT id,name,password FROM user  WHERE email = '{email}'"
    c.execute(query)
    result = c.fetchone()
    conn.close()
    return result

def get_user_by_email_and_password(email,password):
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    query = f"SELECT id,name,password FROM user  WHERE email = '{email}'and password = '{password}'"
    c.execute(query)
    result = c.fetchone()
    conn.close()
    return result

def get_user_by_id(id):
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    query = f"SELECT id,name,password,nationality,age,gender,avatar FROM user  WHERE id = '{id}'"
    c.execute(query)
    result = c.fetchone()
    conn.close()
    return result

def update_user(id, user: User):
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    query = f"UPDATE user SET name = '{user.name}', email = '{user.email}', password = '{user.password}', nationality = '{user.nationality}', age = '{user.age}', gender = '{user.gender}', avatar = '{user.avatar}' WHERE id = '{id}'"
    c.execute(query)
    conn.commit()
    conn.close()


