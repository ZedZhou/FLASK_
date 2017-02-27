from flask import g,jsonify,redirect,request,current_app,url_for
from . import api
from ..Models import User,Post
from .decorators import permission_required
from ..Models import Permission,Comment
from .. import db

@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or404(id)
    return jsonify(user.to_json())

@api.route('users/<int:id>/posts/')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page',1,type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page,per_page=15,error_out=False
    )
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_posts',page=page-1,_external=True)
        next = None
    if pagination.has_next:
        next = url_for('api.get_user_posts',page=page+1,_external=True)
    return jsonify({
        'posts':[post.to_json() for post in posts],
        'prev':prev,
        'next':next,
        'count':pagination.total
    })

# 关注用户的posts
@api.route('/users/<int:id>/timeline')
def get_user_followed_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page',1,type=int)
    pagination = user.followed_posts.order_by(Post.timestamp.desc()).paginate(
        page,per_page=15,error_out=False
    )
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_followed_posts', page=page - 1,
                       _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_followed_posts', page=page + 1,
                       _external=True)
    return jsonify({
        'posts':[post.to_json() for post in posts],
        'prev':prev,
        'next':next,
        'count':pagination.total
    })

# 添加评论
@api.route('posts/<int:id>/comments',methods=['POST'])
@permission_required(Permission.COMMENT)
def new_post_comment(id):
    post = Post.query.get_or_404(id)
    # comment = Comment(body=body)
    comment = Comment.from_json(request.json)
    comment.author = g.current_user
    comment.post = post
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()),201,\
           {'Location':url_for('api.get_comment',id=comment.id,_external=True)}

