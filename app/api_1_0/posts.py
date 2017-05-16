# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

from flask import request, jsonify, url_for
from ..models import Post
from .. import db, auth
from . import api

@api.route('/posts/')
@auth.login_required
def get_posts():
    posts = Post.query.all()
    return jsonify({'posts': [post.to_json() for post in posts]})

@api.route('/post/<int:id>')
@auth.login_required
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())

@api.route('/posts/', method=['POST'])
def new_post():
    post = Post.from_json(request.json)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, {'Location': url_for('api.get_post', id=post.id, _external=True) }

@api.route('/posts/<int:id>', method=['PUT'])
@auth.login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    post.content = request.json.get('content', post.content)
    db.session.add(post)
    return jsonify(post.to_json())