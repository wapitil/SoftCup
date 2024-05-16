import base64
import urllib
import requests
import json

API_KEY = "k4EdPM6UR6nQjN2EZ4nPPD7o"
SECRET_KEY = "IeyysQiuL5zALqTjZxc6i9rILLP2S81c"

def main(filepath):
        
    url = "https://aip.baidubce.com/rest/2.0/face/v3/search?access_token=" + get_access_token()
    # print(get_file_content_as_base64(fr'{filepath}',False))
    payload = json.dumps({
        "group_id_list": "Facerepo",
        "image": get_file_content_as_base64(fr'{filepath}',False),
        "image_type": "BASE64",
        "quality_control": "NORMAL",
        "liveness_control": "NORMAL",
        "match_threshold": 80,
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    response_dict = json.loads(response.text)
    # print(response.text)
    if response_dict["error_code"]==0:
        # 人脸匹配成功
        user_id=response_dict["result"]["user_list"][0]["user_id"]
        return True,user_id
    else:
        # print(response_dict["error_msg"])
        return False,response_dict["error_msg"]

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
    img_path='face/imgs/4.jpg'
    main(img_path)
