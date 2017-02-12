# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from app import db, lm
from hashlib import md5
from app import app
import flask_whooshalchemy as whooshalchemy
enable_search = True

# import sys
# if sys.version_info >= (3, 0):
#     enable_search = False
# else:
#     enable_search = True
#     import flask_whooshalchemy as whooshalchemy

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

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

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

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

    def __repr__(self):
        return '<User %s' % self.username

class Post(db.Model):
    __searchable__ = ['body']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %s>' % self.content

if enable_search:
    whooshalchemy.whoosh_index(app, Post)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

