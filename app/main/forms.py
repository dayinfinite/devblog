# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Use
from config import Config


class PostForm(Form):
    title = StringField('title', validators=[Required(), Length(0 ,64)])
    body = PageDownField("What is on your mind", validators=[Required()])
    subject = SelectField('subject', validators=[Required(), choice=(s for s in Config.SUBJECTS)])
    tags = StringField('tags')
    submit = SubmitField('Submit')
