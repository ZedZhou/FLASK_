import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = '15378301867@163.com'
    MAIL_PASSWORD = 'zdyxx1269'
    MAIL_DEBUG = True
    FLASK_ADMIN = '15378301867@163.com'
    FLASK_POSTS_PER_PAGE = 15


    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
    'sqlite:///' + os.path.join(BASE_DIR,'data.sql')


class TestingConfig(Config):
    pass

class ProductionConfig(Config):
    pass



config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig,
}