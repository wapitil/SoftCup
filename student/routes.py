# /student/routes.py
from . import student
from flask import send_from_directory

@student.route('/')
def index():
    return send_from_directory(student.static_folder, 'index.html')

@student.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(student.static_folder, path)
