# -*- coding: utf-8 -*-

import os


class BaseConfig(object):

    # Get app root path
    # ../../configs/config.py
    _basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    PROJECT = "Controller"
    DEBUG = True
    TESTING = False

    ADMINS = frozenset(['trungnq13@fpt.com.vn'])

    # os.urandom(24)
    SECRET_KEY = '\xd2\x0c\xa9\xb7\xd9E\xda-\x1e\xdb;\xb8\x0c\xfc\xbf\xf3\x16[\xa2x\xd5s\x83\xe3'

class DevConfig(BaseConfig):

    DEBUG = True

    # ===========================================
    # Flask-mongokit
    #
    MONGODB_HOST            = '127.0.0.1'
    MONGODB_PORT            = 27017
    MONGODB_DATABASE        = 'fteluv'

    # ===========================================
    # Flask-babel
    #
    #PERMANENT_SESSION_LIFETIME = 3600 * 24 * 7

    # ===========================================
    # Flask-babel
    #
    ACCEPT_LANGUAGES = ['vi']
    BABEL_DEFAULT_LOCALE = 'en'

    # ===========================================
    # Flask-cache
    #
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60

    # ===========================================
    # Flask-mail
    #
    # Should be imported from env var.
    # https://bitbucket.org/danjac/flask-mail/issue/3/problem-with-gmails-smtp-server
    MAIL_DEBUG = DEBUG
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'gmail_username'
    MAIL_PASSWORD = 'gmail_password'
    DEFAULT_MAIL_SENDER = '%s@gmail.com' % MAIL_USERNAME
    # You should overwrite in production.py
    # Limited the maximum allowed payload to 16 megabytes.
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    USER_AVATAR_UPLOAD_FOLDER = "/tmp/uploads"
    #USER_AVATAR_UPLOAD_FOLDER = os.path.join(BaseConfig._basedir, 'uploads')


class TestConfig(BaseConfig):
    TESTING = True
    CSRF_ENABLED = False

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

