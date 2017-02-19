# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown
from flask_moment import Moment

UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app=Flask(__name__)
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
pagedown = PageDown(app)
moment = Moment(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
from app import views, models