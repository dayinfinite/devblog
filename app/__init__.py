# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
app=Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
from app import views, models