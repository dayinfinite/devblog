# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask import render_template, session, redirect, url_for, flash, request, g
from . import main
from .forms import EditForm, PostFrom
from ..models import User, Post
from .. import db
from flask_login import current_user, login_required, login_user, logout_user
from datetime import datetime
from werkzeug import secure_filename
import os
import codecs
import markdown

@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
@main.route('/index/<int:id>', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(db.desc(Post.id))
    return render_template('index.html',
                           posts=posts
                           )

@main.route('/user/<username>')
@login_required
def user(username):
    username = User.query.filter_by(username=username).first()
    if username == None:
        flash('User ' + username + ' not found')
        return redirect(url_for('main.index'))
    posts = Post.query.all()
    return render_template('user.html',
                           user=user,
                           posts=posts)

@main.route('/edit', methods=['GET', 'POST'])
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

@main.route('/about')
def about():
    return render_template('about.html')

# @main.route('/uploads/<filename>')
# @login_required
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# @main.route('/upload', methods=['GET', 'POST'])
# @login_required
# def upload_file():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allow_filename(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             file_url = url_for('uploaded_file', filename=filename)
#             print file_url
#             file_md = codecs.open('/'+ filename, mode='r', encoding='utf-8')
#             text = file_md.read()
#             content = markdown.markdown(text)
#             title = filename.rsplit('.')[0]
#             post = Post(title=title, content=content, timestamp=datetime.utcnow(), author=g.user)
#             db.session.add(post)
#             db.session.commit()
#             return redirect(url_for('index'))
#     return render_template('upload.html')



@main.route('/post/<int:id>')
def post(id=1):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)

@main.route('/posts')
def posts():
    posts = Post.query.order_by(db.desc(Post.id))
    return render_template('posts.html', posts=posts)






