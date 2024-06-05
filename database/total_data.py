import psycopg2
from psycopg2 import sql
import bcrypt
import configparser
import os


# 获取当前脚本所在的绝对路径
current_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_path, '..','config', 'config.ini')
print(config_path)
config = configparser.ConfigParser()
config.read(config_path)
db_name = config['DATABASE']['db_name']
user = config['DATABASE']['user']
password = config['DATABASE']['password']
host = config['DATABASE']['host']
port = config['DATABASE']['port']

class Mydata:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create students table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id SERIAL PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'student' NOT NULL,
            face_login_enabled BOOLEAN NOT NULL
        )
        ''')

        # Create questions table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            question_id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            question_type TEXT,
            score NUMERIC NOT NULL,  -- 分值键
            reference_answer TEXT NOT NULL  -- 参考答案
        )
        ''')

        # Create wrong_answers table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS wrong_answers (
            record_id SERIAL PRIMARY KEY,
            student_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            attempt_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            answer TEXT NOT NULL,
            is_correct BOOLEAN NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (question_id) REFERENCES questions(question_id)
        )
        ''')

        self.conn.commit()


    def close(self):
        self.cursor.close()
        self.conn.close()

    def add_user(self, username, password, role, face_login_enabled):
        self.cursor.execute(
            'INSERT INTO database (username, password, role, face_login_enabled) VALUES (%s, %s, %s, %s)', 
            (username, password, role, face_login_enabled)
        )
        self.conn.commit()
        print(f"User '{username}' added successfully.")

    def get_user(self, username):
        self.cursor.execute('SELECT * FROM database WHERE username = %s', (username,))
        user = self.cursor.fetchone()
        if user:
            print(f"User found: {user}")
        else:
            print(f"No user found with username '{username}'")
            return None
        return user

    def get_all_users(self):
        self.cursor.execute('SELECT * FROM students')
        users = self.cursor.fetchall()
        if users:
            print("All users:")
            for user in users:
                print(user)
        else:
            print("No users found.")
        return users

    def delete_user(self, username):
        self.cursor.execute('DELETE FROM database WHERE username = %s', (username,))
        self.conn.commit()
        print(f"User '{username}' deleted successfully.")

    def update_user_password(self, username, new_password):
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        self.cursor.execute('UPDATE database SET password = %s WHERE username = %s', (hashed_password, username))
        self.conn.commit()
        print(f"Password for user '{username}' updated successfully.")

    def add_exercise(self, type, subject, exercise_point, stem, answer, explain):
        self.cursor.execute(
            'INSERT INTO exercise_center (type, subject, exercise_point, stem, answer, explain) VALUES (%s, %s, %s, %s, %s, %s)',
            (type, subject, exercise_point, stem, answer, explain)
        )
        self.conn.commit()
        print(f"Exercise '{stem}' added successfully.")

    def get_exercise(self, exercise_id):
        self.cursor.execute('SELECT * FROM exercise_center WHERE exercise_id = %s', (exercise_id,))
        exercise = self.cursor.fetchone()
        if exercise:
            print(f"Exercise found: {exercise}")
        else:
            print(f"No exercise found with ID '{exercise_id}'")
            return None
        return exercise

    def get_all_exercises(self):
        self.cursor.execute('SELECT * FROM exercise_center')
        exercises = self.cursor.fetchall()
        if exercises:
            print("All exercises:")
            for exercise in exercises:
                print(exercise)
        else:
            print("No exercises found.")
        return exercises

    def update_exercise(self, exercise_id, type, subject, exercise_point, stem, answer, explain):
        self.cursor.execute('''
            UPDATE exercise_center
            SET type = %s, subject = %s, exercise_point = %s, stem = %s, answer = %s, explain = %s
            WHERE exercise_id = %s
        ''', (type, subject, exercise_point, stem, answer, explain, exercise_id))
        self.conn.commit()
        print(f"Exercise with ID '{exercise_id}' updated successfully.")

    def delete_exercise(self, exercise_id):
        self.cursor.execute('DELETE FROM exercise_center WHERE exercise_id = %s', (exercise_id,))
        self.conn.commit()
        print(f"Exercise with ID '{exercise_id}' deleted successfully.")

    def close(self):
        self.cursor.close()
        self.conn.close()

def menu():
    print("Select an option:")
    print("1. 添加用户")
    print("2. 查询用户")
    print("3. 查询全部用户")
    print("4. 更改密码")
    print("5. 删除用户")

db = Mydata()
if __name__ == "__main__":

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
            type = input("Enter type: ")
            subject = input("Enter subject: ")
            exercise_point = input("Enter exercise point: ")
            stem = input("Enter stem: ")
            answer = input("Enter answer: ")
            explain = input("Enter explain: ")
            db.add_exercise(type, subject, exercise_point, stem, answer, explain)
        
        elif choice == '7':
            exercise_id = input("Enter exercise ID: ")
            db.get_exercise(exercise_id)
        
        elif choice == '8':
            db.get_all_exercises()
        
        elif choice == '9':
            exercise_id = input("Enter exercise ID: ")
            type = input("Enter new type: ")
            subject = input("Enter new subject: ")
            exercise_point = input("Enter new exercise point: ")
            stem = input("Enter new stem: ")
            answer = input("Enter new answer: ")
            explain = input("Enter new explain: ")
            db.update_exercise(exercise_id, type, subject, exercise_point, stem, answer, explain)
        
        elif choice == '10':
            exercise_id = input("Enter exercise ID: ")
            db.delete_exercise(exercise_id)

        elif choice=='11':
            print("Exiting...")
            db.close()
        
        else:
            print("Invalid choice, please try again.")
