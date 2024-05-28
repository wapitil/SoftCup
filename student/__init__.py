# student/__init__.py
from flask import Blueprint

student = Blueprint('student', __name__, template_folder='templates',static_folder='static')

# 导入routes模块以确保它能注册相应的视图函数
from . import routes
