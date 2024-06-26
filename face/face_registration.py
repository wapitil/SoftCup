import base64
import urllib
import requests
import json
import os
import configparser
# 获取当前脚本所在的绝对路径
current_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_path, '..','config', 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)
API_KEY = config['FACE_SEARCH']['API_KEY']
SECRET_KEY = config['FACE_SEARCH']['SECRET_KEY']

def main(user_id,image):
        
    url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add?access_token=" + get_access_token()
    
    # image 可以通过 get_file_content_as_base64("C:\fakepath\1.jpg",False) 方法获取
    payload = json.dumps({
        "group_id": "Facerepo",
        "image_type": "BASE64",
        "user_id": user_id,
        "image":image
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    

def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    user_id="123"
    base64=get_file_content_as_base64('./imgs/1.png') # 使用该命令时注意切换路径至./face
    main(user_id,base64)
