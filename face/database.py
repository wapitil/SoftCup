import sqlite3
import bcrypt

class Database:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.check_same_thread=False #开启多线程操作
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT '学生' NOT NULL,
            face_login_enabled INTEGER NOT NULL  -- 添加人脸登录标志字段
        )
        ''')
        self.conn.commit()

    def add_user(self, username, password, role, face_login_enabled):
        self.cursor.execute('INSERT INTO users (username, password, role, face_login_enabled) VALUES (?, ?, ?, ?)', (username, password, role, face_login_enabled))
        self.conn.commit()

    def get_user(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone()

    def get_all_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def delete_user(self, username):
        self.cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        self.conn.commit()
    
    def update_user_password(self, username, new_password):
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        self.cursor.execute('UPDATE users SET password = ? WHERE username = ?', (hashed_password, username))
        self.conn.commit()

    def close(self):
        self.conn.close()
