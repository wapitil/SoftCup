from flask import Flask, request, jsonify, session,render_template
import bcrypt
import sys
from face.database import Database
from face import anti_spoof, face_registration,face_usersearch
from SmartAssistant.Spark import main
# import SmartAssistant.SparkApi as SparkApi‘
from student import student

app = Flask(__name__)

app.secret_key = "GBnfazrY8sWixwHg"
app.register_blueprint(student, url_prefix='/student')

# 使用持久化的数据库文件
db = Database()

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        user_info = request.get_json()
        name = user_info.get('name')
        password = user_info.get('password')
        role = user_info.get('role', 'student')  # 默认为student
        face_login_enabled = str_to_bool(user_info.get('face_login_enabled', False))
        face_image = user_info.get('face_image')  # 人脸图像
        print(user_info)
        
        if not all([name, password, role]):  
            return jsonify({"error_code": 10000, "msg": "参数不完整","data":{}}), 400

        if db.get_user(name):
            return jsonify({"error_code": 10001,"msg": "用户已存在","data":{}}), 403
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        if face_login_enabled:
            if not face_image:
                return jsonify({"error_code": 10002,"msg": "人脸图像缺失","data":{}}), 400

            if not anti_spoof.run(face_image):
                return jsonify({"error_code": 10003,"msg": "静默检测失败","data":{}}), 400

            if face_usersearch.main(face_image):  
                return jsonify({"error_code": 10004,"msg": "人脸已注册","data":{}}), 403
            
            if not face_registration.main(name,face_image):
                return jsonify({"error_code": 10005,"msg": "人脸注册失败","data":{}}), 500
            # face_registration.main(name,face_image)

        db.add_user(name, hashed_password, role, face_login_enabled)
        
        jsonify({"msg": "test"})
        session["name"] = name
        session["role"] = role
        return jsonify({"error_code": 0,"msg": "success","data":{ "name": name, "role": role}}), 200
    except Exception as e:
        print(f"Error during registration: {e}")
        return jsonify({"error_code": 10006,"msg": "error", "data":{"error_detail":str(e)}}), 500

def str_to_bool(value):
    if isinstance(value, bool):
        return value
    return str(value).lower() in ('true', '1', 'yes', 'y', 't')

@app.route('/login', methods=['POST'])
def login():
    try:
        user_info = request.get_json()
        name = user_info.get('name')
        password = user_info.get('password')
        # face_login_enabled = user_info.get('face_login_enabled', False)  # 默认为0
        
        if not all([name, password]):
            return jsonify({"error_code": 10000,"msg": "参数不完整","data":{}}), 200
        
        user = db.get_user(name)
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            session["name"] = name
            session["role"] = user[3]
            return jsonify({"error_code": 0,"msg": "success","data":{}}), 200
        else:
            return jsonify({"error_code": 10007,"msg": "用户名或密码错误","data":{}}), 200
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"error_code": 10006,"msg": "error", "data":{"error_detail":str(e)}}), 500

@app.route('/face_login', methods=['POST'])
def face_login():
    try:
        user_info = request.get_json()
        face_image = user_info.get('face_image')  
        if face_image is None:
            return jsonify({"error_code": 10002,"msg": "人脸图像缺失","data":{}}), 200
        
        is_success,user=face_usersearch.main(face_image)
        if is_success:
            print(user)
            user = db.get_user(user)
            session["name"] = user[1]
            session["role"] = user[3]
            session["face_login_enabled"] = "True"
            return jsonify({"error_code":0,"msg": "success","data":{}}), 200
    except Exception as e:
        print(f"Error during face login: {e}")
        return jsonify({"error_code": 10006,"msg": "error", "data":{"error_detail":str(e)}}), 500
    
@app.route("/session", methods=["GET"])
def check_session():
    name = session.get("name")
    # role = session.get("role")
    if name is None:
        return jsonify({"error_code":10008,"msg": "未登录","data":{}})
    else:
        return jsonify({"error_code":0,"msg": "success","data":{"name":name}}), 200
    
@app.route("/update_password",methods=['POST'])
def update_password():
    user_info = request.get_json()
    username=user_info.get('name')
    new_password=user_info.get('new_password')
    check_password=user_info.get('check_password')
    if db.get_user(username) is None:
        return jsonify({"error_code":10010,"msg": "用户不存在","data":{}})
    if check_password !=new_password:
        return jsonify({"error_code":10009,"msg": "两次输入的密码不匹配","data":{}}), 200
    else:
        db.update_user_password(username, new_password)
        return jsonify({"error_code": 0,"msg": "success","data":{}}), 200


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return jsonify({"error_code": 0,"msg": "success","data":{}}), 200

@app.route("/spark_ai", methods=["POST"])
def spark_ai():
    try:
        user_input = request.get_json().get("user_input")
        if user_input is None:
            return jsonify({"error_code":"10000","msg": "参数不完整"}), 400
        ai_answer= main(user_input)
        return jsonify({"error_code":0,"msg": "success","data":{"answer":ai_answer}}), 200
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"msg": "error"}), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001,debug=True)
