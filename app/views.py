# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from app import app, db, lm
from flask import render_template, flash, redirect, url_for, g, session, request, send_from_directory
from .forms import LoginForm, EditForm, PostFrom
from flask_login import current_user, login_required, login_user, logout_user
from .models import User, Post
from datetime import datetime
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from werkzeug import secure_filename
import os
import codecs
import markdown


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:id>', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(db.desc(Post.id))
    return render_template('index.html',
                           posts=posts
                           )
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

@app.route('/user/<username>')
@login_required
def user(username):
    username = User.query.filter_by(username=username).first()
    if username == None:
        flash('User ' + username + ' not found')
        return redirect(url_for('index'))
    posts = Post.query.all()
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
    return render_template('about.html')

def allow_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allow_filename(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url = url_for('uploaded_file', filename=filename)
            print file_url
            file_md = codecs.open('/'+ filename, mode='r', encoding='utf-8')
            text = file_md.read()
            content = markdown.markdown(text)
            title = filename.rsplit('.')[0]
            post = Post(title=title, content=content, timestamp=datetime.utcnow(), author=g.user)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('upload.html')



@app.route('/post/<int:id>')
def post(id=1):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)

@app.route('/posts')
def posts():
    posts = Post.query.order_by(db.desc(Post.id))
    return render_template('posts.html', posts=posts)

