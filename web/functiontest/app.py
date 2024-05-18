from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import sqlite3
import bcrypt
import sys
sys.path.append('../..')
from face import anti_spoof, face_registration, face_usersearch

app = Flask(__name__)
CORS(app)

# 数据库操作模块
class Database:
    def __init__(self, db_name='users.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
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
        if user:
            return "Username already exists"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.db.add_user(username, hashed_password)
        return "User registered successfully"

    def login_user(self, username, password):
        user = self.db.get_user(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            return "Login successful"
        else:
            return "Invalid username or password"

db = Database()
user_manager = UserManager(db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    message = user_manager.register_user(username, password)
    return jsonify({'message': message})

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    message = user_manager.login_user(username, password)
    return jsonify({'message': message})

@app.route('/face-register', methods=['POST'])
def face_register():
    username = request.form['username']
    img_path = 'path_to_captured_face_image'  # 替换为实际捕获的图像路径
    if anti_spoof.main(img_path):
        flag, message = face_usersearch.main(img_path)
        if flag:
            return jsonify({'message': 'Face already registered'})
        face_registration.main(username, img_path)
        return jsonify({'message': 'Face registered successfully'})
    else:
        return jsonify({'message': 'Anti-spoofing check failed'})

@app.route('/face-login', methods=['POST'])
def face_login():
    img_path = 'path_to_captured_face_image'  # 替换为实际捕获的图像路径
    if anti_spoof.main(img_path):
        flag, message = face_usersearch.main(img_path)
        if flag:
            return jsonify({'message': f'Face match successful. User ID: {message}'})
        else:
            return jsonify({'message': 'Face match failed'})
    else:
        return jsonify({'message': 'Anti-spoofing check failed'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
