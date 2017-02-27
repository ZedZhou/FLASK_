from flask_httpauth import HTTPBasicAuth
from ..Models import AnonymousUser
from ..Models import *
from . import api
from .errors import unauthorized,forbidden
from flask import jsonify,g


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token,password):
    # 匿名用户
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    # 使用token
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    # 账号密码验证
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('认证失败')

@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden('没有认证的用户')

# 认证令牌发送给客户端为了避免客户端使用旧令牌申请新令牌，
# 要在视图函数中检查 g.token_used 变量的值，
# 如果使用令牌进行认证就拒绝请求.
@api.route('/token')
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token':g.current_user.generate_auth_token(expiration=3600),
                    'expiration':3600})



