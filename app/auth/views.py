# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask import redirect, render_template, flash, url_for, request
from .forms import LoginForm, RegistrationFrom
from flask_login import login_user, logout_user, current_user, login_required
from ..models import User
from . import auth
from .. import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = User.query.filter_by(username=form.username.data).first()
        if username is not None and username.verify_password(form.password.data):
            login_user(username, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.', "warning")
    return render_template('login.html',
                           title='Sign In',
                           form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationFrom()
    if form.validate_on_submit():
        username = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)
        db.session.add(username)
        db.session.commit()
        flash('You can now login')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/secret')
@login_required
def secret():
    return "Only autherticated users are allowed"