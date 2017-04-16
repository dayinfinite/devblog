# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Required, Email
from ..models import User

class LoginForm(FlaskForm):
    # email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField(u'用户名', validators=[DataRequired(), Length(0 ,20, message=u"用户名长度0到20")],
                           render_kw={'class':'form-control', 'placeholder': u'用户名'})
    password = PasswordField(u'密码', validators=[DataRequired(), Length(0, 20, message=u'密码长度0到20')],
                             render_kw={'class': 'form-control', 'placeholder': u'密码'})
    remember_me = BooleanField('remember', default=False)
    submit = SubmitField(u'登录', render_kw={'type': 'submit', 'class': 'btn btn-default'})

class RegistrationFrom(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()],
                        render_kw={'class': 'form-control', 'placeholder': u'邮箱'})
    username = StringField('username', validators=[DataRequired(), Length(0, 20, message=u'用户名长度0到20')],
                           render_kw={'class': 'form-control', 'placeholder': u'用户'}
                           )
    password = PasswordField('password', validators=[DataRequired(), Length(0, 20, message=u'用户名长度0到20')],
                             render_kw={'class': 'form-control', 'placeholder': u'密码'}
                             )
    password2 = PasswordField('confirm', validators=[Required()],
                              render_kw={'class': 'form-control', 'placeholder': u'密码'})
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email alreday registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username alreday registered')