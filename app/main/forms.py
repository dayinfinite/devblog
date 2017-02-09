# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import User
from config import Config


class PostForm(Form):
    title = StringField('title', validators=[Required(), Length(0 ,64)])
    body = PageDownField("What is on your mind", validators=[Required()])
    tags = StringField('tags')
    submit = SubmitField('Submit')
