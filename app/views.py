# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from app import app, db, lm
from flask import render_template, flash, redirect, url_for, g, session, request
from .forms import LoginForm, EditForm, PostFrom, SearchForm
from flask_login import current_user, login_required, login_user, logout_user
from .models import User, Post
from datetime import datetime
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from werkzeug import secure_filename
import os

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:id>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    form = PostFrom()
    if form.validate_on_submit():
        post = Post(content=form.post.data, timestamp=datetime.utcnow(), author=g.user)
        print  post.timestamp, post.content, post.author
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    posts = Post.query.paginate(page, POSTS_PER_PAGE, False)
    return render_template('index.html',
                           user=user,
                           posts=posts,
                           form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = User.query.filter_by(username=form.username.data).first()
        if username is not None:
            login_user(username, form.remember_me.data)
            return redirect('index')
        flash('Invalid username or password.', "warning")
    return render_template('login.html',
                           title='Sign In',
                           form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.before_request
def before_requst():
    g.user = current_user


@app.route('/user/<username>')
@login_required
def user(username):
    username = User.query.filter_by(usernamne=username).first()
    if username == None:
        flash('User ' + username + ' not found')
        return redirect(url_for('index'))
    posts = [
        {'author': user,
         'title': 'post1',
         'body': 'Test post #1'
         },
        {'author': user,
         'title': 'post2',
         'body': 'Test post #2'}
    ]
    return render_template('user.html',
                           user=user,
                           posts=posts)

@app.before_request
def brfore_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.username)
    if form.validate_on_submit():
        g.user.username = form.username.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit'))
    else:
        form.username.data = g.user.username
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/about')
def about():
    return redirect('about.html')

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html',
                           query=query,
                           results=results)

def allow_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allow_filename(file.filename):
            filename  = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url = url_for('upload_file', filename=filename)
            return redirect(url_for('index'))
    return render_template('upload.html')