from flask_wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..Models import User

class LoginForm(Form):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    password = PasswordField('Password',validators=[Required(),])
    remember_me = BooleanField('保持登录')
    submit = SubmitField('Log In')

# 注册新用户
class RegisterForm(Form):
    email = StringField('邮箱',validators=[Required(),Length(1,64),Email()])
    username = StringField('用户名',validators=[Required(),Length(1,64),])
    name = StringField('游戏名',validators=[Required(),Length(1,32)])
    location = StringField('地址',validators=[Required(),Length(1,64)])
    password = PasswordField('密码',validators=[Required(),])
    password2 =PasswordField('确认密码',validators=[EqualTo('password',message='密码不一致！请重新输入。')])
    submit = SubmitField('注册')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册！')
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在！')