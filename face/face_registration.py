import base64
import urllib
import requests
import json

API_KEY = "k4EdPM6UR6nQjN2EZ4nPPD7o"
SECRET_KEY = "IeyysQiuL5zALqTjZxc6i9rILLP2S81c"

def main(user_id,filepath):
        
    url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add?access_token=" + get_access_token()
    
    # image 可以通过 get_file_content_as_base64("C:\fakepath\Ami.png",False) 方法获取
    payload = json.dumps({
        "group_id": "Facerepo",
        "image": get_file_content_as_base64(rf'{filepath}',False),
        "image_type": "BASE64",
        "user_id": f"{user_id}"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    response_dict = json.loads(response.text)
    # print(response.text)
    if response_dict["error_code"]==0:
        # print('人脸注册成功')
        return True
    else:
        print(response_dict["error_msg"])
        return False
    

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

    user_id="123123"
    filepath="face/imgs/1.jpg"
    main(user_id,filepath)