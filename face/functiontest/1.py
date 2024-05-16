import cv2
import base64
import numpy as np
from urllib.parse import quote_plus  # 注意修改导入

def encode_image_to_base64(image, urlencoded=False):
    _, buffer = cv2.imencode('.jpg', image)
    content = base64.b64encode(buffer).decode("utf8")
    if urlencoded:
        content = quote_plus(content)
    print(content)  # 将打印语句放在条件块外部
    return content

encode_image_to_base64