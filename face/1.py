import psycopg2
import bcrypt
import configparser
import os

# 获取当前脚本所在的绝对路径
current_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_path, 'config', 'config.ini')

# Debugging statement to check the config path
print(f"Config path: {config_path}")

config = configparser.ConfigParser()
config.read(config_path)

# Debugging statement to check if config file is read
if config.sections():
    print("Config file read successfully.")
else:
    print("Failed to read config file.")

db_name = config['DATABASE']['db_name']
user = config['DATABASE']['user']
password = config['DATABASE']['password']
host = config['DATABASE']['host']
port = config['DATABASE']['port']

# Debugging statements to check the values read from the config file
print(f"Database Name: {db_name}")
print(f"User: {user}")
print(f"Password: {password}")
print(f"Host: {host}")
print(f"Port: {port}")

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'student' NOT NULL,
            face_login_enabled BOOLEAN NOT NULL
        )
        ''')
        self.conn.commit()

    def add_user(self, username, password, role, face_login_enabled):
        self.cursor.execute(
            'INSERT INTO users (username, password, role, face_login_enabled) VALUES (%s, %s, %s, %s)', 
            (username, password, role, face_login_enabled)
        )
        self.conn.commit()
        print(f"User '{username}' added successfully.")

    def get_user(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = self.cursor.fetchone()
        if user:
            print(f"User found: {user}")
        else:
            print(f"No user found with username '{username}'")
        return user

    def get_all_users(self):
        self.cursor.execute('SELECT * FROM users')
        users = self.cursor.fetchall()
        if users:
            print("All users:")
            for user in users:
                print(user)
        else:
            print("No users found.")
        return users

    def delete_user(self, username):
        self.cursor.execute('DELETE FROM users WHERE username = %s', (username,))
        self.conn.commit()
        print(f"User '{username}' deleted successfully.")

    def update_user_password(self, username, new_password):
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        self.cursor.execute('UPDATE users SET password = %s WHERE username = %s', (hashed_password, username))
        self.conn.commit()
        print(f"Password for user '{username}' updated successfully.")

    def close(self):
        self.cursor.close()
        self.conn.close()

def menu():
    print("Select an option:")
    print("1. Add User")
    print("2. Get User")
    print("3. Get All Users")
    print("4. Update User Password")
    print("5. Delete User")
    print("6. Exit")

if __name__ == "__main__":
    db = Database()

    while True:
        menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role: ")
            face_login_enabled = input("Enable face login (True/False): ")
            face_login_enabled = face_login_enabled.lower() == 'true'
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            db.add_user(username, hashed_password, role, face_login_enabled)
        
        elif choice == '2':
            username = input("Enter username: ")
            db.get_user(username)
        
        elif choice == '3':
            db.get_all_users()
        
        elif choice == '4':
            username = input("Enter username: ")
            new_password = input("Enter new password: ")
            db.update_user_password(username, new_password)
        
        elif choice == '5':
            username = input("Enter username: ")
            db.delete_user(username)
        
        elif choice == '6':
            print("Exiting...")
            db.close()
            break
        
        else:
            print("Invalid choice, please try again.")
