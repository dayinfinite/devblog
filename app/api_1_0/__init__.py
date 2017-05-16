# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, posts, errors
