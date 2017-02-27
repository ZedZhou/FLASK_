from flask import render_template,redirect,request,url_for,flash
from . import auth
from .forms import *
from ..Models import User
from flask_login import login_user
from .. import db
from flask_login import current_user
from ..Models import Permission

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(url_for('main.hello_world'))
        flash('无效的信息！')
    return render_template('auth/login.html',form=form,Permission=Permission)

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password = form.password.data,
                    name = form.name.data,
                    location = form.location.data
                    )
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()

        flash('注册成功，您可以登录了！')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form,Permission=Permission)

from flask_login import logout_user,login_required
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('注销成功！')
    return redirect(url_for('main.hello_world'))

@auth.route('/unconfirmed')
def unconfirmed():
    return '未认证'

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        # if not current_user.confirmed and request.endpoint[:5] != 'auth.':
        #     return redirect(url_for('auth.unconfirmed'))

