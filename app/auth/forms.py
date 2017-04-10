# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Required, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('username', validators=[DataRequired(), Length(0 ,20, message=u"用户名长度0到20")])
    password = PasswordField('password', validators=[DataRequired(), Length(0, 20, message=u'密码长度0到20')])
    remember_me = BooleanField('remember', default=False)