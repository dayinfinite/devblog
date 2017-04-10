# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask import render_template
from . import main
from .. import db

@main.app_errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500