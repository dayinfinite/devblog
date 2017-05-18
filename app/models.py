# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'


from . import db, login_manager
from flask import current_app, url_for
from hashlib import md5
from flask_login import UserMixin
from markdown import markdown
import bleach
from wtforms import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import Serializer
import datetime
class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    location = db.Column(db.String(64))
    about_me = db.Column(db.String(140))
    member_since = db.Column(db.DateTime(), default=datetime.datetime.now())
    last_seen = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
    def ping(self):
        self.last_seen = datetime.datetime.utcnow()
        db.session.add(self)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)

    @staticmethod
    def make_unique_username(username):
        if User.query.filter_by(username=username).first() == None:
            return username
        version = 2
        while True:
            new_username = username +str(version)
            if User.query.filter_by(username=new_username).first() == None:
                break
            version += 1
        return new_username

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %s' % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(), default=datetime.datetime.now())
    tags = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @staticmethod
    def on_changed_article(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em',
                        'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3',
                        'p']
        target.content = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True
        ))

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'title': self.title,
            'content': self.content,
            'tags': self.tags
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        content=json_post.get('content')
        if content is None or content == "":
            raise ValidationError('post does not have a content')
        return Post(title=json_post.get('title'), content=content, timestamp=json_post.get('timestamp'), tags=json_post.get('tags'))

    def __repr__(self):
        return '<Post %s>' % self.content

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
