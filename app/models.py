# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'


from . import db, login_manager
from werkzeug.security import  generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for
from datetime import datetime
import hashlib
from markdown import markdown
from app.exceptions import ValidationError
import bleach

#项目数据库定义
#定义用户表
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

#    @property
#    def password(self):
#        raise AttributeError('password is not readable attribute')
#
#    @password.setter
#    def password(self, password):
#        self.password_hash = generate_password_hash(password)
#
#    def verify_password(self, password):
#        return check_password_hash(self.password_hash, password)
#
#    def generate_confirmation_token(self, expiration=3600):
#        s = Serializer(current_app.config['SECRET_KEY'], expiration)
#        return s.dumps({'confirm':self.id})
#
#    def gravatar(self, size=100, default='identicon', rating='g'):
#        if request.is_secure:
#            url = 'https://secure.gravatar.com/avatar'
#        else:
#            url = 'http://www.gravatar.com/avatar'
#        hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
#        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
#            url=url, hash=hash, size=size, default=default, rating=rating
#        )
#
#
#    def to_json(self):
#        json_user = {
#            'url': url_for('api.get_user', id=self.id, _external=True),
#            'username': self.username,
#            'memeber_since': self.member_since,
#            'last_seen': self.last_seen,
#            'posts': url_for('api.get_user_posts', id=self.id, _external=True),
#            'followed_posts': url_for('api.get_user_followed_posts', id=self.id, _external=True),
#            'post_count': self.post.count()
#        }
#        return json_user

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#定义文章表
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    tags = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    def __repr__(self):
        return '<Post %r>' % (self.body)
#
#    def to_json(self):
#        json_post = {
#            'url': url_for('api.get_post', id=self.id, _external=True),
#            'body': self.body,
#            'body_html': self.body_html,
#            'timestamp': self.timestamp,
#            'author': url_for('apt.get_user', id=self.author_id),
#            'comments': url_for('api.get_post_comments', id=self.id, _external=True),
#            'comment_count': self.comment.count()
#        }
#        return json_post
#
#    @staticmethod
#    def from_json(json_post):
#        body = json_post.get('body')
#        if body is None or body == '':
#            raise ValidationError('post does not have a body')
#        return Post(body=body)
#db.event.listen(Post.body, 'set', Post.on_changed_body)

# 定义评论表
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    @staticmethod
    def on_change_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True
        ))

    def to_json(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id, _external=True),
            'post': url_for('api.get_post', id=self.id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id, _external=True)
        }
        return json_comment

    @staticmethod
    def from_json(json_comment):
        body = json_comment.get('body')
        if body is None or body == '':
            raise ValidationError('comment does not have a body')
        return  Comment(body=body)

db.event.listen(Comment.body, 'set', Comment.on_change_body)
