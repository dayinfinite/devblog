# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, ValidationError, Form
from wtforms.validators import DataRequired, Length, Required, Email
from ..models import User
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField(u'用户名', validators=[DataRequired(), Length(0 ,20, message=u"用户名长度0到20")],
                           render_kw={'class':'form-control', 'placeholder': u'用户名'})
    password = PasswordField(u'密码', validators=[DataRequired(), Length(0, 20, message=u'密码长度0到20')],
                             render_kw={'class': 'form-control', 'placeholder': u'用户名'})
    remember_me = BooleanField('remember', default=False)

class RegistrationFrom(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('username', validators=[DataRequired(), Length(0, 20, message=u'用户名长度0到20')])
    password = PasswordField('password', validators=[DataRequired(), Length(0, 20, message=u'用户名长度0到20')])
    password2 = PasswordField('confirm', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email alreday registered')

    def validate_username(self, field):
        if User.query.filter_by(password=field.data).first():
            raise ValidationError('username alreday registered')