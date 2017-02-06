# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

# 登录表单定义
class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', ValidationError=[Required()])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('Log In')

# 注册表单定义
class RegistrationForm(Form):
    email = StringField('Email', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'username must have only letters.'
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('confirm password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email alreday registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username alreday in use')

# 变更密码表单定义
class changePasswordForm(Form):
    old_password = PasswordField('Old Password', validators=[Required()])
    password = PasswordField('New password', validators=[Required(),
                                                         EqualTo('password2', message='Password must match')])
    password2 = PasswordField('confirm new password', validators=[Required()])
    submit = SubmitField('update password')

# 密码重置请求表单
class PasswordRestRequstForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('Reset password')

# 密码重置表单
class PasswordResetForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password2', message='Password must match')
    ])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')

# 变更邮箱表单
class ChangeEmailForm(Form):
    email = StringField('New Email', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')