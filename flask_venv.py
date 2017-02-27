import os
from datetime import datetime

from flask import Flask
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request,url_for,session,flash
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate,MigrateCommand
from flask_moment import Moment
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

manager = Manager(app)
bootstap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = \
'sqlite:///' + os.path.join(BASE_DIR,'data.sql')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

# @app.route('/',methods=['GET','POST'])
# def hello_world():
#     from app01.main.forms import NameForm
#     form = NameForm()
#     if form.validate_on_submit():
#         old_name = session.get('name')
#         if old_name is not None and old_name != form.name.data:
#             flash('看来你改变了你的名字!!!')
#         session['name'] = form.name.data
#         return redirect(url_for('hello_world'))
#
#     return render_template('user.html',
#                            form=form,name=session.get('name'),
#                            current_time=datetime.utcnow())

# @app.route('/user/<name>')
# def show_name(name):
#     user_agent = request.headers.get('User-Agent')
#     return 'helle %s,your browser is %s' % (name,user_agent)
#
# @app.route('/response')
# def show_response():
#     response = make_response('携带cookie!~~~')
#     response.set_cookie('answer','44')
#     return response
#
# @app.route('/temp')
# def temp():
#     l =[1,2,3]
#     return render_template('模板1.html',name='周冬雨',hello='<h2>你好啊</h2>',l=l)
#
# @app.route('/boot')
# def index():
#     name='周冬雨'
#     return render_template('bootstrap_demo.html',name=name)
#
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
    # manager.run()