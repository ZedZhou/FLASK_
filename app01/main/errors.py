from . import main
from flask import render_template
from ..Models import Permission
from flask import request,jsonify

# @main.app_errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'),404

# 使用http内容协商处理错误
@main.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        response = jsonify({'error':'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'),404



@main.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'),403