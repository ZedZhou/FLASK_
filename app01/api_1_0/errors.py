from flask import jsonify
from app01.exceptions import ValidationError
from . import api

# Web 服务的视图函数可以调用这些辅助函数生成错误响应
def bad_request(message):
    response = jsonify({'error':'unauthorized','message':message})
    response.status_code = 400
    return response

def unauthorized(message):
    response = jsonify({'error':'unauthorized','message':message})
    response.status_code = 401
    return response

def forbidden(message):
    response = jsonify({'error':'forbidden','message':message})
    response.status_code = 403
    return response

@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])

