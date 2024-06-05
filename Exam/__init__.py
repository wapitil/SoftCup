# ExamCenter/__init__.py
from flask import Blueprint
exam = Blueprint('exam', __name__)

# 导入routes模块以确保它能注册相应的视图函数
from . import routes
