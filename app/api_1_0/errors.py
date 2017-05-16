# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask import jsonify
from . import api
from wtforms import ValidationError
def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response
def badrequest(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 400
    return response

@api.errorhandler(ValidationError)
def validation_error(e):
    return badrequest(e.args[0])
