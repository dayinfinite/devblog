# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEAROWN=True
    FLASKY_MAIL_SUBJECT_PREFIX= 'Devblog'
    FLASKY_MAIL_SENDER='Flasky Admin <zsq941556540@163.com>'
    FLASKY_ADMIN=os.environ.get('john')
    FLASK_POSTS_PER_PAGE = 3
    SUBJECTS = [
        "python文章",
        "WEB技术",
        "Linux"
    ]

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI=os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config={
    'development':DevelopmentConfig,
    'testing': TestingConfig,
    'producting': ProductionConfig,
    'default': DevelopmentConfig
}
