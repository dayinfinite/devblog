# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, validators
from wtforms.validators import DataRequired, Length, EqualTo
from .models import User

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(0 ,20, message=u"用户名长度0到20")])
    password = PasswordField('password', validators=[DataRequired(), Length(0, 20, message=u'密码长度0到20')])
    remember_me = BooleanField('remember', default=False)

class EditForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_username, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.original_username =original_username

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.username.data == self.original_username:
            return True
        user = User.query.filter_by(username=self.username.data).first()
        if user != None:
            self.username.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True

class PostFrom(FlaskForm):
    post = StringField('post', validators=[DataRequired()])


class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])

