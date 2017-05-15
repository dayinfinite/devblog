# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask_login import login_required
from . import api

@api.route('/posts/')
def get_posts():
    pass