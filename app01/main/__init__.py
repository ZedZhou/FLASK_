from flask import Blueprint

main = Blueprint('main',__name__)


# 导入这两个模块就能把路由和错误处理程序与蓝本关联起来,注意 必须在末尾导入 避免循环
from . import views,errors