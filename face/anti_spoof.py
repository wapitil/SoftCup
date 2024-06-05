from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import json
import requests
import urllib
import os
import configparser


# 获取当前脚本所在的绝对路径
current_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_path, '..','config', 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

appid = config['XUNFEI']['appid']
apisecret = config['XUNFEI']['apisecret']
apikey = config['XUNFEI']['apikey']

class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg

class Url:
    def __init__(self, host, path, schema):
        self.host = host
        self.path = path
        self.schema = schema

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

def parse_url(requset_url):
    stidx = requset_url.index("://")
    host = requset_url[stidx + 3:]
    schema = requset_url[:stidx + 3]
    edidx = host.index("/")
    if edidx <= 0:
        raise AssembleHeaderException("invalid request url:" + requset_url)
    path = host[edidx:]
    host = host[:edidx]
    u = Url(host, path, schema)
    return u

def assemble_ws_auth_url(requset_url, method="GET", api_key="", api_secret=""):
    u = parse_url(requset_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'), digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (api_key, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    values = {"host": host, "date": date, "authorization": authorization}
    return requset_url + "?" + urlencode(values)

def gen_body(appid, image, server_id):
    body = {
        "header": {"app_id": appid, "status": 3},
        "parameter": {
            server_id: {
                "service_kind": "XUNFEI",
                "XUNFEI_result": {"encoding": "utf8", "compress": "raw", "format": "json"}
            }
        },
        "payload": {
            "input1": {"encoding": "jpg", "status": 3, "image": image}
        }
    }
    return json.dumps(body)

def run(image, server_id='s67c9c78c'):
    url = 'https://api.xf-yun.com/v1/private/{}'.format(server_id)
    request_url = assemble_ws_auth_url(url, "POST", apikey, apisecret)
    headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'app_id': appid}

    try:
        response = requests.post(request_url, data=gen_body(appid, image, server_id), headers=headers)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")

        if response.status_code != 200:
            print(f"Error: Received non-200 status code: {response.status_code}")
            return False

        resp_data = response.json()
        text_decode = base64.b64decode(resp_data['payload']['XUNFEI_result']['text']).decode()
        result_json = json.loads(text_decode)

        if result_json['passed']:
            print('活体检测通过')
            return True
        else:
            print('活体检测不通过')
            print(result_json['score'])
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Response content: {response.content}")

def main(image_base64):
    run(image_base64)

if __name__ == '__main__':
    # 第一种方法：通过图像路径进行检测
    img_path = './imgs/1.png'
    base64_image = get_file_content_as_base64(img_path)
    with open('1.txt','w',encoding='utf-8') as f:
        f.write(base64_image)
    main(base64_image)

    # 第二种方法：直接使用base64编码的图像数据进行检测
    # base64_image = "your_base64_encoded_image_data"
    # main(base64_image)
