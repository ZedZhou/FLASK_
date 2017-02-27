from flask_wtf import Form
from wtforms import StringField,SubmitField,TextAreaField,BooleanField,SelectField
from wtforms import TextAreaField
from wtforms import ValidationError
from wtforms.validators import Required,Length,Email
from ..Models import Role,User
from flask_pagedown.fields import PageDownField


class NameForm(Form):
    name = StringField('你的名字？',validators=[Required(),])
    submit = SubmitField('Submit')

class EditorProfileForm(Form):
    name = StringField('游戏名称',validators=[Length(0,32)])
    location = StringField('地址',validators=[Length(0,64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')

class EditProfilrAdminForm(Form):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    username = StringField('管理员名称',validators=[Required(),Length(1,32)])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role',coerce=int)
    name = StringField('游戏名称',validators=[Length(0,32)])
    about_me = TextAreaField('关于我')
    location = StringField('地址',validators=[Required(),Length(0,64)])
    submit = SubmitField('提交')

    def __init__(self,user,*args,**kwargs):
        super(EditProfilrAdminForm,self).__init__(*args,**kwargs)
        self.role.choices = [(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self,field):
        if field.data != self.user.email and \
            User.query.filter_by(email=field.data):
            raise ValidationError('邮箱已存在!')
    def validate_username(self,field):
        if field.data != self.user.username and \
            User.query.filter_by(usernmae=field.data).first():
            raise ValidationError('用户名存在！')

class PostForm(Form):
    # body = TextAreaField('写点什么？')
    body = PageDownField('写点什么？',validators=[Required()])
    submit = SubmitField('提交')

class CommentForm(Form):
    body = StringField('',validators=[Required()])
    submit = SubmitField('提交评论')
