from flask import Flask, request, jsonify, session
import bcrypt
import sys
# sys.path.append('../')
# from face.database import Database
from database import Database
import anti_spoof, face_registration,face_usersearch
app = Flask(__name__)
app.secret_key = "GBnfazrY8sWixwHg"

# 使用持久化的数据库文件
db = Database()


@app.route('/register', methods=['POST'])
def register():
    try:
        user_info = request.get_json()
        name = user_info.get('name')
        password = user_info.get('password')
        role = user_info.get('role','student')  # 默认为student
        face_login_enabled = user_info.get('face_login_enabled', 0)  # 默认为0
        face_image_base64 = user_info.get('face_image_base64')  # 假设前端发送base64编码的图像数据
        
        if not all([name, password,role]):
            return jsonify({"msg": "参数不完整"}), 400

        # 先检查用户是否存在
        if db.get_user(name):
            return jsonify({"msg": "用户已存在"}), 400
        
        # 哈希密码
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        if face_login_enabled == 1:
            if not face_image_base64:
                return jsonify({"msg": "人脸图像缺失"}), 400

            # 静默检测
            if not anti_spoof.run(face_image_base64):
                return jsonify({"msg": "静默检测失败"}), 400

            # 人脸搜索
            if face_usersearch.main(face_image_base64):
                return jsonify({"msg": "人脸已注册"}), 400
            
            # 人脸注册
            if not face_registration.main(role,face_image_base64,name):
                return jsonify({"msg": "人脸注册失败"}), 500

        db.add_user(name, hashed_password,role, face_login_enabled)
        
        session["name"] = name
        session["role"] = role
        return jsonify({"msg": "注册成功","name": name,"role":role }), 201
    except Exception as e:
        print(f"Error during registration: {e}")
        return jsonify({"msg": "error"}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        user_info = request.get_json()
        name = user_info.get('name')
        password = user_info.get('password')
        
        if not all([name, password]):
            return jsonify({"msg": "参数不完整"}), 400
        
        user = db.get_user(name)
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            session["name"] = name
            session["role"] = user[3]
            return jsonify({"msg": "登录成功"}), 200
        else:
            return jsonify({"msg": "用户名或密码错误"}), 401
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"msg": "error"}), 500

@app.route('/face_login', methods=['POST'])
def face_login():
    try:
        face_image_base64 = request.get_json().get('image_base64')  # 假设前端发送base64编码的图像数据
    
        if not face_image_base64:
            return jsonify({"msg": "人脸图像缺失"}), 400
        
        is_success,user=face_usersearch.main(face_image_base64)
        if is_success:
            user = db.get_user(user)
            session["name"] = user[1]
            session["role"] = user[3]
            return jsonify({"msg": "人脸登录成功"}), 200
    except Exception as e:
        print(f"Error during face login: {e}")
        return jsonify({"msg": "error"}), 500
        
@app.route("/session", methods=["GET"])
def check_session():
    name = session.get("name")
    role = session.get("role")
    if name is None:
        return jsonify({"msg": "未登录"}), 401
    else:
        return jsonify({"name": name, "role": role}), 200

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return jsonify({"msg": "退出成功"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
