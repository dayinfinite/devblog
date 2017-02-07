# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('submit')

class EditProfileFrom(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Loaction', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('submit')

class EditProfileAdminFrom(Form):
    email = StringField('Email', validators=[Required(), Length(0, 64), Email()])
    username = StringField('Username', validators=[Required(), Length(0, 64), Required('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminFrom, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if field.data != self.user.name and User.query.filter_by(username=field.data).first():
            raise ValidationError('username alreday in use')

class PostForm(Form):
    body = PageDownField("What is on your mind", validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(Form):
    body = StringField('Enter your comment', validators=[Required()])
    submit = SubmitField('Submit')