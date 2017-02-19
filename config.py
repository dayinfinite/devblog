# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

CSRF_ENABLED = True
SECRET_KEY = 'You-will-never-give-up'
POSTS_PER_PAGE = 10
MAX_SEARCH_RESULTS = 50
UPLOAD_FOLDER = '/devblog/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'md'])

import os
basedir = os.path.abspath(os.path.dirname(__file__))
WHOOSH_BASE = os.path.join(basedir, 'search.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True