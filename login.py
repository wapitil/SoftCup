import sqlite3
import bcrypt
from face import anti_spoof, face_registration, face_usersearch

# 数据库操作模块
class Database:
    def __init__(self, db_name='users.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def add_user(self, username, hashed_password):
        self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
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

# 用户注册和登录模块
class UserManager:
    def __init__(self, db):
        self.db = db

    def register_user(self, username, password):
        user = self.db.get_user(username)
        print(f"Checking if username '{username}' exists in the database: {user}")
        if user:
            return "Username already exists"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # print(f"Hashed password for '{username}': {hashed_password}")
        self.db.add_user(username, hashed_password)
        # print("User registered successfully. Current users in database:")
        # users = self.db.get_all_users()
        # for user in users:
        #     print(user)
        return "User registered successfully"

    def login_user(self, username, password):
        user = self.db.get_user(username)
        # print(f"Trying to login with username '{username}': {user}")
        if user is None:
            return "Username does not exist"
        stored_password = user[2]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return "Login successful"
        else:
            return "Invalid password"

# 人脸检测和注册模块
class FaceManager:
    def __init__(self, appid, apisecret, apikey):
        self.appid = appid
        self.apisecret = apisecret
        self.apikey = apikey

    def anti_spoof_check(self, img_path):
        return anti_spoof.run(
            appid=self.appid,
            apisecret=self.apisecret,
            apikey=self.apikey,
            img_path=img_path,
        )

    def register_face(self, user_id, img_path):
        # if flag is True, then face already exists
        flag,message=face_usersearch.main(img_path)
        if flag:
            return False, message
        face_registration.main(user_id, img_path)
        return True, 'Face registration successful'

    def login_face(self, img_path):
        flag, message = face_usersearch.main(img_path)
        if flag:
            return True, f'Face match successful. User ID: {message}'
        else:
            return False, f'Face match failed. Reason: {message}'

if __name__ == '__main__':
    # 初始化模块
    db = Database()
    user_manager = UserManager(db)
    face_manager = FaceManager(
        appid='764c37a5',
        apisecret='ZmY4MWI0NTJlNjE2ZjFhZmYzNDJjMGZm',
        apikey='76b4dede8794d3bb2ad38d63283b91e3'
    )

    img_path = 'face/imgs/2.jpg'
    choice = int(input("1:注册 2:密码登陆 3:人脸登陆 4:查看所有用户 5:删除用户\n请选择:"))

    if choice == 1:
        user_id = input("请输入学号:")
        password = input("请输入密码:")
        if face_manager.anti_spoof_check(img_path):
            success, message = face_manager.register_face(user_id, img_path)
            if success:
                register_message = user_manager.register_user(user_id, password)
                print(register_message)
            else:
                print(message)
    elif choice == 2:
        user_id = input("请输入学号:")
        password = input("请输入密码:")
        login_message = user_manager.login_user(user_id, password)
        print(login_message)
    elif choice == 3:
        if face_manager.anti_spoof_check(img_path):
            success, message = face_manager.login_face(img_path)
            print(message)
    elif choice == 4:
        print("Current users in database:")
        users = db.get_all_users()
        for user in users:
            print(user)
    elif choice == 5:
        username = input("请输入要删除的用户名:")
        db.delete_user(username)
        print(f"User '{username}' deleted successfully")

    # 关闭数据库连接
    db.close()
