# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from app import app

@app.route('/')
@app.route('/index')
def index():
    return 'Hello, World'