import cv2
import base64
import requests

def capture_and_send_image():
    cap = cv2.VideoCapture(0)  # 开启摄像头
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    ret, frame = cap.read()
    cap.release()  # 释放摄像头
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return

    encoded_image = encode_image_to_base64(frame)
    send_image_to_server(encoded_image)

def encode_image_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    return jpg_as_text

def send_image_to_server(image_data):
    url = 'http://localhost:5000/login'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json={'image': image_data}, headers=headers)
    print(response.json())

capture_and_send_image()
