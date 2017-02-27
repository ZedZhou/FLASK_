from flask import render_template,session,redirect,url_for,flash,request,make_response
from datetime import datetime
from . import main
from flask_login import login_required,current_user
from .. import mail
from ..Models import User,Permission,Post,Comment
from flask import abort
from app01.main.forms import PostForm,CommentForm

@main.route('/',methods=['GET','POST'])
def hello_world():
    from app01.main.forms import NameForm
    form = NameForm()
    form2 = PostForm()
    if form2.validate_on_submit() and \
            current_user.can(Permission.WRITE_ARTICLE):
        post = Post(body=form2.body.data,author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.hello_world'))

    posts = Post.query.order_by(Post.timestamp.desc()).all()

    # if form.validate_on_submit():
    #     old_name = session.get('name')
    #     if old_name is not None and old_name != form.name.data:
    #         flash('看来你改变了你的名字!!!')
    #     session['name'] = form.name.data
    #     return redirect(url_for('.hello_world'))
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed',''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query


    page = request.args.get('page',1,type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page,per_page=current_app.config['FLASK_POSTS_PER_PAGE'],error_out=False
    )
    posts = pagination.items

    return render_template('user.html',
                           form=form,form2=form2,name=session.get('name'),posts=posts,
                           current_time=datetime.utcnow(),user=current_user,Permission=Permission,
                           pagination=pagination,show_followed=show_followed
                           )

@main.route('/user/<name>')
def show_name(name):
    user_agent = request.headers.get('User-Agent')
    return 'hello %s,your browser is %s' % (name,user_agent)

@main.route('/response')
def show_response():
    response = make_response('携带cookie!~~~')
    response.set_cookie('answer','44')
    return response

@main.route('/temp')
def temp():
    l =[1,2,3]
    return render_template('模板1.html',name='周冬雨',hello='<h2>你好啊</h2>',l=l)

@main.route('/boot')
# @login_required
def index():
    name='周冬雨'
    return render_template('bootstrap_demo.html',name=name,user=current_user,Permission=Permission)

@main.route('/register')
def new_user():
    pass

from flask_mail import Mail,Message
from flask import current_app
@main.route('/email')
def send_email():
    msg = Message('我是周冬雨，很高兴认识你。',sender=current_app.config['MAIL_USERNAME'],recipients=['253711560@qq.com'])
    msg.body = '这些是正文~~~。。。。'
    mail.send(msg)
    print(current_app.config['MAIL_USERNAME'])
    print('发送成功')
    return 'Sent ~~~!!!!'

@main.route('/username/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    posts = user.posts.order_by(Post.timestamp.desc()).all()

    if user is None:
        abort(404)
    return render_template('user_info.html',user=user,Permission=Permission,posts=posts)

from .forms import EditorProfileForm
from .. import db
from ..decorators import admin_required
@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditorProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('更改成功！')
        return redirect(url_for('.user',username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',form=form,Permission=Permission,user=current_user)

from .forms import EditProfilrAdminForm
from ..Models import Role
@main.route('/edit-profile/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfilrAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.name = form.name.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('管理员资料更新成功')
        return redirect(url_for('main.user',username=user.username,user=user))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role.id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me

    return render_template('edit_profile.html',form=form,user=user)

@main.route('/post/<int:id>',methods=['GET','POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('评论成功')
        return redirect(url_for('.post',id=post.id,page=-1))
    page = request.args.get('page',1,type=int)
    if page == -1:
        page = (post.comments.count()-1)/15 + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page,per_page=15,error_out=False

    )
    comments = pagination.items
    return render_template('post.html',posts=[post],form=form,
                           comments=comments,pagination=pagination,Permission=Permission
                           )


@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('修改文章成功')
        return redirect(url_for('main.post',id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html',form=form,Permission=Permission)

# 关注
from ..decorators import Permission,permission_required
@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户')
        return redirect(url_for('.hello_world'))
    if current_user.is_following(user):
        flash('你已经关注了次用户')
        return redirect(url_for('.user',username=username))
    current_user.follow(user)
    flash('成功关注 %s' % username)
    return redirect(url_for('.user',username=username))
# 取消关注
@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户')
        return redirect('.hello_world')
    if current_user.is_following(user):
        current_user.unfollow(user)
        flash('取消关注 %s 成功'% user.username)
    return redirect(url_for('.user',username=username))

@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户')
        return redirect(url_for('.hello_world'))
    page = request.args.get('page',1,type=int)
    pagination = user.followers.paginate(
        page,per_page=20,error_out=False
    )
    follows = [{'user':item.follower,'timestamp':item.timestamp}
               for item in pagination.items
               ]
    return render_template('followers.html',user=user,
                           title='Followers of',
                           endpoint='.followers',pagination=pagination,
                           follows=follows
                           )

@main.route('/followed/<username>')
def followed(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户')
        return redirect('.hello_world')
    page = request.args.get('page',1,type=int)
    pagination = user.followed.paginate(
        page,per_page=20,error_out=False
    )
    followeds =[{'user':item.followed,'timestamp':item.timestamp}
                for item in pagination.items
                ]
    return render_template('followeds.html',user=user,title='我的关注',
                           endpoint='.followed',pagination=pagination,
                           followeds=followeds,Permission=Permission)

@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.hello_world')))
    resp.set_cookie('show_followed','',max_age=60*60*24*7)
    return resp

@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.hello_world')))
    resp.set_cookie('show_followed','1',max_age=60*60*24*7)
    return resp

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page',1,type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page,per_page=15,error_out=False
    )
    comments = pagination.items
    return render_template('moderate.html',comments=comments,
                           page=page,pagination=pagination,Permission=Permission)

# 管理评论路由
@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled=False
    db.session.add(comment)
    return redirect(url_for('.moderate',page=request.args.get('page',1,type=int)))

@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate',page=request.args.get('page',1,type=int)))
