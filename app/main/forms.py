# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, validators, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from ..models import User
from flask_pagedown.fields import PageDownField

class EditForm(FlaskForm):
    username = StringField(u'用户', validators=[DataRequired(), Length(0, 64)])
    location = StringField(u'地区', validators=[DataRequired(), Length(0, 64)])
    about_me = TextAreaField(u'个人介绍', validators=[Length(min=0, max=140)])
    submit = SubmitField(u'确认')

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
    post = PageDownField('Post', validators=[DataRequired()])
    submit = SubmitField('Submit')