# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask import Blueprint

main=Blueprint('main', __name__)

from . import views, forms, errors
from ..models import Permission

@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)
