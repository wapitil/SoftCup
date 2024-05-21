from . import student
from flask import render_template, send_from_directory

@student.route('/')
def index():
    return render_template('index.html')

@student.route('/info_center')
def serve_exam_outline_pdf():
    # 假设PDF文件名为 '2024年考研计算机学科专业基础考试大纲.pdf'
    return send_from_directory('student/info_center', '2024年考研计算机学科专业基础考试大纲.pdf')
