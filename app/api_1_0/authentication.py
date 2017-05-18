# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask_httpauth import HTTPBasicAuth
from ..models import User
from . import api
from flask import g, jsonify
from .errors import forbidden, unauthorized
auth=HTTPBasicAuth()

@auth.verify_password
def verify_password(user_or_token, password):

    if password == '':
        g.current_user = User.verify_auth_token(user_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(username=user_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_userd = False
    return user.verify_password(password)

@auth.error_handler
def auth_error():
    return unauthorized('Invaild credentials')

@api.route('/token')
def get_token():

    # if g.token_used:
    #     return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(expiration=3600), 'expiration': 3600})

