# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from . import db, login_manager
from werkzeug.security import  generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from datetime import datetime
import hashlib
from markdown import markdown
import bleach

#项目数据库定义

#角色表定义
class Role(db.Model):
    __tablename__ = 'roles'


