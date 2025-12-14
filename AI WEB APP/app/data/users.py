from app.data.db import connect_database


def get_user_by_username(username):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    return user


def insert_user(id,username, password_hash, role='user'):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (id, username, password_hash, role) VALUES (?, ?, ?, ?)",
        (id, username, password_hash, role)
    )
    conn.commit()
    conn.close()


def get_all_users():
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


def delete_user(username):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()



class User:
	def __init__(self, user_id, username, password_hash, role):
		self.user_id = user_id
		self.username = username
		self.password_hash = password_hash
		self.role = role

	def __str__(self):
		return f"User: {self.username} (Role: {self.role})"