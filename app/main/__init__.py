# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask import Blueprint

main=Blueprint('main', __name__)

from . import views, forms, errors
