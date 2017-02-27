from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from config import config
from flask_login import LoginManager
from flask_mail import Mail
from flask_pagedown import PageDown


bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
# LoginManager 对象的 session_protection 属性可以设为 None、'basic' 或 'strong'
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
mail = Mail()
pagedown = PageDown()

def create_app(configname):
    app = Flask(__name__)
    # 选择配置
    app.config.from_object(config[configname])
    # 调用静态方法
    config[configname].init_app(app)

    # 注册实例
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    pagedown.init_app(app)

    # 附加路由和错误页面
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')
    from .api_1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint,url_prefix='/api/v1.0')

    return app